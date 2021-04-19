from moviepy.editor import *
import unittest
import os

# Because I used relative paths below; please ensure you run this test script 
# from the tests directory.

class TestExportVideoToFrames(unittest.TestCase):
    """Tests for interacting with Video Files via the moviepy package.

    Note that you need the specified sample video file for this test to pass.
    I retrieved the sample file here: 
    https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_5mb.mp4
    """

    def test_init_video_file(self):
        """Tests initializing a VideoFileClip object."""

        # print(f'Current Directory is: {os.getcwd()}')

        # note that this video file is not included in repository.
        with VideoFileClip("../media/ben_test.mp4", audio=False) as clip:
            pass

    def test_get_frames_iter(self):
        """Tests retrieving an iterator of frames from the given video file."""
        with VideoFileClip("../media/ben_test.mp4", audio=False) as clip:

            # let's only retrieve the frames of the initial second for now.
            with clip.subclip(0, 1) as subclip:
                frames = subclip.iter_frames()

        # now that we have our frames we can analyze them with pillow or 
        # write them to the disk.

    def test_write_images_sequence(self):
        """Tests writing every frame of a VideoFileClip to disk.

        I don't think this will be needed, but perhaps we may use it in 
            the future. 
        """
        with VideoFileClip("../media/ben_test.mp4", audio=False) as clip:
            # let's retrieve only a few frames from the video.
            with clip.subclip(0.5, 1) as subclip:
                subclip.write_images_sequence("../media/image_export/frame_%04d.png")


if __name__ == "__main__":
    unittest.main()
