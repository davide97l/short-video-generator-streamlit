import os


def text_add_color(text:str, substring:str, color: str):
    """
    Modifies the substring a inside string b such that a becomes ':color[a]'.

    Args:
        text: The string containing the substring to modify.
        substring: The substring to modify.

    Returns:
        The modified string text.
    """
    start_index = text.find(substring)
    if start_index != -1:
        end_index = start_index + len(substring)
        return text[:start_index] + f':{color}[' + substring + ']' + text[end_index:]
    else:
        return text


def has_paired_file(filename, target_ext):
    print(filename)
    """
    Checks if a file with the same name (without extension) and target extension exists in the same directory as the given filename.

    Args:
        filename: The full path or filename (without extension).
        target_ext: The target extension to check for (e.g., ".txt", ".jpg").

    Returns:
        True if a file with the same name (without extension) and target extension exists, False otherwise.
    """
    # Extract directory path and filename without extension
    directory = os.path.dirname(filename)
    base, _ = os.path.splitext(filename)  # Discard the original extension
    # Check all files in the directory
    for file in os.listdir(directory):
        file_base, file_ext = os.path.splitext(file)
        filename_base = base.split('/')[-1]
        print(filename_base, file_base, target_ext.lower(), file_ext.lower())
        if filename_base == file_base and target_ext.lower() == file_ext.lower():
            return True
    return False
