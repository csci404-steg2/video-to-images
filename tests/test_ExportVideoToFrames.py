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
        self.clip = VideoFileClip("../media/big_buck_bunny.mp4", audio=False)

    def test_get_frames_iter(self):
        """Tests retrieving an iterator of frames from the given video file."""
        self.clip = VideoFileClip("../media/big_buck_bunny.mp4", audio=False)

        # let's only retrieve the frames of the initial second for now.
        subclip = self.clip.subclip(0, 1)

        frames = subclip.iter_frames()

        # now that we have our frames we can analyze them with pillow or 
        # write them to the disk.

    def test_write_images_sequence(self):
        """Tests writing every frame of a VideoFileClip to disk.

        I don't think this will be needed, but perhaps we may use it in 
            the future. 
        """
        self.clip = VideoFileClip("../media/big_buck_bunny.mp4", audio=False)

        # let's retrieve only a few frames from the video.
        subclip: VideoFileClip = self.clip.subclip(0, 0.05)

        subclip.write_images_sequence("../media/image_export/frame_%04d.png")


if __name__ == "__main__":
    unittest.main()
