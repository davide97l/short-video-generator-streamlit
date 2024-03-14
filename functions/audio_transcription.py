import whisper
import json
import os


def audio_transcription(audio_path, output_path=None, word_level=True):
    """
    Transcribes a video using Whisper and saves the results with timestamps to a JSON file.

    Args:
      audio_path: Path to the video file.
      output_path: Path to save the transcription JSON file.
    """

    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=word_level)

    # Ensure the result is a JSON-serializable dictionary
    if not isinstance(result, dict):
        try:
            result = json.loads(result)  # Attempt to convert to a dictionary
        except json.JSONDecodeError:
            print("Warning: Transcription result is not in a JSON-compatible format. It will be saved as a plain string.")

    # Determine output path if not provided
    if not output_path:
        # Extract filename without extension
        filename, _ = os.path.splitext(os.path.basename(audio_path))
        # Generate output path in the same folder with ".json" extension
        output_path = os.path.join(os.path.dirname(audio_path), f"{filename}.json")

    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)  # Save as indented JSON

    return output_path
