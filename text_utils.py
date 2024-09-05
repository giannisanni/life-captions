import pyttsx3
from groq import Groq
import os
import time
import logging
from config import TTS_VOICE_RATE, RETRY_DELAY, MAX_RETRIES, DEFAULT_TEXT_MODEL, IMAGE_ANALYSIS_MODEL

logger = logging.getLogger(__name__)

def get_groq_api_key():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY environment variable is not set.")
        api_key = input("Please enter your Groq API key: ").strip()
        if not api_key:
            raise ValueError("API key is required to run this program.")
        os.environ["GROQ_API_KEY"] = api_key
    return api_key

# Initialize Groq client
try:
    client = Groq(api_key=get_groq_api_key())
except ValueError as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    raise

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', TTS_VOICE_RATE)

def analyze_image(image_base64):
    for attempt in range(MAX_RETRIES):
        try:
            completion = client.chat.completions.create(
                model=IMAGE_ANALYSIS_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image and provide a brief description in 50 words or less:"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_base64
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0,
                top_p=1,
                stream=False,
                stop=None
            )
            logger.info("Image analysis completed successfully")
            return completion.choices[0].message.content.strip()
        except Exception as e:
            if "rate_limit_exceeded" in str(e) and attempt < MAX_RETRIES - 1:
                logger.warning(f"Rate limit exceeded. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Error analyzing image: {e}")
                return "Error analyzing image"
    
    logger.error("Failed to analyze image after multiple attempts")
    return "Failed to analyze image after multiple attempts"

def generate_text(prompt, model=DEFAULT_TEXT_MODEL):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=model,
            max_tokens=500
        )
        logger.info("Text generation completed successfully")
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        return "Error generating text"

def text_to_speech(text):
    try:
        engine.say(text)
        engine.runAndWait()
        logger.info("Text-to-speech completed successfully")
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
