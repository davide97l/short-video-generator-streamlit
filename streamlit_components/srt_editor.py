import streamlit as st
import re
import os

def parse_srt(srt_text):
    """Parses SRT text into a list of dictionaries."""
    srt_data = []
    pattern = r"(\d+)\n(\d+:\d+:\d+,\d{3}) --> (\d+:\d+:\d+,\d{3})\n(.*?)(?=\n\d+|$)"
    matches = re.findall(pattern, srt_text, re.DOTALL)
    for sequence_number, start_time, end_time, sentence in matches:
        srt_data.append({
            "sequence_number": sequence_number,
            "start_time": start_time,
            "end_time": end_time,
            "sentence": sentence.strip()
        })
    return srt_data

def format_srt(srt_data):
    """Formats SRT data back into SRT text."""
    srt_text = ""
    for item in srt_data:
        srt_text += f"{item['sequence_number']}\n{item['start_time']} --> {item['end_time']}\n{item['sentence']}\n\n"
    return srt_text

def edit_srt(srt_data):
    """Edits SRT data based on user modifications."""
    for item in srt_data:
        new_sentence = st.text_input(f"Sentence {item['sequence_number']}: {str(item['start_time']).split(',')[0]} -->"
                                     f" {str(item['end_time']).split(',')[0]}", item["sentence"])
        if new_sentence:
            item["sentence"] = new_sentence.strip()

def srt_editor(input_file, output_file=None):
    """Reusable Streamlit component for SRT file editing."""

    # Option 1: Specify a default file path
    if input_file:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                srt_text = f.read()
            srt_data = parse_srt(srt_text)
        except FileNotFoundError:
            st.error("File not found. Please check the default path.")
            return

    if srt_data:
        edit_srt(srt_data)

        if st.button("Save Changes"):
            # Modify these paths as needed for saving
            if not output_file:
                input_filepath = os.path.abspath(os.path.expanduser(os.path.expandvars(input_file)))
                base, ext = os.path.splitext(input_filepath)
                output_file = base + "_mod" + ext
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(format_srt(srt_data))
            st.success("File saved successfully!")