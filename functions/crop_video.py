from moviepy.editor import VideoFileClip
import os


def crop_video(input_video_path, top, bottom, width, height, output_video_path=None, alignment=None):
    # Load video
    clip = VideoFileClip(input_video_path)

    # Get the dimensions of the original video
    width, height = clip.size

    # Check if the new dimensions are valid, if not cap to max
    new_width = min(new_width, width)
    new_height = min(new_height, height)

    # Calculate the cropping boundaries based on the alignment
    if alignment == 'left':
        left = 0
    elif alignment == 'right':
        left = width - new_width
    else:  # center
        left = (width - new_width) / 2

    top = (height - new_height) / 2
    right = left + new_width
    bottom = top + new_height

    # Crop the video and retain the audio from the original clip
    cropped_clip = clip.crop(x1=int(left), y1=int(top), x2=int(right), y2=int(bottom)).set_audio(clip.audio)

    # If output_video_path is None, use the same path of input_video_path
    if output_video_path is None:
        base_name = os.path.basename(input_video_path)
        name, ext = os.path.splitext(base_name)
        output_video_path = os.path.join(
            os.path.dirname(input_video_path),
            "{name}_cropped_{new_width}_{new_height}{ext}".format(
                name=name,
                new_width=new_width,
                new_height=new_height,
                ext=ext
            )
        )

    # Write the output file
    cropped_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

    # Return the full filename of the new video
    return output_video_path
