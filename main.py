import os
import asyncio
from extract_audio import extract_audio
from audiototext import transcribe_audio
from translate_text import smart_chunk_text
from translatedtext_to_speech import text_to_speech_edgetts
from Merge_audio_to_video import sync_audio_with_video
from googletrans import Translator, LANGUAGES

def main():
    print("Welcome to the Speech Audio Translation Tool!")
    
    try:
        # Step 1: Get user inputs
        video_path = input("Enter the path to the input video file: ").strip()
        if not os.path.isfile(video_path):
            print("Error: The video file does not exist. Exiting.")
            return

        print("\nSelect Whisper model size:")
        print("1. tiny\n2. base\n3. small\n4. medium\n5. large")
        model_choice = input("Enter the number corresponding to your choice (1-5): ").strip()
        model_sizes = {
            "1": "tiny",
            "2": "base",
            "3": "small",
            "4": "medium",
            "5": "large"
        }
        model_size = model_sizes.get(model_choice, "base")  # Default to "base" if input is invalid

        print("\nSupported Languages for Translation:")
        for code, language in LANGUAGES.items():
            print(f"{code}: {language}")
        target_language = input("\nEnter the target language code (e.g., 'es' for Spanish, 'fr' for French): ").strip()
        if target_language not in LANGUAGES:
            print("Error: Invalid language code. Exiting.")
            return

        # Step 2: Extract audio from the video
        audio_path = os.path.splitext(video_path)[0] + "_audio.wav"
        print("\nExtracting audio from the video...")
        extract_audio(video_path, audio_path)
        if not os.path.isfile(audio_path):
            print("Error: Audio extraction failed. Exiting.")
            return

        # Step 3: Transcribe audio to text
        transcription_path = os.path.splitext(audio_path)[0] + "_transcription.txt"
        print("\nTranscribing audio to text using Whisper...")
        transcribe_audio(audio_path, model_size)
        if not os.path.isfile(transcription_path):
            print("Error: Transcription failed. Exiting.")
            return

        # Step 4: Translate text
        print("\nTranslating the transcribed text...")
        translator = Translator()
        with open(transcription_path, "r", encoding="utf-8") as f:
            text = f.read()

        translated_text_path = transcription_path.replace(".txt", f"_translated_{target_language}.txt")
        with open(translated_text_path, "w", encoding="utf-8") as f:
            text_chunks = smart_chunk_text(text)
            for chunk in text_chunks:
                translation = translator.translate(chunk, dest=target_language)
                f.write(translation.text + "\n")

        print(f"Translation successful! Translated text saved to {translated_text_path}")

        # Step 5: Convert translated text to speech
        translated_audio_path = translated_text_path.replace(".txt", "_speech.mp3")
        print("\nGenerating translated speech audio...")
        asyncio.run(text_to_speech_edgetts(translated_text_path))
        if not os.path.isfile(translated_audio_path):
            print("Error: Text-to-speech conversion failed. Exiting.")
            return

        # Step 6: Merge translated audio with the original video
        print("\nMerging translated audio back into the video...")
        sync_audio_with_video(video_path, translated_audio_path)

        print("\nProcess complete! The final video with the translated audio has been created.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

