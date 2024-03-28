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
from functions.text_to_paragraph import text_to_paragraph
from functions.streamlit_utils import text_add_color, has_paired_file, box_algorithm
from PIL import Image
from random import randint
from streamlit_components.srt_editor import srt_editor


def display_video(url):
    """Displays a video from a given URL."""
    st.video(url)


st.title("Short Video Generator")
st.session_state.video_url = st.text_input("Enter Video URL")

# -----DOWNLOAD VIDEO------------------------------------------------------------------------
#if 'video_url' in st.session_state and st.session_state.video_url is not None:
    #with st.spinner('Downloading video...'):
        #st.session_state.video_path = download_video_youtube(st.session_state.video_url, path='data2')
st.session_state.video_path = "data2/These_5_Books_Scaled_My_Business_to_Multiple_6_Figures.mp4"  #TODO keep for test

# -----TRANSCRIPT VIDEO------------------------------------------------------------------------
if 'video_path' in st.session_state and st.session_state.video_path is not None:
    display_video(st.session_state.video_path)
    st.session_state.max_video_duration = video_duration(st.session_state.video_path)

    if 'audio_path' not in st.session_state:
        if not has_paired_file(st.session_state.video_path, 'mp3'):
            st.session_state.audio_path = extract_audio_video(st.session_state.video_path)

    if 'transcription_path' not in st.session_state and 'audio_path' in st.session_state:
        #with st.spinner('Processing video transcription...'):
        #    st.session_state.transcription_path = audio_transcription(st.session_state.audio_path)
        st.session_state.transcription_path = 'data2/These_5_Books_Scaled_My_Business_to_Multiple_6_Figures.json'
        #sentence_dict = audio_transcription_to_sentence_dict(st.session_state.transcription_path)
        #strings = []
        #for i, sentence in enumerate(sentence_dict, start=1):
        #    sentence_string = f"{i}) S:{int(sentence['start'])}s | E:{int(sentence['end'])}s | D:{int(sentence['duration'])}s | {sentence['text']}"
        #    strings.append(sentence_string)
        #sentence_info = '\n'.join(strings)

    if 'video_text' not in st.session_state and 'transcription_path' in st.session_state:
        st.session_state.video_text = audio_transcription_to_text(st.session_state.transcription_path)
        st.session_state.video_text_original = st.session_state.video_text

if 'video_text' in st.session_state:
    with st.container(height=300):
        text_slot = st.empty()
        text_slot.markdown(st.session_state.video_text)

    # -----HIGHLIGHT PARAGRAPHS------------------------------------------------------------------------
    if st.button("Smart text suggestions"):
        st.session_state.video_text = st.session_state.video_text_original
        threshold = 7
        colors = ['blue', 'violet']
        with st.spinner('Selecting interesting parts...'):
            paragraphs = text_to_paragraph(st.session_state.video_text)
        highlights = 0
        for entry in paragraphs:
            if threshold and entry["score"] < threshold:
                continue
            if entry["paragraph"] in st.session_state.video_text:
                st.session_state.video_text = text_add_color(st.session_state.video_text, entry["paragraph"],
                                                             color=colors[highlights % 2])
                highlights += 1
        if highlights > 0:
            st.success(f"Individuated {highlights} suggestions!")
        else:
            st.warning(f"No available suggestions!")
        text_slot.markdown(st.session_state.video_text)

    # -----TRIM VIDEO LENGTH------------------------------------------------------------------------
    st.header("Trim video length")
    extracted_text = st.text_input("Paste extracted text here")

    if "start" not in st.session_state:
        st.session_state.start = 0.
    if "end" not in st.session_state:
        st.session_state.end = st.session_state.max_video_duration
    if "sub_video" not in st.session_state:
        st.session_state.sub_video = st.session_state.video_path

    if st.button("Extract short video from transcription text"):
        if not extracted_text:
            st.warning("No extracted text provided!")
        else:
            st.session_state.start, st.session_state.end = substring_start_end_in_transcription(st.session_state.transcription_path, extracted_text)
            with st.spinner('Trimming video...'):
                st.session_state.sub_video = split_video_intervals(st.session_state.video_path, [st.session_state.start, st.session_state.end],
                                                                   keep_excluded_intervals=False)[0]
            st.success("Video Trimmed Successfully!")

    st.session_state.start = st.slider("Start Time (seconds)", min_value=0., max_value=st.session_state.max_video_duration, format="%f", value=st.session_state.start, step=0.1)
    st.session_state.end = st.slider("End Time (seconds)", min_value=0., max_value=st.session_state.max_video_duration, format="%f", value=st.session_state.end, step=0.1)
    if st.button("Extract short video from start and end time"):
        if st.session_state.start >= st.session_state.end:
            st.warning("Start must have a lower value than end!")
        else:
            with st.spinner('Trimming video...'):
                st.session_state.sub_video = split_video_intervals(st.session_state.video_path, [st.session_state.start, st.session_state.end],
                                                                   keep_excluded_intervals=False)[0]
            st.success("Video Trimmed Successfully!")

    if 'sub_video' in st.session_state:
        video_slot = st.empty()
        video_slot.video(st.session_state.sub_video)

# -----CROP VIDEO SIZE------------------------------------------------------------------------
if 'sub_video' in st.session_state and st.session_state.sub_video is not None:
    st.header("Crop video size")
    st.session_state.img_file = video_thumbnail(st.session_state.sub_video)

    # Cropper options section
    st.subheader("Cropper Options")
    realtime_update = True
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
        # Get a cropped image from the frontend
        cropped_img, box = st_cropper(img, realtime_update=realtime_update, box_color='#0000FF',
                                      aspect_ratio=aspect_ratio, return_type='both', box_algorithm=box_algorithm)

        # Manipulate cropped image at will
        _ = cropped_img.thumbnail((150, 150))
        st.image(cropped_img)

        if 'crop_video_path' not in st.session_state:
            st.session_state.crop_video_path = None
        if st.button("Crop video"):
            with st.spinner('Cropping video...'):
                crop_video_path = crop_video(st.session_state.sub_video, box['left'], box['top'], box['width'], box['height'])
            st.session_state.crop_video_path = crop_video_path

    if 'crop_video_path' in st.session_state and st.session_state.crop_video_path is not None:
        cols = st.columns((1, 2, 1))
        cols[1].video(st.session_state.crop_video_path)

# -----VIDEO CAPTIONS------------------------------------------------------------------------
if 'crop_video_path' in st.session_state and 'transcription_path' in st.session_state and\
        st.session_state.crop_video_path is not None:
    st.header("Video captions")
    subtitles = audio_transcription_to_subtitle(st.session_state.transcription_path, output_format="srt")
    if 'video_captions_path' not in st.session_state:
        st.session_state.video_captions_path = None
    # Add a color picker for font color
    font_color = st.color_picker("Choose font color", '#ffff00')  # Initial color is yellow
    # Add a slider for font size
    font_size = st.slider("Font size", min_value=0, max_value=120, value=24, step=12)
    # Caption position mapping with renaming dictionary
    caption_options = {"center": "Center", "top": "Top", "first_quarter": "First quarter",
                       "third_quarter": "Third quarter", "bottom": "Bottom"}
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

    with st.expander('Expand edit captions', expanded=False):
        srt_editor(subtitles, output_file=subtitles, time_range=(st.session_state.start, st.session_state.end))

    if st.button("Make captions"):
        with st.spinner('Adding captions...'):
            video_captions_path = video_add_captions(
                subtitles, st.session_state.crop_video_path,
                color=font_color, fontsize=font_size, remove_punctuation=remove_punctuation, font=font_path,
                position=caption_position_key)
        st.session_state.video_captions_path = video_captions_path

if 'video_captions_path' in st.session_state and st.session_state.video_captions_path is not None:
    cols2 = st.columns((1, 2, 1))
    cols2[1].video(st.session_state.video_captions_path)
    with open(st.session_state.video_captions_path, 'rb') as file:
        btn = st.download_button(
            "Download Video",
            file,
            file_name=st.session_state.video_captions_path,
            mime="video/mp4",
        )
