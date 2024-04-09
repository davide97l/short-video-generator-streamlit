import os
import streamlit as st
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
from functions.subtitles_trim import subtitles_trim
from functions.streamlit_utils import text_add_color, box_algorithm
from functions.longest_common_substring import longest_common_substring
from functions.subtitles_modify_row import subtitles_modify_row
from PIL import Image
from streamlit_components.srt_editor import srt_editor


# ----OPTIONS-------------

cache_max_entries = 10
cache_ttl = None
cache_show_spinner = False
data_folder = 'data'
font_folder = "fonts"
st.set_page_config(page_title="Short Video Generator", initial_sidebar_state="collapsed")

# ---SIDE BAR

if st.sidebar.button("Clear Cache"):
    st.runtime.legacy_caching.clear_cache()
    try:
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            os.remove(file_path)
        st.success("Cache cleared successfully.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    st.rerun()

openai_key = st.sidebar.text_input("Enter your OpenAI API key")
if openai_key != "":
    os.environ['OPENAI_API_KEY'] = openai_key
    st.sidebar.success("OpenAI API key set!")

# -----DOWNLOAD VIDEO------------------------------------------------------------------------

st.title("Short Video Generator")
st.header("Download Video")
st.session_state.video_url = st.text_input(
    "Paste your Youtube video URL here:", placeholder="https://...",
)


@st.cache_data(max_entries=cache_max_entries, ttl=cache_ttl, show_spinner=cache_show_spinner)
def cached_download_video(video_url, save_path):
    return download_video_youtube(video_url, path=save_path)

#st.session_state.video_url='https://www.youtube.com/watch?v=kNMlvVCc6es' # keep for testing

if 'video_url' in st.session_state and st.session_state.video_url is not None:
    with st.spinner('Downloading video (this may take a while according to the size of video)...'):
        st.session_state.video_path = cached_download_video(st.session_state.video_url, data_folder)

# -----TRANSCRIPT VIDEO------------------------------------------------------------------------

if 'video_path' in st.session_state and st.session_state.video_path is not None:
    st.video(st.session_state.video_path)
    st.session_state.max_video_duration = video_duration(st.session_state.video_path)

    if 'audio_path' not in st.session_state:
        @st.cache_data(max_entries=cache_max_entries, ttl=cache_ttl, show_spinner=cache_show_spinner)
        def cached_extract_audio_video(video_path):
            return extract_audio_video(video_path)
        with st.spinner('Extracting audio...'):
            st.session_state.audio_path = cached_extract_audio_video(st.session_state.video_path)

    if 'transcription_path' not in st.session_state and 'audio_path' in st.session_state:
        @st.cache_data(max_entries=cache_max_entries, ttl=cache_ttl, show_spinner=cache_show_spinner)
        def cached_audio_transcription(audio_path):
            return audio_transcription(audio_path)
        with st.spinner('Processing video transcription...'):
            st.session_state.transcription_path = cached_audio_transcription(st.session_state.audio_path)

        sentence_dict = audio_transcription_to_sentence_dict(st.session_state.transcription_path)
        strings = []
        for i, sentence in enumerate(sentence_dict, start=1):
            sentence_string = f"{i}) S:{int(sentence['start'])}s | E:{int(sentence['end'])}s | D:{int(sentence['duration'])}s | {sentence['text']}"
            strings.append(sentence_string)
        st.session_state.sentence_info = '\n'.join(strings)

    if 'video_text' not in st.session_state and 'transcription_path' in st.session_state:
        st.session_state.video_text = audio_transcription_to_text(st.session_state.transcription_path)
        st.session_state.video_text_original = st.session_state.video_text

if 'video_text' in st.session_state:
    st.subheader("Video Transcription")
    with st.container(height=300):
        text_slot = st.empty()
        text_slot.markdown(st.session_state.video_text)
    with st.expander('Expand to see sentence level timestamps', expanded=False):
        st.markdown(st.session_state.sentence_info)

# -----HIGHLIGHT PARAGRAPHS------------------------------------------------------------------------
    st.subheader("Use AI to suggest relevant parts")
    if st.button("Smart text suggestions"):
        st.session_state.video_text = st.session_state.video_text_original
        threshold = 7
        colors = ['blue', 'violet']
        with st.spinner('Selecting interesting parts...'):
            try:
                paragraphs = text_to_paragraph(st.session_state.video_text)
            except Exception as e:
                st.error(f"Error processing text: {str(e)}")
                paragraphs = []
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

    st.header("Trim video")
    st.subheader("Trim from text")
    st.session_state.extracted_text = st.text_input("Paste extracted text here (no split words)")

    if "start" not in st.session_state:
        st.session_state.start = 0.
    if "end" not in st.session_state:
        st.session_state.end = st.session_state.max_video_duration
    if "sub_video" not in st.session_state:
        st.session_state.sub_video = st.session_state.video_path

    if st.button("Extract short video from transcription text"):
        if 'extracted_text' not in st.session_state or not st.session_state.extracted_text:
            st.warning("No extracted text provided!")
        else:
            temp_start, temp_end = st.session_state.start, st.session_state.end
            try:
                st.session_state.start, st.session_state.end = substring_start_end_in_transcription(st.session_state.transcription_path, st.session_state.extracted_text)
                with st.spinner('Trimming video...'):
                    st.session_state.sub_video = split_video_intervals(st.session_state.video_path, [st.session_state.start, st.session_state.end],
                                                                       keep_excluded_intervals=False)[0]
                    st.success("Video Trimmed Successfully!")
            except Exception as e:
                st.warning(f"Could find selected text from video transcription. Make sure not to split words.")
                st.session_state.start, st.session_state.end = temp_start, temp_end

    st.subheader("Trim from start and end time")
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

# -----CROP VIDEO------------------------------------------------------------------------

if 'sub_video' in st.session_state and st.session_state.sub_video is not None:
    st.header("Crop Video")
    st.session_state.img_file = video_thumbnail(st.session_state.sub_video)

    # Cropper options section
    realtime_update = True
    st.subheader("Cropper Options")
    aspect_choice = st.radio(label="Aspect Ratio", options=["9:16", "16:9", "4:3", "3:4", "Free", "1:1"], horizontal=True)
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
        st.subheader("Crop Area")
        img = Image.open(st.session_state.img_file)
        # Get a cropped image from the frontend
        cropped_img, box = st_cropper(img, realtime_update=realtime_update, box_color='#0000FF',
                                      aspect_ratio=aspect_ratio, return_type='both', box_algorithm=box_algorithm)
        # Manipulate cropped image at will
        #_ = cropped_img.thumbnail((150, 150))
        #st.image(cropped_img)

    if 'crop_video_path' not in st.session_state:
        st.session_state.crop_video_path = None
    if st.button("Crop video"):
        with st.spinner('Cropping video...'):
            crop_video_path = crop_video(st.session_state.sub_video, box['left'], box['top'], box['width'], box['height'])
        st.success("Video cropped successfully!")
        st.session_state.crop_video_path = crop_video_path

    if 'crop_video_path' in st.session_state and st.session_state.crop_video_path is not None:
        st.subheader("Cropped video")
        cols = st.columns((1, 2, 1))
        cols[1].video(st.session_state.crop_video_path)

# -----VIDEO CAPTIONS------------------------------------------------------------------------
if 'crop_video_path' in st.session_state and 'transcription_path' in st.session_state and\
        st.session_state.crop_video_path is not None:
    st.header("Video captions")
    subtitles = audio_transcription_to_subtitle(st.session_state.transcription_path, output_format="srt")
    if 'trimmed_subtitles' not in st.session_state:
        st.session_state.trimmed_subtitles = subtitles_trim(subtitles, st.session_state.start, st.session_state.end)
        if 'extracted_text' in st.session_state and len(st.session_state.extracted_text) > 1:
            subtitles_first_row = subtitles_modify_row(st.session_state.trimmed_subtitles, 0)[-1]
            subtitles_last_row = subtitles_modify_row(st.session_state.trimmed_subtitles, -1)[-1]
            first_row = longest_common_substring(subtitles_first_row, st.session_state.extracted_text)
            last_row = longest_common_substring(subtitles_last_row, st.session_state.extracted_text)
            st.session_state.trimmed_subtitles = subtitles_modify_row(st.session_state.trimmed_subtitles, 0, first_row)[0]
            st.session_state.trimmed_subtitles = subtitles_modify_row(st.session_state.trimmed_subtitles, -1, last_row)[0]
    if 'video_captions_path' not in st.session_state:
        st.session_state.video_captions_path = None
    cols3 = st.columns((1, 1))
    # Add a color picker for font color
    font_color = cols3[0].color_picker("Choose font color", '#ffff00')  # Initial color is yellow
    # Add a slider for font size
    font_size = cols3[0].slider("Font size", min_value=0, max_value=120, value=24, step=12)
    # Caption position mapping with renaming dictionary
    caption_options = {"center": "Center", "top": "Top", "first_quarter": "First quarter",
                       "third_quarter": "Third quarter", "bottom": "Bottom"}
    caption_position = cols3[0].radio("Caption Position", list(caption_options.values()), horizontal=True)
    # Display caption position selection (optional)
    caption_position_key = list(caption_options.keys())[list(caption_options.values()).index(caption_position)]
    # Add checkbox for remove punctuation
    remove_punctuation = cols3[0].checkbox("Remove punctuation", value=False)  # Default checked

    # Get available fonts from the "font" folder
    font_files = [f for f in os.listdir(font_folder) if f.endswith((".ttf", ".otf"))]
    # Extract font names without extensions
    available_fonts = [os.path.splitext(f)[0] for f in font_files]  # Get filename without extension

    # Display a dropdown to select font (show only name)
    if available_fonts:
        selected_font = cols3[0].selectbox("Font type", available_fonts)
        font_path = os.path.join(font_folder, font_files[available_fonts.index(selected_font)])
    else:
        st.warning("No font files found in the 'font' folder.")
        selected_font = None
        font_path = None  # Set to None if no fonts found

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    upload_font = cols3[0].file_uploader("Choose a font file (TTF, OTF)", type=["ttf", "otf"],
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
            cols3[0].success(f"Font '{font_name}' uploaded and saved successfully!")
            st.session_state["file_uploader_key"] += 1
            st.rerun()
        except Exception as e:
            st.error(f"Error saving font: {e}")

    # Preview font display (if font path available)
    if selected_font:
        st.session_state.cropped_thumbnail = video_thumbnail(st.session_state.crop_video_path)
        preview_text = cols3[0].text_input("Edit preview text", "This is a preview of the selected font.")
        captions_thumbnail_path = image_add_captions(
            image_path=st.session_state.cropped_thumbnail, text=preview_text,
            color=font_color, fontsize=font_size, remove_punctuation=remove_punctuation, font=font_path,
            position=caption_position_key)
        cols3[1].image(captions_thumbnail_path)

    if 'trimmed_subtitles' in st.session_state:
        with st.expander('Expand edit captions', expanded=False):
            st.session_state.trimmed_subtitles = srt_editor(st.session_state.trimmed_subtitles, time_range=(None, None))

    if st.button("Make captions"):
        with st.spinner('Adding captions...'):
            video_captions_path = video_add_captions(
                st.session_state.trimmed_subtitles, st.session_state.crop_video_path,
                color=font_color, fontsize=font_size, remove_punctuation=remove_punctuation, font=font_path,
                position=caption_position_key)
            st.success("Video Captions added successfully!")
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
