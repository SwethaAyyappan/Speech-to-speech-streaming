import subprocess
import os

def sync_audio_with_video(video_path, translated_audio_path):
    """
    Syncs the translated audio with the original video using FFmpeg.
    
    Parameters:
    - video_path (str): Path to the original video file.
    - translated_audio_path (str): Path to the translated audio file.
    
    Returns:
    - str: Path to the synchronized video file.
    """
    try:
        # Validate paths
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        if not os.path.exists(translated_audio_path):
            raise FileNotFoundError(f"Audio file not found: {translated_audio_path}")
        
        # Extract the directory and filename from the input video path
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(video_dir, f"{video_name}_final_translated_video.mp4")
        
        # FFmpeg command to sync audio and video
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-i", video_path,  # Input video
            "-i", translated_audio_path,  # Input audio
            "-c:v", "copy",  # Copy video without re-encoding
            "-c:a", "aac",  # Encode audio to AAC format
            "-map", "0:v:0",  # Select the video stream from the first input
            "-map", "1:a:0",  # Select the audio stream from the second input
            "-shortest",  # Trim output to the shortest input stream
            output_path  # Output file
        ]

        # Execute FFmpeg command
        subprocess.run(ffmpeg_cmd, check=True)

        # Ensure the output file exists
        if os.path.exists(output_path):
            print(f"✅ Audio and video synchronized successfully! Output saved to: {output_path}")
            return output_path
        else:
            raise FileNotFoundError(f"⚠️ FFmpeg process completed, but output file not found: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    return None  # Return None if something went wrong

# Example usage:
if __name__ == "__main__":
    video_path = input("Enter the path of the input video file: ")
    translated_audio_path = input("Enter the path of the translated audio file: ")
    output_file = sync_audio_with_video(video_path, translated_audio_path)
    if output_file:
        print(f"🎬 Final video saved at: {output_file}")
    else:
        print("❌ Synchronization failed.")
