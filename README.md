# Speech-to-Speech Video Translation and Integration

This project is a streamlined pipeline for extracting, translating, and reintegrating audio content into video files. It enables seamless conversion of video audio into another language with a translated voice-over.

---

## Key Features
1. **Audio Extraction from Video**: Isolates the audio track from the input video file for further processing.
2. **Speech-to-Text Conversion**: Transforms extracted audio into textual format using speech recognition.
3. **Language Translation**: Converts the transcribed text into the target language.
4. **Text-to-Speech Synthesis**: Generates speech audio from the translated text.
5. **Audio-Video Synchronization**: Merges the translated audio back into the original video seamlessly.

---

## Project Overview
- **`main.py`**: Script for running the pipeline programmatically without a graphical interface.
- **`main_app.py`**: Gradio-based web application to provide an interactive and user-friendly UI for the pipeline.

### Core Components
- **`audiototext.py`**: Responsible for converting audio into text using speech recognition tools.
- **`extract_audio.py`**: Handles the process of extracting audio from video files.
- **`translate_text.py`**: Implements functionality for translating the extracted text into a specified language.
- **`translatedtext_to_speech.py`**: Converts translated text into synthetic speech audio.
- **`Merge_audio_to_video.py`**: Reinserts the translated audio into the original video while preserving synchronization.

---

## Installation Instructions
1. Clone this repository to your local machine.
Clone this repository to your local machine:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
3. Install the required dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt





# How to Use  

## Command Line Usage  
To run the pipeline programmatically:  

```bash
python main.py
```

## Web Application  
To launch the Gradio-based web UI:  

```bash
python main_app.py
```

1. Open the provided Gradio URL in your browser.

2. Upload the video file you want to process.

3. Select the target language and follow the steps in the UI to complete the translation process.


## Dependencies
Make sure to install all the necessary dependencies listed in requirements.txt before running the project. Use the following command:

```bash
pip install -r requirements.txt
```

This ensures that all required libraries and packages are installed for smooth execution of the pipeline.










