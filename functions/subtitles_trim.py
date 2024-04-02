import pysrt
import os


def seconds_to_subrip_time(seconds):
    # Convert seconds to hours, minutes, seconds, milliseconds format
    millis = seconds * 1000
    hours = millis // 3600000
    millis %= 3600000
    mins = millis // 60000
    millis %= 60000
    secs = millis // 1000
    millis %= 1000

    return pysrt.SubRipTime(hours, mins, secs, millis)


def subtitles_trim(file_path, start_time, end_time, new_file_path=None, reset_time=True):
    # Load the subtitles
    subs = pysrt.open(file_path)

    # Convert start_time and end_time into pysrt compatible format
    start_time_srt = seconds_to_subrip_time(start_time)
    end_time_srt = seconds_to_subrip_time(end_time)

    # Trim the subtitles
    trimmed_subs = [s for s in subs if start_time_srt < s.end <= end_time_srt]

    if reset_time:
        # Update the start and end times of each subtitle
        for s in trimmed_subs:
            s.start -= start_time_srt
            s.end -= start_time_srt

    # Save the trimmed subtitles to a new file or modified original file
    trimmed_file = pysrt.SubRipFile(items=trimmed_subs)
    if new_file_path is None:
        base, ext = os.path.splitext(file_path)
        new_file_path = f'{base}_trimmed{ext}'
    trimmed_file.save(new_file_path)

    return new_file_path


if __name__ == '__main__':
    subtitles_path = '../data2/These_5_Books_Scaled_My_Business_to_Multiple_6_Figures.srt'
    substring = "You just need to know how people think. And that's literally it besties the six books that help me go from zero to 100,000 dollar months in on the two years. It may be a secret weapon for me, but as I reminded from me to you, stop reading, just read, start reading to act. In this era of new education, we don't wait to get tested. We test ourselves. See you in the next video."
    x = subtitles_trim(subtitles_path, 5, 15)