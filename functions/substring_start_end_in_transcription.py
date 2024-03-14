from functions.audio_transcription_to_text import audio_transcription_to_text
from functions.audio_transcription_to_words import audio_transcription_to_words


def substring_start_end_in_transcription(audio_transcription, substring):

    text = audio_transcription_to_text(audio_transcription)
    words_with_time = audio_transcription_to_words(audio_transcription)
    words = text.split()
    target_words = substring.split()
    target_len = len(target_words)

    for i in range(len(words)):
        if words[i:i+target_len] == target_words:
            #print('Found substring in', (i, i+target_len-1))
            return words_with_time[i]['start'], words_with_time[i+target_len-1]['end']

    return -1, -1
