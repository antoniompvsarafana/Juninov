import requests

def transcribe_audio(file_path):
    """
    Transcribes a single audio file using OpenAI Whisper.

    Args:
        file_path (str or Path): Path to the audio file (.wav, .mp3, etc.)

    Returns:
        str: The transcription text (also saved as a .txt file)
    """
    

    import os
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    print(f"Transcribing: {file_path}\n")


    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(str(file_path)) as source:
            audio = r.record(source)
            # Language set to en-US; change if needed
            transcript_text = r.recognize_google(audio, language="en-UK")

        return transcript_text

    except Exception as e:
        print("Transcription failed:", e)
        return None


# Example usage:
# transcribe_audio("audio_data/example.wav")
