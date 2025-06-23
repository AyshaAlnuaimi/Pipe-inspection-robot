# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py

import cv2
import numpy as np
import time  # Make sure this import is at the top


class BilateralFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.window = "Noise reduction"
        self.d = 1
        self.max_d = 15
        self.sigmaColor = 1
        self.max_sigmaColor = 200
        self.sigmaSpace = 1
        self.max_sigmaSpace = 200

        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)

        self.init_done = False  # 🔴 Add this flag
        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)

        cv2.createTrackbar("d", self.window, self.d, self.max_d, self.bilateral_filtering)
        cv2.createTrackbar("sigmaColor", self.window, self.sigmaColor, self.max_sigmaColor, self.bilateral_filtering)
        cv2.createTrackbar("sigmaSpace", self.window, self.sigmaSpace, self.max_sigmaSpace, self.bilateral_filtering)

        self.init_done = True  # ✅ Mark initialization as done
        self.bilateral_filtering()  # ✅ Manually call after setup

    def bilateral_filtering(self, val=None):
        if not self.init_done:
            return  # ⛔️ Exit early if trackbars aren't ready

        d = cv2.getTrackbarPos("d", self.window)
        sigmaColor = cv2.getTrackbarPos("sigmaColor", self.window)
        sigmaSpace = cv2.getTrackbarPos("sigmaSpace", self.window)

        if d < 1:
            d = 1

        filtered = cv2.bilateralFilter(self.original_img, d, sigmaColor, sigmaSpace)
        cv2.imshow(self.window, filtered)

    def run(self):
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key to exit
                break
        cv2.destroyAllWindows()