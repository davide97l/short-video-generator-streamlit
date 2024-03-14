import json


def audio_transcription_to_words(json_file_path, output_file=None):

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    words = []
    for segment in data["segments"]:
        for word in segment["words"]:
            words.append({"word": word["word"], "start": word["start"], "end": word["end"]})

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(words, f, indent=4)  # Indentation for better readability

    return words
