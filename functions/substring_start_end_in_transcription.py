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


if __name__ == '__main__':
    audio_transcription = '../data2/These_5_Books_Scaled_My_Business_to_Multiple_6_Figures.json'
    substring = "You just need to know how people think. And that's literally it besties the six books that help me go from zero to 100,000 dollar months in on the two years. It may be a secret weapon for me, but as I reminded from me to you, stop reading, just read, start reading to act. In this era of new education, we don't wait to get tested. We test ourselves. See you in the next video."
    x = substring_start_end_in_transcription(audio_transcription, substring)
