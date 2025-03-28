import edge_tts
from langdetect import detect
import os

async def text_to_speech_edgetts(input_file_path, output_file_path):
    try:
        # Read the text file
        with open(input_file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            print("⚠️ The input file is empty. Please provide valid content.")
            return

        # Detect language using langdetect
        detected_language = detect(text)
        print(f"🌍 Detected language: {detected_language}")

        # Map detected language to an EdgeTTS voice
        language_voice_map = {
            "en": "en-US-JennyNeural",  # English (US)
            "ta": "ta-IN-PallaviNeural",  # Tamil
            "hi": "hi-IN-SwaraNeural",  # Hindi
            "fr": "fr-FR-DeniseNeural",  # French
            "es": "es-ES-ElviraNeural",  # Spanish
        }

        voice = language_voice_map.get(detected_language, "en-US-JennyNeural")  # Default to English
        print(f"🗣 Using voice: {voice}")

        # Create EdgeTTS object
        communicator = edge_tts.Communicate(text, voice)

        # Generate speech and save it as an MP3 file
        print("🔊 Generating speech...")
        await communicator.save(output_file_path)
        print(f"✅ Speech saved: {output_file_path}")

        # Ensure the file was created
        if not os.path.exists(output_file_path):
            print(f"❌ Error: Expected audio file {output_file_path} was not created!")

    except Exception as e:
        print(f"❌ An error occurred during text-to-speech conversion: {e}")
