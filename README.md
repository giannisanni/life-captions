# Life Captions App
=====================

A Python application that uses computer vision and natural language processing to generate humorous narrations of webcam captures.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [How it Works](#how-it-works)
* [Troubleshooting](#troubleshooting)

## Installation

### Install Ollama

Follow the instructions to install Ollama on your system:

* **Linux:** 
    1. Open your terminal and run the following command:
       ```bash
       curl -fsSL https://ollama.com/install.sh | sh
       ```
* **Windows:** 
    1. Download the Ollama installer from the official [Ollama website](https://ollama.com/).
    2. Run the installer and follow the installation prompts.
* **Mac (via Homebrew):** 
    1. Open your terminal and run the following command:
       ```bash
       brew install ollama
       ```

### Download Required Model

After installing Ollama, download the required model by running the following command:

```bash
ollama pull llava-phi3
```

### Install Requirements

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Make sure you have the `requirements.txt` file in the same directory as your `app.py` file. The `requirements.txt` file should contain the following dependencies:

```
opencv-python
base64
Pillow
pyttsx3
langchain-community
```

## Usage

To run the application, execute the following command:

```bash
python app.py
```

## How it Works

The Life Captions App uses the following steps to generate humorous narrations:

1. **Webcam Setup**: The application connects to the default webcam.
2. **Image Capture**: The application captures an image from the webcam and converts it to a base64-encoded string.
3. **Title Generation**: The first time the application runs, it generates a witty title for a comical nature documentary series based on the captured image.
4. **Narration Generation**: For each subsequent run, the application generates a concise and entertaining narration based on the current image, focusing on the most prominent or interesting elements.
5. **Text-to-Speech**: The generated narration is then read aloud using a Text-to-Speech engine.
6. **Output Clearing**: To prevent flooding, the application clears the previous output after each run.

## Troubleshooting

If you encounter any issues during the installation or usage of the application, try the following:

* Verify that you have installed Ollama correctly by checking its version: `ollama --version`.
* Ensure that you have downloaded the required model (`llava-phi3`) using the `ollama pull` command.
* Check the application logs for any error messages or exceptions.

If you are still experiencing issues, please contact the developers or search for solutions online.




# Webcam Storyteller

Webcam Storyteller is a Python project that uses computer vision and natural language processing to generate creative stories based on images captured from your webcam. It features multiple storytelling modes, including a humorous nature documentary and an interactive D&D campaign.

## Features

- Automatic or manual image capture from webcam
- Image analysis using the Groq API
- Text generation for storytelling
- Multiple storytelling modes (Nature Documentary, D&D Campaign)
- Text-to-Speech narration
- Story saving and loading

## Requirements

- Python 3.7+
- OpenCV
- Pillow
- pyttsx3
- Groq API client

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/webcam-storyteller.git
   cd webcam-storyteller
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install opencv-python pillow pyttsx3 groq
   ```

4. Set up your Groq API key:
   - Sign up for a Groq API account and obtain your API key
   - Set the `GROQ_API_KEY` environment variable:
     ```
     export GROQ_API_KEY='your-api-key-here'  # On Windows, use `set GROQ_API_KEY=your-api-key-here`
     ```

## Usage

Run the main script:
```
python main.py
```

Follow the on-screen prompts to:
1. Choose between manual and automatic image capture
2. Load an existing story or start a new one
3. Select a storytelling mode (Nature Documentary or D&D Campaign)

### Manual Mode

In manual mode, you'll be prompted before each image capture. You can:
- Press Enter to capture the next image
- Type 'switch' to change the storytelling mode
- Type 'save' to manually save the current story
- Type 'quit' to save and exit the program

### Automatic Mode

In automatic mode, images will be captured automatically at regular intervals. To stop the program, press Ctrl+C (or Cmd+C on Mac).

### D&D Mode

In D&D mode, you'll be presented with choices (A, B, C, or D) after each narrative segment. Your choices will influence the direction of the story.

## Quitting and Saving

1. Manual Mode:
   - Type 'quit' when prompted to save and exit
   - Type 'save' to save the story and continue
   - Press Ctrl+C (or Cmd+C on Mac) to interrupt, save, and exit

2. Automatic Mode:
   - Press Ctrl+C (or Cmd+C on Mac) to interrupt, save, and exit

In all cases, you'll see a confirmation message that the story has been saved before the program exits.

## File Structure

- `main.py`: The main script that runs the program
- `story_manager.py`: Manages story state, saving, and loading
- `image_utils.py`: Functions for image capture and processing
- `text_utils.py`: Functions for text generation, image analysis, and text-to-speech
- `ui_utils.py`: User interface functions
- `templates.py`: Contains the prompt templates for different storytelling modes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


# Webcam Storyteller

Webcam Storyteller is a Python project that uses computer vision and natural language processing to generate creative stories based on images captured from your webcam. It features multiple storytelling modes, including a humorous nature documentary and an interactive D&D campaign.

## Features

- Automatic or manual image capture from webcam
- Image analysis using the Groq API
- Text generation for storytelling
- Multiple storytelling modes (Nature Documentary, D&D Campaign)
- Text-to-Speech narration
- Story saving and loading

## Requirements

- Python 3.7+
- OpenCV
- Pillow
- pyttsx3
- Groq API client

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/webcam-storyteller.git
   cd webcam-storyteller
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install opencv-python pillow pyttsx3 groq
   ```

4. Set up your Groq API key:
   - Sign up for a Groq API account and obtain your API key
   - Set the `GROQ_API_KEY` environment variable:
     ```
     export GROQ_API_KEY='your-api-key-here'  # On Windows, use `set GROQ_API_KEY=your-api-key-here`
     ```

## Usage

Run the main script:
```
python main.py
```

Follow the on-screen prompts to:
1. Choose between manual and automatic image capture
2. Load an existing story or start a new one
3. Select a storytelling mode (Nature Documentary or D&D Campaign)

### Manual Mode

In manual mode, you'll be prompted before each image capture. You can:
- Press Enter to capture the next image
- Type 'switch' to change the storytelling mode
- Type 'save' to manually save the current story
- Type 'quit' to save and exit the program

### Automatic Mode

In automatic mode, images will be captured automatically at regular intervals. To stop the program, press Ctrl+C (or Cmd+C on Mac).

### D&D Mode

In D&D mode, you'll be presented with choices (A, B, C, or D) after each narrative segment. Your choices will influence the direction of the story.

## Saving and Loading Stories

### Saving

- Stories are automatically saved when you exit the program.
- In manual mode, you can also type 'save' to save the current story at any time.
- The story is saved as a JSON file. The filename is created from a cleaned version of the story title, limited to 50 characters.

### Loading

- When starting the program, you'll be asked if you want to load an existing story.
- If you choose to load a story, you'll be prompted to enter the filename of the saved story.
- Enter the full filename, including the `.json` extension.

## File Structure

- `main.py`: The main script that runs the program
- `story_manager.py`: Manages story state, saving, and loading
- `image_utils.py`: Functions for image capture and processing
- `text_utils.py`: Functions for text generation, image analysis, and text-to-speech
- `ui_utils.py`: User interface functions
- `templates.py`: Contains the prompt templates for different storytelling modes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
