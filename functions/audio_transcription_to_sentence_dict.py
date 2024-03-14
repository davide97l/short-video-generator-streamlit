import whisper
import json
import os


def audio_transcription_to_sentence_dict(json_file_path):
    sentence_info = []
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        for segment in json_data["segments"]:
            sentence_dict = {}
            sentence_dict['text'] = segment['text']
            sentence_dict['start'] = segment['start']
            sentence_dict['end'] = segment['end']
            sentence_dict['duration'] = segment['end'] - segment['start']
            sentence_info.append(sentence_dict)
        return sentence_info
