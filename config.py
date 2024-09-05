import os

# API Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Audio Configuration
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_CHUNK = 1024
AUDIO_RECORD_SECONDS = 5

# Image Configuration
WEBCAM_INDEX = 0
IMAGE_CAPTURE_INTERVAL = 5  # seconds between automatic captures

# Story Configuration
MAX_HISTORY_CONTEXT = 3
MAX_TITLE_WORDS = 5

# User Interface
MANUAL_MODE_PROMPT = "Do you want to confirm before each picture is taken? (y/n): "
VOICE_INPUT_PROMPT = "Do you want to enable voice input for choices? (y/n): "
LOAD_STORY_PROMPT = "Do you want to load an existing story? (y/n): "

# File Paths
RECORDINGS_DIR = 'recordings'
STORIES_DIR = 'saved_stories'

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
LOG_FILE = 'webcam_storyteller.log'

# Text-to-Speech Configuration
TTS_VOICE_RATE = 160

# Timeout Configuration
USER_INPUT_TIMEOUT = 5  # seconds
RETRY_DELAY = 60  # seconds
MAX_RETRIES = 3

# Model Configuration
DEFAULT_TEXT_MODEL = "llama3-groq-70b-8192-tool-use-preview"
IMAGE_ANALYSIS_MODEL = "llava-v1.5-7b-4096-preview"

# Story Modes
STORY_MODES = ["nature_documentary", "dnd", "mystery_detective", "time_travel", "superhero_chronicles", "sci-fi_adventure"]

