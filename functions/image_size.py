from PIL import Image


def get_image_size(image_path):
    """
    This function takes an image path as input and returns its size (width, height) in pixels.

    Args:
        image_path (str): Path to the image file.

    Returns:
        tuple: A tuple containing the image width and height (width, height).

    Raises:
        IOError: If the image file cannot be opened.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except OSError:
        raise IOError(f"Could not open image file: {image_path}")