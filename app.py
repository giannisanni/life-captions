import cv2
import base64
from io import BytesIO
from IPython.display import clear_output
from PIL import Image
from langchain_community.llms import Ollama
import time
import pyttsx3

llava = Ollama(model="llava-phi3")
engine = pyttsx3.init()
VoiceRate = 160
engine.setProperty('rate', VoiceRate)

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

# Start the webcam
cap = cv2.VideoCapture(0)

story_title = ""
episode_count = 1

try:
    while True:
        pil_image = capture_image_from_webcam(cap)
        if pil_image:
            image_b64 = convert_to_base64(pil_image)
            
            if not story_title:
                # First run: Create a story title
                title_prompt = "Based on what you see in this image, create a witty title for a comical nature documentary series. The title should be short, catchy, and relate to the main subject or theme you observe."
                llm_with_image_context = llava.bind(images=[image_b64])
                story_title = llm_with_image_context.invoke(title_prompt)
                print(f"New Series: {story_title}")
            
            prompt = f"""You are the narrator of a comical nature documentary series titled "{story_title}". This is episode {episode_count}.

Analyze the current image and describe what you see, focusing on the most prominent or interesting elements. Your narration should:
1. Be entirely based on the current image, without referencing any previous observations.
2. Maintain the style of a nature documentary, but with a humorous twist.
3. Poke fun at the scene, making comical remarks and comparisons.
4. Introduce absurd "facts" about the subjects in view.
5. Use dramatic pauses and exaggerated tones (indicated by ... or ALL CAPS) for comedic effect.

Keep your response concise (2-3 sentences) and make it entertaining! Remember, you're telling a ridiculous story about the 'wildlife' you observe in this specific image!

Important: Ensure that your response is unique and different from any previous narrations. Do not repeat the same phrases or ideas."""
            
            llm_with_image_context = llava.bind(images=[image_b64])
            response = llm_with_image_context.invoke(prompt)
            print(f"Episode {episode_count}: {response}")
            
            # Use Text-to-Speech on the response
            engine.say(response)
            engine.runAndWait()
            
            # Clear the output to prevent flooding
            clear_output(wait=True)
            
            # Increment episode count
            episode_count += 1
            
            # Sleep to avoid overloading
            time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    cap.release()
    engine.stop() 
