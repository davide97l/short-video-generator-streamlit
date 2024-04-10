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


def download_video_instagram(url, save_path='videos_downloaded'):
    if 'reel' in url.split('/')[-3]:
        url = re.sub(r'/reel/', '/p/', url)
    video_id = extract_media_id(url)
    out_path = os.path.join(save_path, video_id + '.mp4')
    if os.path.exists(out_path):
        print('Video already downloaded')
        return out_path
    L = instaloader.Instaloader(dirname_pattern=save_path, filename_pattern=video_id)
    post = Post.from_shortcode(L.context, video_id)
    L.download_post(post, target=video_id)
    # remove extra files
    for file in os.listdir(save_path):
        if not file.endswith('.mp4'):
            os.remove(os.path.join(save_path, file))
    return out_path


if __name__ == '__main__':
    url = 'https://www.instagram.com/p/CzvLPDsoyGr/'
    save_path = "videos_downloaded"
    download_video_instagram(url, save_path)