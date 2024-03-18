import json
import os
import datetime


def format_time(timedelta):
    """
    Converts a datetime.timedelta object into SRT time format string ("hh:mm:ss,ms").
    Args:
        timedelta: A datetime.timedelta object.
    Returns:
        A string in SRT time format ("hh:mm:ss,ms").
    """
    total_seconds = int(timedelta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = timedelta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def audio_transcription_to_subtitle(json_file, output_format="srt"):
    # The codes inside this function are almost the same with your original function.
    # I only revised the part where the start_time_str and end_time_str are formatted for SRT subtitles.

    # Get the directory path from the JSON file path
    json_dir = os.path.dirname(json_file)

    with open(json_file, 'r') as f:
        data = json.load(f)

    segments = data["segments"]
    content = ""
    count = 1  # Counter for subtitle line numbers

    for segment in segments:
        # Convert start and end times to strings with formatting
        start_time_str = f"{segment['start']:.3f}"
        end_time_str = f"{segment['end']:.3f}"
        text = segment["text"].replace("\r?\n|\r", "<br>" if output_format == "ass" else "\\n")  # Replace newline based on format

        if output_format == "srt":
            # Format SRT line with line number, timestamps, and text
            start_time_ms = int(segment['start'] * 1000)
            end_time_ms = int(segment['end'] * 1000)

            # Convert milliseconds to timedelta objects
            start_timedelta = datetime.timedelta(milliseconds=start_time_ms)
            end_timedelta = datetime.timedelta(milliseconds=end_time_ms)

            # Format the time using the helper function
            start_time_str = format_time(start_timedelta)
            end_time_str = format_time(end_timedelta)

            content += f"{count}\n{start_time_str} --> {end_time_str}\n{text}\n\n"
            count += 1
        else:
            # Format ASS dialogue line with styling
            content += f'Dialogue: 0,{start_time_str},{end_time_str},{start_time_str},Style=Plain,{text}\n'

    # Generate filename based on the JSON file name (without extension)
    filename, _ = os.path.splitext(os.path.basename(json_file))
    output_filename = f"{filename}.{output_format}"
    output_path = os.path.join(json_dir, output_filename)

    # Write the content to the file
    with open(output_path, "w") as f:
        f.write(content)

    return output_path

# Example usage (generate SRT subtitle)
'''json_path = "../data/audio_transcription.json"
srt_file_path = audio_transcription_to_subtitle(json_path, output_format="ass")
print(f"Generated SRT file saved at: {srt_file_path}")

# Example usage (generate ASS subtitle)
#ass_file_path = audio_transcription_to_subtitle(json_path, output_format="srt")
#print(f"Generated ASS file saved at: {ass_file_path}")'''
