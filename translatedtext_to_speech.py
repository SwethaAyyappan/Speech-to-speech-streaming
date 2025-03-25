import edge_tts
from langdetect import detect
import asyncio
import os

async def text_to_speech_edgetts(input_file_path):
    try:
        # Read the text file
        with open(input_file_path, "r", encoding="utf-8") as f:
            text = f.read()

        if not text.strip():
            print("The input file is empty. Please provide valid content.")
            return

        # Detect language using langdetect
        detected_language = detect(text)
        print(f"Detected language code: {detected_language}")

        # Map detected language to an EdgeTTS voice
        language_voice_map = {
            "en": "en-US-JennyNeural",  # English (US)
            "ta": "ta-IN-PallaviNeural",  # Tamil
            "hi": "hi-IN-SwaraNeural",  # Hindi
            "fr": "fr-FR-DeniseNeural",  # French
            "es": "es-ES-ElviraNeural",  # Spanish
        }

        voice = language_voice_map.get(detected_language, "en-US-JennyNeural")  # Default to English
        print(f"Using voice: {voice}")

        # Create EdgeTTS object
        communicator = edge_tts.Communicate(text, voice)

        # Define the output file path
        output_file_path = input_file_path.replace(".txt", "_speech.mp3")

        # Generate speech and save it as an MP3 file
        print("Generating speech...")
        await communicator.save(output_file_path)
        print(f"Speech generation successful! Audio saved to: {output_file_path}")

    except Exception as e:
        print("An error occurred during text-to-speech conversion:", e)

def run_text_to_speech():
    input_file_path = input("Enter the path of the translated text file: ").strip()
    if os.path.isfile(input_file_path):
        asyncio.run(text_to_speech_edgetts(input_file_path))
    else:
        print("The specified file does not exist. Please check the path and try again.")

if __name__ == "__main__":
    run_text_to_speech()
