import cv2
import unittest

class TestExportVideoToFramesCV2(unittest.TestCase):
    # tutorial from https://theailearner.com/2018/10/15/extracting-and-saving-video-frames-using-opencv-python/

    def test_get_fps_of_video(self):
        cam = cv2.VideoCapture('../media/ben_test.mp4')
        fps = cam.get(cv2.CAP_PROP_FPS)
    
    def test_export_video(self):
        cam = cv2.VideoCapture('../media/ben_test.mp4')
        i = 0

        while(cam.isOpened()):
            ret, frame = cam.read()
            print(f'ret: {ret}, frame: {frame}')
            if ret == False:
                break
            cv2.imwrite(f"../media/image_export/frame_{i}.png", frame)
            i += 1

if __name__ == "__main__":
    unittest.main()
