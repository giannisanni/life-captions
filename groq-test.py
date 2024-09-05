import cv2
import base64
from io import BytesIO
from PIL import Image
import time
import pyttsx3
import os
from groq import Groq

# ... (previous imports and initializations remain the same)

# Updated PROMPT_TEMPLATES
PROMPT_TEMPLATES = {
    "nature_documentary": """As a humorous narrator for "{title}" (Episode {episode}), continue the story based on this new scene: {description}. 
    Previous context: {context}
    Create a funny 3-4 sentence narration that builds on the previous events. Be comical, use puns, introduce absurd 'facts', and use dramatic pauses (...) or ALL CAPS for effect. 
    Maintain continuity with previous episodes if similar elements are present.""",
    
    "dnd": """As the Dungeon Master for an ongoing D&D campaign "{title}" (Session {episode}), engage directly with the person(s) visible in this scene: {description}.
    Previous context: {context}
    In 3-4 sentences:
    1. Describe the fantastic setting or situation the person(s) find themselves in, incorporating elements from the real image into a fantasy context.
    2. Present a challenge, decision, or roleplaying opportunity directly to the person(s) in the image.
    3. Ask a specific question or prompt a choice that the person(s) need to make to progress the story.
    Use vivid fantasy descriptions, address the person(s) directly as their character(s), and maintain continuity with previous sessions if possible."""
}

# ... (other functions remain the same)

def select_template():
    while True:
        print("\nAvailable prompt templates:")
        for i, key in enumerate(PROMPT_TEMPLATES.keys(), 1):
            print(f"{i}. {key}")
        choice = input("Choose a prompt template (enter the number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(PROMPT_TEMPLATES):
                return list(PROMPT_TEMPLATES.keys())[index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    story_title = ""
    episode_count = 1
    story_history = []
    
    # Choose initial prompt template
    current_template = select_template()
    
    try:
        while True:
            if manual_mode:
                user_input = input("Press Enter to capture the next image, or type 'switch' to change prompt template: ")
                if user_input.lower() == 'switch':
                    current_template = select_template()
                    continue
            else:
                print("Capturing next image automatically...")
                time.sleep(5)  # Increased delay for automatic capture
            
            pil_image = capture_image_from_webcam(cap)
            if pil_image:
                image_base64 = pil_to_base64(pil_image)
                
                # Analyze image
                image_description = analyze_image(image_base64)
                
                if not story_title:
                    # Create a story title based on the first image description
                    title_prompt = f"Create a witty title for a {'D&D campaign' if current_template == 'dnd' else 'comical nature documentary series'} based on this description: {image_description}. Keep it short and catchy."
                    story_title = generate_text(title_prompt)
                    print(f"New {'Campaign' if current_template == 'dnd' else 'Series'}: {story_title}")
                
                # Generate continuous narrative
                context = ". ".join(story_history[-3:]) if story_history else ""
                
                narration_prompt = PROMPT_TEMPLATES[current_template].format(
                    title=story_title,
                    episode=episode_count,
                    description=image_description,
                    context=context
                )
                
                response = generate_text(narration_prompt)
                print(f"{'Session' if current_template == 'dnd' else 'Episode'} {episode_count}:")
                print(response)
                
                # Add to story history
                story_history.append(response)
                
                # Use Text-to-Speech on the response
                engine.say(response)
                engine.runAndWait()
                
                # For D&D mode, prompt for player response
                if current_template == "dnd" and manual_mode:
                    player_response = input("Your response (or press Enter to continue): ")
                    if player_response:
                        story_history.append(f"Player: {player_response}")
                
                # Increment episode count
                episode_count += 1
                
                # Small delay to ensure TTS is complete before next iteration
                time.sleep(2)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        cap.release()
        engine.stop()

if __name__ == "__main__":
    main()
