from moviepy.editor import VideoFileClip
import os


def extract_audio_video(video_file, audio_file=None):
    if audio_file is None:
        # If audio file name is not specified, generate it from the video file name
        base_name = os.path.splitext(video_file)[0]  # get the base name of the video file (without extension)
        audio_file = base_name + '.mp3'  # append .mp3 extension

    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)

    return audio_file
