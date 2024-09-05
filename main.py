import cv2
import time
import os
import sys
import threading
import select
import logging
from image_utils import capture_image_from_webcam, pil_to_base64
from text_utils import analyze_image, generate_text, text_to_speech, get_groq_api_key
from ui_utils import select_template
from templates import PROMPT_TEMPLATES
from story_manager import StoryManager
from audio_utils import transcribe_audio, interpret_choice
from audio_recorder import record_audio, get_audio_file_path
from config import *

# Set up logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

running = True

def get_voice_input(audio_file, result, is_open_ended=False):
    logger.info(f"Starting voice recording to {audio_file}")
    record_audio(audio_file, duration=AUDIO_RECORD_SECONDS)
    logger.info(f"Voice recording completed. File size: {os.path.getsize(audio_file)} bytes")
    try:
        logger.info("Starting transcription...")
        transcribed_response = transcribe_audio(audio_file)
        logger.info(f"Transcription result: {transcribed_response}")
        if transcribed_response:
            if is_open_ended:
                result['voice'] = transcribed_response
            else:
                interpreted_choice = interpret_choice(transcribed_response)
                if interpreted_choice != "UNCLEAR":
                    result['voice'] = interpreted_choice
            logger.info(f"Valid {'response' if is_open_ended else 'choice'} detected: {result['voice']}")
            return
        logger.warning(f"No valid {'response' if is_open_ended else 'choice'} found in transcription")
    except Exception as e:
        logger.error(f"Error in voice recognition: {e}")
    result['voice'] = None
    logger.info("Voice input process completed without a valid response")

def get_player_input(voice_input, story_manager, image_description, is_open_ended):
    result = {'voice': None, 'typed': None}
    audio_file = get_audio_file_path()
    
    if voice_input:
        logger.info("Voice input enabled. Starting voice recognition...")
        voice_thread = threading.Thread(target=get_voice_input, args=(audio_file, result, is_open_ended))
        voice_thread.start()
    
    prompt = "Please speak or type your response..." if is_open_ended else "Please speak or type your choice (A, B, C, or D)..."
    print(prompt)
    
    typed_input = None
    timeout = time.time() + USER_INPUT_TIMEOUT
    while time.time() < timeout and typed_input is None:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            typed_input = sys.stdin.readline().strip()
            if not is_open_ended:
                typed_input = typed_input.upper()
                if typed_input not in ['A', 'B', 'C', 'D']:
                    typed_input = interpret_choice(typed_input)
    
    if voice_input:
        logger.info("Waiting for voice recognition to complete...")
        voice_thread.join()
    
    voice_input = result['voice']
    
    logger.info(f"Voice input: {voice_input}")
    logger.info(f"Typed input: {typed_input}")
    
    recordings = sorted([f for f in os.listdir(RECORDINGS_DIR) if f.startswith('audio_input_')])
    for old_file in recordings[:-2]:
        old_file_path = os.path.join(RECORDINGS_DIR, old_file)
        logger.info(f"Removing old recording: {old_file_path}")
        os.remove(old_file_path)
    
    final_input = None
    if voice_input and typed_input:
        if voice_input != typed_input:
            print(f"Voice input recognized as: {voice_input}")
            print(f"Typed input recognized as: {typed_input}")
            confirmation = input("Which input do you want to use? (voice/typed): ").lower()
            final_input = voice_input if confirmation.startswith('v') else typed_input
        else:
            final_input = voice_input
    elif voice_input:
        final_input = voice_input
    elif typed_input:
        final_input = typed_input
    
    if final_input:
        logger.info(f"Final input: {final_input}")
        if is_open_ended:
            return story_manager.process_player_response(final_input, image_description)
        else:
            return story_manager.process_player_choice(final_input, image_description)
    else:
        logger.warning("No valid input detected. Prompting user for manual input.")
        while True:
            manual_input = input("Enter your response: " if is_open_ended else "Enter A, B, C, or D: ").strip()
            if is_open_ended or manual_input.upper() in ['A', 'B', 'C', 'D']:
                if is_open_ended:
                    return story_manager.process_player_response(manual_input, image_description)
                else:
                    return story_manager.process_player_choice(manual_input.upper(), image_description)
            else:
                logger.warning("Invalid choice entered.")
                print("Invalid choice. Please enter A, B, C, or D.")

def check_for_commands(story_manager):
    global running
    while running:
        command = input().lower().strip()
        if command == 'quit':
            running = False
            print("Quitting application...")
        elif command == 'save':
            story_manager.save_story()
            print("Story saved.")
        elif command == 'switch':
            story_manager.current_template = select_template()
            print(f"Switched to template: {story_manager.current_template}")
        elif command == 'help':
            print("Available commands: quit, save, switch, help")
        else:
            print("Unknown command. Type 'help' for a list of commands.")

def main():
    global running
    running = True
    
    try:
        api_key = get_groq_api_key()
        logger.info("API key set successfully.")
    except ValueError as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}")
        return

    manual_mode = input(MANUAL_MODE_PROMPT).lower().strip() == 'y'
    voice_input = input(VOICE_INPUT_PROMPT).lower().strip() == 'y'
    
    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        logger.error("Could not open webcam.")
        print("Error: Could not open webcam.")
        return

    story_manager = StoryManager()
    
    load_existing = input(LOAD_STORY_PROMPT).lower().strip() == 'y'
    if load_existing:
        story_manager.load_story()
    else:
        story_manager.start_new_story()
    
    command_thread = threading.Thread(target=check_for_commands, args=(story_manager,))
    command_thread.start()
    
    try:
        while running:
            if manual_mode:
                print("Press Enter to capture the next image, or type a command (type 'help' for options)...")
                if input().strip():
                    continue
            else:
                print("Looking... (Type 'help' for available commands)")
                time.sleep(IMAGE_CAPTURE_INTERVAL)
            
            pil_image = capture_image_from_webcam(cap)
            if pil_image:
                image_base64 = pil_to_base64(pil_image)
                
                image_description = analyze_image(image_base64)
                
                narrative, questions, question_type = story_manager.generate_narrative(image_description)
                print(f"{'Session' if story_manager.current_template == 'dnd' else 'Episode'} {story_manager.episode_count}:")
                print(narrative)
                
                text_to_speech(narrative)
                
                if question_type is not None:  # Skip for life-captions mode
                    print("\nQuestion:")
                    print(questions)
                    text_to_speech(questions)
                    
                    is_open_ended = (question_type == "open_ended")
                    if is_open_ended:
                        print("Please provide your thoughts or decision:")
                    else:
                        print("Choose an option (A, B, C, or D):")
                    
                    choice_response = get_player_input(voice_input, story_manager, image_description, is_open_ended)
                    print("Outcome:", choice_response)
                    text_to_speech(choice_response)
                
                story_manager.episode_count += 1
                
                time.sleep(2)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt detected. Saving story and exiting...")
    finally:
        running = False
        command_thread.join()
        story_manager.save_story()
        cap.release()
        logger.info("Story saved. Program terminated.")

if __name__ == "__main__":
    main()
