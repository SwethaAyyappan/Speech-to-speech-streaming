from googletrans import Translator, LANGUAGES

def smart_chunk_text(text, max_length=2000):
    """Split text into smaller chunks while preserving sentence boundaries."""
    chunks = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind(".")
        if split_index == -1:
            split_index = max_length
        chunks.append(text[:split_index + 1].strip())
        text = text[split_index + 1:].strip()
    chunks.append(text.strip())
    return chunks


def translate_text():
    try:
        translator = Translator()

        # Ask user for input file
        input_file_path = input("Enter the path of the input text file: ").strip()

        # Display supported languages
        print("Supported Languages:")
        for code, language in LANGUAGES.items():
            print(f"{code}: {language}")

        # Ask user for target language code
        target_language = input("Enter the target language code (from the list above): ").strip()

        # Read text from input file
        with open(input_file_path, "r", encoding="utf-8") as f:
            text = f.read()

        if not text.strip():
            print("The input file is empty. Please provide valid content.")
            return

        print(f"Translating the text to '{LANGUAGES.get(target_language, target_language)}'...")

        # Split text into manageable chunks
        text_chunks = smart_chunk_text(text)

        # Translate and write each chunk sequentially
        output_file_path = input_file_path.replace(".txt", f"_translated_{target_language}.txt")
        with open(output_file_path, "w", encoding="utf-8") as f:
            for chunk in text_chunks:
                translation = translator.translate(chunk, dest=target_language)
                f.write(translation.text + "\n")

        print("Translation successful!")
        print(f"Translated text saved to {output_file_path}")

    except Exception as e:
        print("An error occurred during translation:", e)

if __name__ == "__main__":
    translate_text()
