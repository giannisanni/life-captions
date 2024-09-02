import cv2
import base64
from io import BytesIO
from PIL import Image
from langchain_community.llms import Ollama
import time
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from playsound import playsound
import os
import threading
import queue

# Initialize Ollama
llava = Ollama(model="moondream")

# Initialize ElevenLabs client
elevenlabs_client = ElevenLabs(
    api_key="",
)

# Queue to store processed narrations
narration_queue = queue.Queue()

# Event to signal the narration thread to stop
stop_event = threading.Event()

def convert_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def capture_image_from_webcam(cap):
    success, frame = cap.read()
    if success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        return pil_image
    else:
        print("Failed to capture image")
        return None

def text_to_speech(text):
    audio_stream = elevenlabs_client.text_to_speech.convert_as_stream(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )
    
    # Save the audio stream to a temporary file
    with open("temp_audio.mp3", "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    
    # Play the audio
    playsound("temp_audio.mp3")
    
    # Remove the temporary file
    os.remove("temp_audio.mp3")

def process_image(image):
    image_b64 = convert_to_base64(image)
    llm_with_image_context = llava.bind(images=[image_b64])
    response = llm_with_image_context.invoke("Describe what you see. You are narrating a documentary of someone's life, do not use the word image when describing to keep the immersion. You may also make jokes about what you see. Begin like this: 'This scene shows....'")
    narration_queue.put(response)

def narration_thread():
    while not stop_event.is_set():
        try:
            narration = narration_queue.get(timeout=1)
            print(narration)
            text_to_speech(narration)
        except queue.Empty:
            continue

# Start the webcam
cap = cv2.VideoCapture(0)

# Start the narration thread
narration_thread = threading.Thread(target=narration_thread)
narration_thread.start()

try:
    while True:
        pil_image = capture_image_from_webcam(cap)
        if pil_image:
            # Process image in a separate thread
            threading.Thread(target=process_image, args=(pil_image,)).start()
        
        # Wait for 5 seconds before capturing the next image
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping...")
    stop_event.set()
    narration_thread.join()
finally:
    cap.release()  # Make sure to release the webcam
