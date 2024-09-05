import os
from groq import Groq
import logging
from config import GROQ_API_KEY, DEFAULT_TEXT_MODEL

logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(audio_file_path):
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="distil-whisper-large-v3-en",
                response_format="verbose_json",
            )
        logger.info(f"Audio transcription completed for {audio_file_path}")
        return transcription.text
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return None

def interpret_choice(transcribed_text):
    try:
        prompt = f"""
        Given the following transcribed text from a user, determine which option (A, B, C, or D) they are choosing.
        If no clear choice is made, return "UNCLEAR".

        Transcribed text: "{transcribed_text}"

        Respond with only the letter of the chosen option or "UNCLEAR".
        """

        response = client.chat.completions.create(
            model=DEFAULT_TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that interprets user choices."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0
        )

        interpreted_choice = response.choices[0].message.content.strip().upper()
        logger.info(f"Interpreted choice: {interpreted_choice}")

        if interpreted_choice in ['A', 'B', 'C', 'D']:
            return interpreted_choice
        else:
            return "UNCLEAR"
    except Exception as e:
        logger.error(f"Error interpreting choice: {e}")
        return "UNCLEAR"
