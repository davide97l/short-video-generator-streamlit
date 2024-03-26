from pytube import YouTube
import os


def download_video_youtube(url, resolution=None, path='.'):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the stream with the highest resolution if no resolution is specified
        if resolution is None:
            stream = yt.streams.get_highest_resolution()
        else:
            # Get the stream with the specified resolution
            stream = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution).first()

        # Check if a stream with the specified resolution was found
        if stream is None:
            print(f"No stream found with resolution {resolution}")
            return

        # Download the video
        download_filename = stream.download(output_path=path)
        base, ext = os.path.splitext(download_filename)
        filename = download_filename
        new_filename = os.path.join(path, f"{filename.replace(' ', '_')}{ext}")
        os.rename(download_filename, new_filename)
        print(f"Video downloaded and renamed to {filename}")
        return new_filename

    except Exception as e:
        print(f"An error occurred: {e}")

