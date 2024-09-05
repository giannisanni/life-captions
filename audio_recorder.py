import pyaudio
import wave
import os
import logging
from config import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS, AUDIO_CHUNK, AUDIO_RECORD_SECONDS, RECORDINGS_DIR

logger = logging.getLogger(__name__)

def record_audio(filename, duration=AUDIO_RECORD_SECONDS, sample_rate=AUDIO_SAMPLE_RATE, chunk=AUDIO_CHUNK, channels=AUDIO_CHANNELS):
    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

        logger.info(f"Recording for {duration} seconds...")

        frames = []

        for i in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        logger.info("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        logger.info(f"Audio saved as {filename}")
    except Exception as e:
        logger.error(f"Error during audio recording: {e}")

def get_audio_file_path():
    if not os.path.exists(RECORDINGS_DIR):
        os.makedirs(RECORDINGS_DIR)
        logger.info(f"Created directory: {RECORDINGS_DIR}")
    
    base_filename = 'audio_input'
    extension = '.wav'
    counter = 1
    while os.path.exists(f"{RECORDINGS_DIR}/{base_filename}_{counter}{extension}"):
        counter += 1
    
    filename = f"{RECORDINGS_DIR}/{base_filename}_{counter}{extension}"
    logger.info(f"Generated audio file path: {filename}")
    return filename
