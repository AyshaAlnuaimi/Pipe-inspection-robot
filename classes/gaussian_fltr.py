
# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py

import cv2
import numpy as np

class GaussianFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.window = "Noise reduction"

        self.gaussian_filtering_ksize = 5
        self.sigmaX = 1.5
        self.init_done = False  # 🟡 Flag to block early callbacks

        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)

        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)

        cv2.createTrackbar("ksize", self.window, self.gaussian_filtering_ksize, 31, self.gaussian_filtering)
        cv2.createTrackbar("sigmaX", self.window, int(self.sigmaX * 10), 100, self.gaussian_filtering)

        self.init_done = True  # ✅ Enable processing
        self.gaussian_filtering()  # ✅ Trigger once after setup

    def gaussian_filtering(self, val=None):
        if not self.init_done:
            return  # ⛔ Skip if trackbars aren't ready yet

        k = cv2.getTrackbarPos("ksize", self.window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        self.gaussian_filtering_ksize = k

        sigma = cv2.getTrackbarPos("sigmaX", self.window)
        self.sigmaX = sigma / 10.0

        filtered = cv2.GaussianBlur(
            self.original_img,
            (self.gaussian_filtering_ksize, self.gaussian_filtering_ksize),
            self.sigmaX
        )
        cv2.imshow(self.window, filtered)

    def run(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()
