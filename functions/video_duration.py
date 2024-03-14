import subprocess


def video_duration(video_path):
    """Gets the video duration in seconds using ffprobe"""
    # Construct the ffprobe command to get video duration
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_path}"

    # Execute the command and capture output
    output = subprocess.check_output(cmd, shell=True).decode()

    # Convert the output (string) to a float representing duration in seconds
    try:
        duration = float(output)
    except ValueError:
        print("Error parsing ffprobe output!")
        return None

    return duration
