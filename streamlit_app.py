import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import time

# Function to download video
def download_video(url, folder):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        video_url = soup.find("meta", property="og:video")["content"]
        with open(os.path.join(folder, 'video.mp4'), 'wb') as f:
            f.write(requests.get(video_url).content)
        return True
    except Exception as e:
        return False, str(e)

# Function to display video
def display_video(url):
    st.video(url)

# Function to list downloaded videos
def list_downloaded_videos(folder):
    return os.listdir(folder)

# Main function
def main():
    st.title("Instagram Video Downloader")

    # Sidebar
    st.sidebar.header("Downloaded Videos")
    downloaded_videos = list_downloaded_videos('videos_downloaded')
    selected_video = st.sidebar.selectbox("Select Video", downloaded_videos)

    if st.sidebar.button("Download Selected Video"):
        # Download selected video
        st.sidebar.write(f"Downloading {selected_video}...")
        time.sleep(2)  # Simulating download time
        st.sidebar.write(f"Downloaded {selected_video}")

    if st.sidebar.button("Cancel Download"):
        st.sidebar.write("Download canceled.")

    # Main page
    url = st.text_input("Enter Instagram Video URL:")
    if st.button("Download"):
        if url:
            if download_video(url, 'videos_downloaded'):
                st.success("Video downloaded successfully!")
            else:
                st.error("Failed to download video. Please check the URL.")
        else:
            st.warning("Please enter a valid Instagram video URL.")

        st.write("Downloaded Videos:")
        downloaded_videos = list_downloaded_videos('videos_downloaded')
        for video in downloaded_videos:
            st.write(f"- {video}")
            display_video(os.path.join('videos_downloaded', video))

if __name__ == "__main__":
    main()
