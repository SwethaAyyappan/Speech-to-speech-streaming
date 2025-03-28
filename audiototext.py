import os
import whisper

def transcribe_audio(audio_file, model_size):
    try:
        # Load the selected Whisper model
        print(f"Loading the {model_size} model...")
        model = whisper.load_model(model_size)

        # Transcribe the audio
        print("Transcribing audio...")
        result = model.transcribe(audio_file)

        # Generate output file name in the same directory as the audio file
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_file = os.path.join(os.path.dirname(audio_file), f"{base_name}_transcription.txt")

        # Save the transcription to the output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])

        # Confirmation messages
        print("Transcription successful!")
        print(f"Transcription saved to {output_file}")

        return output_file  # Return the transcription file path

    except Exception as e:
        print("An error occurred during transcription:", e)
        return None  # Return None on error

if __name__ == "__main__":
    print("Welcome to the Whisper Transcription Tool!")

    # Prompt user to input the path to the audio file
    audio_file = input("Enter the full path to the audio file: ").strip()

    # Prompt user to select a Whisper model
    print("\nSelect the Whisper model size:")
    print("1. tiny\n2. base\n3. small\n4. medium\n5. large")
    model_choice = input("Enter the number corresponding to your choice (1-5): ").strip()

    # Map user input to the model size
    model_sizes = {
        "1": "tiny",
        "2": "base",
        "3": "small",
        "4": "medium",
        "5": "large"
    }
    model_size = model_sizes.get(model_choice, "base")  # Default to "base" if input is invalid

    # Call the transcription function
    transcription_path = transcribe_audio(audio_file, model_size)

    if transcription_path:
        print(f"Transcription file created: {transcription_path}")
    else:
        print("Transcription failed.")
