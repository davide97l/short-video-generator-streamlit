import os
import sys
import unittest
from ..download_video_youtube import download_video_youtube


class TestDownloadYoutubeVideo(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.path = "test_data"
        self.filename = 'youtube_video'
        self.full_path = os.path.join(self.path, self.filename + '.mp4')

        # Ensure the test file does not exist before testing
        if os.path.exists(self.full_path):
            os.remove(self.full_path)

    def test_download_youtube_video(self):
        download_video_youtube(self.url, resolution=None, path=self.path, filename=self.filename)
        self.assertTrue(os.path.exists(self.full_path))


if __name__ == "__main__":
    unittest.main()
