import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import time
from functions.download_video_instagram import download_video_instagram
import sys
import argparse


video_path = 'videos_downloaded'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Instagram reels from URLs provided in a text file.')
    parser.add_argument('--urls_file', type=str, help='Path to the text file containing Instagram reel URLs', default='videos_to_download.txt', required=False)
    parser.add_argument('--save_dir', type=str, default='videos_downloaded', help='Directory to save downloaded reels (default: videos_downloaded)', required=False)
    args = parser.parse_args()

    urls_file = args.urls_file
    save_dir = args.save_dir

    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Read URLs from the text file
    with open(urls_file, 'r') as file:
        urls = file.readlines()

    # Download each reel
    for index, url in enumerate(urls, start=1):
        print('downloading video...', url)
        video = download_video_instagram(url, save_dir)
        print('downloaded video at', video)
