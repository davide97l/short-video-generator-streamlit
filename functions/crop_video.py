from moviepy.editor import VideoFileClip
import os


def crop_video(input_video_path, x, y, width, height, output_video_path=None):
    # Load video
    clip = VideoFileClip(input_video_path)

    # Get the dimensions of the original video
    max_width, max_height = clip.size

    # Calculate the cropping boundaries
    left = min(max_width, x)
    top = min(max_height, y)
    right = min(max_width, left + width)
    bottom = min(max_height, top + height)

    # Crop the video and retain the audio from the original clip
    cropped_clip = clip.crop(x1=int(left), y1=int(top), x2=int(right), y2=int(bottom)).set_audio(clip.audio)

    # If output_video_path is None, use the same path of input_video_path
    if output_video_path is None:
        base_name = os.path.basename(input_video_path)
        name, ext = os.path.splitext(base_name)
        output_video_path = os.path.join(
            os.path.dirname(input_video_path),
            f"{name}_crop_{x}_{y}_{width}_{height}{ext}"
        )

    # Write the output file
    cropped_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

    # Return the full filename of the new video
    return output_video_path
