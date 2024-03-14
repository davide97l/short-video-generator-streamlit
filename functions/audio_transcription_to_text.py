import json


def audio_transcription_to_text(json_file_path):
    """
    This function takes a JSON-like string and returns the value of the key 'text' as a string.

    Args:
        json_string: A JSON-like string.

    Returns:
        The value of the key 'text' as a string, or None if the key is not found or the JSON is invalid.
    """
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            return data.get('text').strip()
    except (json.JSONDecodeError, KeyError, IOError):
        return None

