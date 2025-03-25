import ffmpeg
import os

def extract_audio(video_file, audio_file):
    """
    Extracts audio from a given video file and saves it as a WAV file.
    
    Parameters:
    video_file (str): Path to the input video file.
    audio_file (str): Path to save the extracted audio.
    
    Returns:
    str: Path to the extracted audio file, or None if extraction fails.
    """

    
    try:
        # Configure FFmpeg to extract audio with specific settings
        ffmpeg.input(video_file).output(
            audio_file, format='wav', acodec='pcm_s16le', ac=1, ar='16000'
        ).run(overwrite_output=True, quiet=True)
        print(f"Audio has been successfully extracted to: {audio_file}")
        return audio_file
    except Exception as error:
        print(f"Error occurred during audio extraction: {error}")
        return None

def main():
    # Get the video file path from the user
    video_path = input("Enter the path to the video file: ").strip()

    # Check if the video file exists
    if not os.path.isfile(video_path):
        print("The file you entered does not exist. Please check the path and try again.")
        return

    # Generate a default audio file name based on the video file name
    audio_output_path = os.path.splitext(video_path)[0] + "_audio.wav"

    # Extract the audio
    extract_audio(video_path, audio_output_path)

if __name__ == "__main__":
    main()
