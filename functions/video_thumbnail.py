import cv2
import os


def video_thumbnail(video_path):
    """Extracts the first frame of the video as a thumbnail and saves it.

    Args:
        video_path (str): Path to the video file.

    Returns:
        str: Path to the saved thumbnail (or None if errors occur).
    """

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file!")
        return None

    # Read the first frame
    success, frame = cap.read()
    if not success:
        print("Error reading video file!")
        return None

    # Construct the thumbnail path
    dirname, filename = os.path.split(video_path)  # Split path and filename
    thumbnail_path = os.path.join(dirname, f"{filename.split('.')[0]}.jpg")

    # Save the first frame as a thumbnail
    cv2.imwrite(thumbnail_path, frame)
    cap.release()

    return thumbnail_path
