import instaloader
from instaloader import Post
import os
import re


def extract_media_id(url):
    # Define the regex pattern to match the media ID
    pattern = r"https://www.instagram.com/p/([A-Za-z0-9_-]+)/?"

    # Search for the media ID in the URL using the pattern
    match = re.search(pattern, url)

    # If a match is found, return the media ID, otherwise return None
    if match:
        return match.group(1)
    else:
        return None


def download_instagram_video(url, save_path='videos_downloaded'):
    try:
        video_id = extract_media_id(url)
        L = instaloader.Instaloader(dirname_pattern=save_path, filename_pattern=video_id)
        post = Post.from_shortcode(L.context, video_id)
        L.download_post(post, target=video_id)
    except Exception as e:
        print(f"Error downloading video: {e}")


if __name__ == '__main__':
    url = "https://www.instagram.com/p/C5dEJKNLa_L/"
    save_path = "videos_downloaded"
    download_instagram_video(url, save_path)