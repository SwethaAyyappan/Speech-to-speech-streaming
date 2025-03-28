import os
import gradio as gr
import asyncio
from extract_audio import extract_audio
from audiototext import transcribe_audio
from translate_text import smart_chunk_text
from translatedtext_to_speech import text_to_speech_edgetts
from Merge_audio_to_video import sync_audio_with_video
from googletrans import Translator, LANGUAGES

# Convert language dictionary to user-friendly format
language_options = [f"{name.capitalize()} ({code})" for code, name in LANGUAGES.items()]
language_mapping = {f"{name.capitalize()} ({code})": code for code, name in LANGUAGES.items()}

async def process_video(video_file, model_size, target_language):
    try:
        video_path = video_file.name

        # Extract the language code
        target_language = language_mapping.get(target_language, target_language)

        # Validate file format
        allowed_extensions = (".mp4", ".avi", ".mov", ".mkv")
        if not video_path.lower().endswith(allowed_extensions):
            return None, "❌ Error: Please upload a valid video file (mp4, avi, mov, mkv).", None

        base_dir = os.path.abspath(os.path.dirname(video_path))  # Ensure correct path
        temp_dir = os.path.join(base_dir, "translated_output")
        os.makedirs(temp_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(video_path))[0]

        # Define paths for intermediate and output files
        audio_path = os.path.join(temp_dir, f"{base_name}_audio.wav")
        transcription_path = os.path.join(temp_dir, f"{base_name}_transcription.txt")
        translated_text_path = os.path.join(temp_dir, f"{base_name}_translated_{target_language}.txt")
        translated_audio_path = os.path.join(temp_dir, f"{base_name}_speech.mp3")  # ✅ Ensuring correct naming

        print(f"🎥 Processing video: {video_path}")
        print(f"📝 Temp Directory: {temp_dir}")

        # Step 1: Extract Audio
        extract_audio(video_path, audio_path)
        print(f"🎵 Audio extracted: {audio_path}")

        # Step 2: Transcribe Audio
        transcription_path = transcribe_audio(audio_path, model_size)
        print(f"📜 Transcription saved: {transcription_path}")

        if not os.path.exists(transcription_path):
            return None, f"❌ Error: Transcription file not found: {transcription_path}", None

        # Step 3: Translate Text
        translator = Translator()
        with open(transcription_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        with open(translated_text_path, "w", encoding="utf-8") as f:
            text_chunks = smart_chunk_text(text)
            for chunk in text_chunks:
                translation = translator.translate(chunk, dest=target_language)
                f.write(translation.text + "\n")

        print(f"🌍 Translation completed: {translated_text_path}")

        # Step 4: Convert Translated Text to Speech
        print(f"🔊 Calling TTS function with: {translated_text_path}")
        await text_to_speech_edgetts(translated_text_path, translated_audio_path)  # ✅ Await TTS function
        print(f"✅ Checking if audio exists: {translated_audio_path}, Exists: {os.path.exists(translated_audio_path)}")

        # ✅ Check if the audio file exists before merging
        if not os.path.exists(translated_audio_path):
            return None, f"❌ Error: Audio file not found: {translated_audio_path}", None

        # Step 5: Merge Translated Audio with Video
        output_video_path = sync_audio_with_video(video_path, translated_audio_path)
        if not output_video_path:
            return None, "❌ Error: Merging failed. No output video generated.", None

        print(f"🎬 Merged Video: {output_video_path}")

        message = "✅ Translation successful! Download your video below."
        return output_video_path, message, output_video_path

    except Exception as e:
        return None, f"❌ Error: {str(e)}", None

iface = gr.Interface(
    fn=lambda video, model, lang: asyncio.run(process_video(video, model, lang)),  # Run async function
    inputs=[
        gr.File(label="📂 Upload Video", type="filepath", file_types=["video/*"]),
        gr.Radio(["tiny", "base", "small", "medium", "large"], label="🎙 Select Whisper Model"),
        gr.Dropdown(language_options, label="🌍 Target Language")
    ],
    outputs=[
        gr.Video(label="🎬 Translated Video"),
        gr.Textbox(label="📌 Status Message"),
        gr.File(label="⬇️ Download Translated Video")
    ],
    title="🔊 Speech-to-Speech Video Translation",
    description="🎥 Upload a video, select a Whisper model, choose a target language, and get a translated video with dubbed audio.",
    allow_flagging="never"  # 🚫 Disable the flag button
)

iface.launch()
