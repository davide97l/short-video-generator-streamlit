import os
import streamlit as st
import streamlit_scrollable_textbox as stx
from functions.download_video_youtube import download_video_youtube
from functions.extract_audio_video import extract_audio_video
from functions.audio_transcription import audio_transcription
from functions.audio_transcription_to_text import audio_transcription_to_text
from functions.audio_transcription_to_sentence_dict import audio_transcription_to_sentence_dict
from functions.substring_start_end_in_transcription import substring_start_end_in_transcription
from functions.split_video_intervals import split_video_intervals
from functions.crop_video import crop_video
from functions.video_duration import video_duration
from functions.video_thumbnail import video_thumbnail
from functions.video_add_captions import video_add_captions
from functions.audio_transcription_to_subtitle import audio_transcription_to_subtitle
from functions.image_add_captions import image_add_captions
from streamlit_cropper import st_cropper
from PIL import Image
from random import randint


def display_video(url):
    """Displays a video from a given URL."""
    st.video(url)


st.title("Video Player")
video_url = st.text_input("Enter Video URL")
#video_path = download_video_youtube(video_url)
#TODO remove
video_path = "data2/youtube_video.mp4"

if video_path:
    max_video_duration = video_duration(video_path)
    # Display video with some space above it
    display_video(video_path)

#audio_path = extract_audio_video(video_path)
audio_path = 'data2/youtube_video.mp3'
print(audio_path)
transcription_path = 'data2/youtube_video.json'
#transcription_path = audio_transcription(audio_path)
print(transcription_path)
video_text = audio_transcription_to_text(transcription_path)
sentence_dict = audio_transcription_to_sentence_dict(transcription_path)

strings = []
for i, sentence in enumerate(sentence_dict, start=1):
    sentence_string = f"{i}) S:{int(sentence['start'])}s | E:{int(sentence['end'])}s | D:{int(sentence['duration'])}s | {sentence['text']}"
    strings.append(sentence_string)
sentence_info = '\n'.join(strings)

video_text = ':blue[This text is blue.]' + video_text

with st.container(height=300):
    st.markdown(video_text)

with st.expander('Expand to see sentence level timestamps', expanded=False):
    st.markdown(sentence_info)

extracted_text = st.text_input("Paste extracted text here")

#TODO remove
#extracted_text = "Embrace them, tackle them, and watch yourself level up in the game of life. You've got the skills, determination, and spirit to conquer anything that comes your way. Hope you gain some value from this story, and try to implement it in your life, and always keep rising."

if "start" not in st.session_state:
    st.session_state.start = 0.
if "end" not in st.session_state:
    st.session_state.end = max_video_duration
if "sub_video" not in st.session_state:
    st.session_state.sub_video = video_path


if st.button("Extract short video from transcription text"):
    if not extracted_text:
        st.warning("No extracted text provided!")
    else:
        st.session_state.start, st.session_state.end = substring_start_end_in_transcription(transcription_path, extracted_text)
        st.session_state.sub_video = split_video_intervals(video_path, [st.session_state.start, st.session_state.end],
                                                           keep_excluded_intervals=False)[0]
        st.success("Video Trimmed Successfully!")

st.session_state.start = st.slider("Start Time (seconds)", min_value=0., max_value=max_video_duration, format="%f", value=st.session_state.start, step=0.1)
st.session_state.end = st.slider("End Time (seconds)", min_value=0., max_value=max_video_duration, format="%f", value=st.session_state.end, step=0.1)
if st.button("Extract short video from start and end time"):
    if st.session_state.start >= st.session_state.end:
        st.warning("Start must have a lower value than end!")
    else:
        st.session_state.sub_video = split_video_intervals(video_path, [st.session_state.start, st.session_state.end],
                                                           keep_excluded_intervals=False)[0]
        st.success("Video Trimmed Successfully!")

if st.session_state.sub_video:
    video_slot = st.empty()  # Placeholder for the video
    video_slot.video(st.session_state.sub_video)

st.session_state.sub_video = video_path # TODO remove

if st.session_state.sub_video:
    st.header("Cropper Demo")
    st.session_state.img_file = video_thumbnail(st.session_state.sub_video)

    # Cropper options section
    st.subheader("Cropper Options")
    realtime_update = st.checkbox(label="Update in Real Time", value=True)
    box_color = st.color_picker(label="Box Color", value='#0000FF')
    aspect_choice = st.radio(label="Aspect Ratio", options=["9:16", "16:9", "4:3", "3:4", "Free", "1:1"])
    aspect_dict = {
        "9:16": (9, 16),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "3:4": (3, 4),
        "1:1": (1, 1),
        "Free": None
    }
    aspect_ratio = aspect_dict[aspect_choice]

    if st.session_state.img_file:
        img = Image.open(st.session_state.img_file)
        if not realtime_update:
            st.write("Double click to save crop")
        # Get a cropped image from the frontend
        cropped_img, box = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                      aspect_ratio=aspect_ratio, return_type='both')

        # Manipulate cropped image at will
        st.subheader(f"Preview ({box})")
        _ = cropped_img.thumbnail((150,150))
        st.image(cropped_img)

        st.session_state.crop_video_path = None
        if st.button("Crop video"):
            crop_video_path = crop_video(st.session_state.sub_video, box['left'], box['top'], box['width'], box['height'])
            st.session_state.crop_video_path = crop_video_path


st.session_state.crop_video_path = 'data2/youtube_video_cropped.mp4'
if st.session_state.crop_video_path:
    cols = st.columns((1, 2, 1))
    cols[1].video(st.session_state.crop_video_path)

if st.session_state.crop_video_path:
    st.session_state.video_captions_path = None
    # Add a color picker for font color
    font_color = st.color_picker("Choose font color", '#ffff00')  # Initial color is yellow
    # Add a slider for font size
    font_size = st.slider("Font size", min_value=0, max_value=120, value=24, step=12)
    # Caption position mapping with renaming dictionary
    caption_options = {"center": "Center", "top": "Top", "bottom": "Bottom"}
    caption_position = st.radio("Caption Position", list(caption_options.values()))
    # Display caption position selection (optional)
    caption_position_key = list(caption_options.keys())[list(caption_options.values()).index(caption_position)]
    # Add checkbox for remove punctuation
    remove_punctuation = st.checkbox("Remove punctuation", value=False)  # Default checked

    # Get available fonts from the "font" folder
    font_folder = "fonts"  # Replace with your actual folder path
    font_files = [f for f in os.listdir(font_folder) if f.endswith((".ttf", ".otf"))]
    # Extract font names without extensions
    available_fonts = [os.path.splitext(f)[0] for f in font_files]  # Get filename without extension

    # Display a dropdown to select font (show only name)
    if available_fonts:
        selected_font = st.selectbox("Font type", available_fonts)
        font_path = os.path.join(font_folder, font_files[available_fonts.index(selected_font)])
    else:
        st.warning("No font files found in the 'font' folder.")
        selected_font = None
        font_path = None  # Set to None if no fonts found

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    upload_font = st.file_uploader("Choose a font file (TTF, OTF)", type=["ttf", "otf"],
                                   key=st.session_state["file_uploader_key"])
    if upload_font is not None:
        font_bytes = upload_font.read()
        font_name = upload_font.name  # Use full name including extension for saving
        if not os.path.exists(font_folder):
            os.makedirs(font_folder)
        save_path = os.path.join(font_folder, font_name)
        try:
            with open(save_path, "wb") as f:
                f.write(font_bytes)
            st.success(f"Font '{font_name}' uploaded and saved successfully!")
            st.session_state["file_uploader_key"] += 1
            st.rerun()
        except Exception as e:
            st.error(f"Error saving font: {e}")

    # Preview font display (if font path available)
    if selected_font:
        st.session_state.cropped_thumbnail = video_thumbnail(st.session_state.crop_video_path)
        preview_text = st.text_input("Edit preview text", "This is a preview of the selected font.")
        captions_thumbnail_path = image_add_captions(
            image_path=st.session_state.cropped_thumbnail, text=preview_text,
            color=font_color, fontsize=font_size, remove_punctuation=remove_punctuation, font=font_path,
            position=caption_position_key)
        cols3 = st.columns((1, 2, 1))
        cols3[1].image(captions_thumbnail_path)
        #st.write(f'<span style="font-family: {font_path}; font-size: {font_size}px; color: {font_color}">{preview_text}</span>', unsafe_allow_html=True)

    if st.button("Make captions"):
        subtitles = audio_transcription_to_subtitle(transcription_path, output_format="srt")
        video_captions_path = video_add_captions(
            subtitles, st.session_state.crop_video_path,
            color=font_color, fontsize=font_size, remove_punctuation=remove_punctuation, font=font_path,
            position=caption_position_key)
        st.session_state.video_captions_path = video_captions_path

st.session_state.video_captions_path = 'data2/youtube_video_cropped_subtitled1.mp4'
if st.session_state.video_captions_path:
    cols2 = st.columns((1, 2, 1))
    cols2[1].video(st.session_state.video_captions_path)
    with open(st.session_state.video_captions_path, 'rb') as file:
        btn = st.download_button(
            "Download Video",
            file,
            file_name=st.session_state.video_captions_path,
            mime="video/mp4",
        )
