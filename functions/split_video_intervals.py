import moviepy.editor as mp
import os


def split_video_intervals(video_path, timestamps, output_folder=None, assumed_audio_codec="aac",
                          keep_excluded_intervals=False):
    """Splits an MP4 video into sub-videos based on timestamps, attempting to preserve quality.

    Args:
        video_path (str): Path to the MP4 video file.
        timestamps (list): List of timestamps (in seconds) where to split the video.
        output_folder (str): Path to the folder where sub-videos will be saved.
        assumed_audio_codec (str, optional): Assumed audio codec for sub-videos.
            Defaults to "aac" (common choice for MP4).
        keep_excluded_intervals (bool, optional): If False, keep also the intervals corresponding to the start and end of
            the video.

    Raises:
        AttributeError: If `moviepy` cannot access the audio codec.
    """

    # Determine output path if not provided
    if not output_folder:
        # Extract filename without extension
        output_folder = os.path.dirname(video_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load the video clip
    clip = mp.VideoFileClip(video_path)

    # Sort timestamps in ascending order
    timestamps.sort()

    if keep_excluded_intervals:
        if timestamps[-1] < clip.duration:
            timestamps.append(clip.duration)
        start_time = 0
    else:
        assert len(timestamps) > 1
        start_time = timestamps[0]
        timestamps = timestamps[1:]

    i = 1
    outputs = []
    for end_time in timestamps:
        subclip = clip.subclip(start_time, end_time)
        output_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_{i}.mp4"
        output_path = os.path.join(output_folder, output_filename)

        try:
            # Attempt to use assumed codec
            subclip.write_videofile(output_path, fps=clip.fps, audio_codec=assumed_audio_codec, audio_fps=clip.audio.fps)
            outputs.append(output_path)
        except AttributeError as e:
            # If codec access fails, notify and suggest alternatives
            print(f"Error accessing audio codec: {e}")
            print("Consider using FFmpeg or other libraries for more control over audio codecs.")
            raise

        start_time = end_time
        i += 1

    # Release the clip resources
    clip.close()

    return outputs
