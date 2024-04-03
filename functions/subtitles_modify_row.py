import re


def subtitles_modify_row(filepath, row_number, new_content=None):
    """
    Modifies an SRT file by replacing the content of a specific row with new content (if provided).

    Args:
        filepath (str): Path to the SRT file.
        new_content (str): New content to replace the existing content of the row (or None to keep it unchanged).
        row_number (int): Row number (0-based for both positive and negative indexing).

    Returns:
        tuple: (str, str) - A tuple containing the path to the modified SRT file and the content of the specified row.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        srt_data = file.read()

    # Split the SRT data into individual subtitle entries
    subtitle_pattern = r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|$)"
    subtitle_entries = re.findall(subtitle_pattern, srt_data, flags=re.DOTALL)

    # Get the number of rows (positive value)
    num_rows = len(subtitle_entries)

    # Handle negative row numbers (counting from the end)
    if row_number < 0:
        row_number = num_rows + row_number

    # Check if the requested row number is valid (considering both positive and negative indexing)
    if row_number < 0 or row_number >= num_rows:
        raise ValueError(f"Invalid row number: {row_number}")

    # Modify the content of the specified row (if new_content provided)
    if new_content is not None:
        subtitle_entries[row_number] = (
            subtitle_entries[row_number][0],  # Index
            subtitle_entries[row_number][1],  # Start time
            subtitle_entries[row_number][2],  # End time
            new_content,  # New content
        )

    # Join the modified subtitle entries back into a string
    modified_srt_data = "\n\n".join([f"{entry[0]}\n{entry[1]} --> {entry[2]}\n{entry[3]}" for entry in subtitle_entries])

    # Generate new filename with "_modified" suffix (if content changed)
    new_filepath = (f"{filepath.rsplit('.', 1)[0]}_modified.srt"
                    if new_content is not None else filepath)

    # Save the modified SRT data to a new file (if content changed)
    if new_content is not None:
        with open(new_filepath, 'w', encoding='utf-8') as file:
            file.write(modified_srt_data)

    # Return path and content of the specified row
    return new_filepath, subtitle_entries[row_number][3]


if __name__ == '__main__':
    filepath = "../data2/These_5_Books_Scaled_My_Business_to_Multiple_6_Figures.srt"
    new_content = 'hi'
    row_number = 0

    modified_filepath, edited_row_content = subtitles_modify_row(filepath, row_number, new_content)
    print(f"Modified SRT file saved to: {modified_filepath}")  # No change, original file path
    print(f"Edited row content: {edited_row_content}")
