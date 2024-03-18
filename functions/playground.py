from download_video_youtube import download_video_youtube
from split_video_intervals import split_video_intervals
from crop_video import crop_video
from extract_audio_video import extract_audio_video
from audio_transcription import audio_transcription
from audio_transcription_to_text import audio_transcription_to_text
from text_to_paragraph import text_to_paragraphs
from audio_transcription_to_words import audio_transcription_to_words
from substring_start_end_in_transcription import substring_start_end_in_transcription

youtube_url = "https://www.youtube.com/watch?v=z97_vajw-Do"
path = '../data'
video_path = '../data/youtube_video.mp4'
short_video_path = '../data/youtube_video_1.mp4'
cropped_short_video_path = '../data/cropped_youtube_video_1.mp4'
split_video_timestamps = [15, 20]
audio_speech_path = '../data/youtube_video_1.mp3'
audio_transcription_sentences = "../data/audio_transcription.json"
audio_transcription_words = "../data/audio_transcription_words.json"
substring = "so child came"



#download_video_youtube(youtube_url, resolution=None, path=path, filename='youtube_video')
#split_video_intervals(video_path, split_video_timestamps, output_folder=path, keep_excluded_intervals=False)
#crop_video(short_video_path, cropped_short_video_path, new_width=400, new_height=800, alignment='center')
extract_audio_video(video_file=short_video_path)
audio_transcription(audio_speech_path, audio_transcription_sentences, word_level=True)
#text = audio_transcription_to_text(audio_transcription_sentences)
#print(text)
#paragraphs = text_to_paragraphs(text)
#print(paragraphs)
#audio_transcription_to_words(audio_transcription_sentences, audio_transcription_words)
start_time, end_time = substring_start_end_in_transcription(audio_transcription_sentences, substring)
print(start_time, end_time)
