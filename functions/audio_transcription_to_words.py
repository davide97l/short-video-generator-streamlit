import json


def audio_transcription_to_words(json_file_path, output_file=None):

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    words = []
    for segment in data["segments"]:
        reference_words = segment["text"].split()
        i, j = 0, 0
        while i < len(segment["words"]):
            word = segment["words"][i]["word"].strip()
            x = 0
            while reference_words[j] != word:
                i += 1
                if i >= len(segment["words"]):
                    break
                word += segment["words"][i]["word"]
                x += 1
            words.append({"word": word, "start": segment["words"][i-x]["start"], "end": segment["words"][i]["end"]})
            i += 1
            j += 1

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(words, f, indent=4)  # Indentation for better readability

    return words
