import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, AutoFeatureExtractor
from transformers.generation.streamers import BaseStreamer
import sounddevice as sd
import cv2
import base64
from io import BytesIO
from IPython.display import clear_output
from PIL import Image
from langchain_community.llms import Ollama
import time
import threading
import math
from queue import Queue
import numpy as np

class ParlerTTSStreamer(BaseStreamer):
    def __init__(self):
        self.device = "mps"  # Changed from "cuda:0" to "cpu"
        torch_dtype = torch.float32  # Changed from float16 to float32 for CPU compatibility
       
        repo_id = "parler-tts/parler_tts_mini_v0.1"
        self.tokenizer = AutoTokenizer.from_pretrained(repo_id)
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(repo_id)

        self.SAMPLE_RATE = self.feature_extractor.sampling_rate

        self.model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True).to(self.device)
        self.decoder = self.model.decoder
        self.audio_encoder = self.model.audio_encoder
        self.generation_config = self.model.generation_config

        self.sampling_rate = self.model.audio_encoder.config.sampling_rate
        frame_rate = self.model.audio_encoder.config.frame_rate

        play_steps_in_s = 2.0
        play_steps = int(frame_rate * play_steps_in_s)

        # variables used in the streaming process
        self.play_steps = play_steps

        hop_length = math.floor(self.audio_encoder.config.sampling_rate / self.audio_encoder.config.frame_rate)
        self.stride = hop_length * (play_steps - self.decoder.num_codebooks) // 6
        self.token_cache = None
        self.to_yield = 0

        # variables used in the thread process
        self.audio_queue = Queue()
        self.stop_signal = None
        self.timeout = None

    # The rest of the ParlerTTSStreamer class methods remain the same

# The rest of your script remains largely the same, but ensure all references to CUDA are removed or changed to CPU

llava = Ollama(model="moondream")

# Initialize TTS streamer
tts_streamer = ParlerTTSStreamer()

# ... (rest of your functions)

# Start the webcam
cap = cv2.VideoCapture(0)

try:
    while True:
        pil_image = capture_image_from_webcam(cap)
        if pil_image:
            image_b64 = convert_to_base64(pil_image)
            
            llm_with_image_context = llava.bind(images=[image_b64])
            response = llm_with_image_context.invoke("what do you see? do not use the word image when describing. describe what you see like you are narrating a documentary")
            print(response)
            
            # Generate and play audio in a separate thread
            audio_thread = threading.Thread(target=lambda: play_audio_stream(text_to_speech_stream(response)))
            audio_thread.start()
            
            # Clear the output to prevent flooding
            clear_output(wait=True)
            
            # Sleep to avoid overloading
            time.sleep(0.1)  # Reduced sleep time
            
            # Wait for audio to finish before next iteration
            audio_thread.join()

except KeyboardInterrupt:
    print("Stopped.")
finally:
    cap.release()  # Make sure to release the webcam
