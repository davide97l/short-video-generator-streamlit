from moviepy.editor import TextClip, CompositeVideoClip, ImageClip
from functions.text_remove_punctuation import text_remove_punctuation
import os


def image_add_captions(image_path: str, text: str, output_path: str = None,
                       font='Arial', fontsize=24, color='yellow',
                       caption_width=100, position='center', remove_punctuation=False):
    # Load image
    image_clip = ImageClip(image_path).set_duration(0.01)
    image_width, image_height = image_clip.size

    # Define the TextClip
    caption_width_pixels = int(image_width * caption_width / 100)
    size = (caption_width_pixels, None)
    if remove_punctuation:
        text = text_remove_punctuation(text)
    text_clip = TextClip(text, font=font, fontsize=fontsize, color=color, method='caption', align='center', size=size).set_duration(image_clip.duration)

    # Create a composite video clip with image and text layered
    if position == 'third_quarter':
        position = (0, image_height * 3 / 4)
    elif position == 'first_quarter':
        position = (0, image_height * 1 / 4)
    final_clip = CompositeVideoClip([image_clip, text_clip.set_pos(position)])

    # Set output path if not provided
    if not output_path:
        output_path = os.path.join(os.path.dirname(image_path), f"{os.path.basename(image_path)[:-4]}_subtitled.png")

    # Write the image
    final_clip.save_frame(output_path, t=0)

    return output_path


if __name__ == '__main__':
    font = '../fonts/LEMONMILK-Regular.otf'
    subtitle_path = "../data/audio_transcription.srt"
    video_path = "../data/youtube_videoooo.jpg"

    x = image_add_captions(video_path, 'hello world', font=font, remove_punctuation=False, color='#ffffff', position='third_quarter')
    print(x)