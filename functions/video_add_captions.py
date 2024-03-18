from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from functions.text_remove_punctuation import text_remove_punctuation
import os
import pysrt


def video_add_captions(subtitle_path: str, video_path: str, output_path: str = None,
                       font='Arial', fontsize=24, color='yellow',
                       caption_width=100, position='center', remove_punctuation=False):
    # Load SRT file
    subs = pysrt.open(subtitle_path)
    video_clip = VideoFileClip(video_path)
    video_width, _ = video_clip.size

    # Convert SubRipItems to the format that SubtitlesClip expects
    subtitles = [((s.start.ordinal / 1000, s.end.ordinal / 1000), s.text) for s in subs]

    # Define the corrected function to create TextClips for each subtitle
    def txtclip(txt, font, fontsize, color, caption_width=100):
        if remove_punctuation:
            txt = text_remove_punctuation(txt)
        caption_width_pixels = int(video_width * caption_width / 100)
        size = (caption_width_pixels, None)
        text_clip = TextClip(txt, font=font, fontsize=fontsize, color=color, method='caption', align='center', size=size)
        return text_clip

    generator = lambda txt: txtclip(txt, font, fontsize, color, caption_width)
    subtitles = SubtitlesClip(subtitles, make_textclip=generator).set_pos(position)

    # Create a composite video clip with video and subtitles layered
    final_clip = CompositeVideoClip([video_clip, subtitles.set_duration(video_clip.duration)])

    # Set output path if not provided
    if not output_path:
        output_path = os.path.join(os.path.dirname(video_path), f"{os.path.basename(video_path)[:-4]}_subtitled1.mp4")

    # Write the merged video
    final_clip.write_videofile(output_path)
    #print(f"Video with subtitles saved at: {output_path}")

    return output_path


font = '../fonts/LEMONMILK-Regular.otf'
subtitle_path = "../data/audio_transcription.srt"
video_path = "../data/youtube_video_1.mp4"

video_add_captions(subtitle_path, video_path, font=font, remove_punctuation=False)