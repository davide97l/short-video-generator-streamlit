import os
from PIL import Image


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
        if filename_base == file_base and target_ext.lower() == file_ext.lower():
            return True
    return False


def box_algorithm(img: Image, aspect_ratio: tuple = None) -> dict:
    # Find a recommended box for the image (could be replaced with image detection)
    box = (img.width * 0.05, img.height * 0.05, img.width * 0.95, img.height * 0.95)
    box = [int(i) for i in box]
    height = box[3] - box[1]
    width = box[2] - box[0]

    # If an aspect_ratio is provided, then fix the aspect
    if aspect_ratio:
        ideal_aspect = aspect_ratio[0] / aspect_ratio[1]
        height = (box[3] - box[1])
        current_aspect = width / height
        if current_aspect > ideal_aspect:
            new_width = int(ideal_aspect * height)
            offset = (width - new_width) // 2
            resize = (offset, 0, -offset, 0)
        else:
            new_height = int(width / ideal_aspect)
            offset = (height - new_height) // 2
            resize = (0, offset, 0, -offset)
        box = [box[i] + resize[i] for i in range(4)]
        left = box[0]
        top = box[1]
        width = 0
        iters = 0
        while width < box[2] - left:
            width += aspect_ratio[0]
            iters += 1
        height = iters * aspect_ratio[1]
    else:
        left = box[0]
        top = box[1]
        width = box[2] - box[0]
        height = box[3] - box[1]
    return {'left': int(left), 'top': int(top), 'width': int(width), 'height': int(height)}
