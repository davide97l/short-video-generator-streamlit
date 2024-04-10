import streamlit as st
import os
from functions.download_video_instagram import download_video_instagram


# Function to display video
def display_video(url):
    st.video(url)


# Function to list downloaded videos
def list_downloaded_videos(folder):
    return os.listdir(folder)


video_path = 'videos_downloaded'


# Main function
def main():
    st.title("Instagram Video Downloader")

    # Sidebar
    st.sidebar.header("Downloaded Videos")
    downloaded_videos = list_downloaded_videos(video_path)
    mp4_downloaded_videos = [video for video in downloaded_videos if video.endswith('.mp4')]
    selected_video = st.sidebar.selectbox("Select Video", mp4_downloaded_videos)

    if st.sidebar.button("Select Video"):
        st.session_state.last_video_path = os.path.join(video_path, selected_video)

    # Main page
    url = st.text_input("Enter Instagram Video URL:")
    if st.button("Download"):
        if url:
            try:
                st.session_state.last_video_path = download_video_instagram(url, video_path)
                st.success("Video downloaded successfully!")
                downloaded_videos = list_downloaded_videos(video_path)
                mp4_downloaded_videos = [video for video in downloaded_videos if video.endswith('.mp4')]
            except:
                st.error("Failed to download video. Please check the URL.")
        else:
            st.warning("Please enter a valid Instagram video URL.")

    if 'last_video_path' in st.session_state:
        display_video(st.session_state.last_video_path)


if __name__ == "__main__":
    main()
