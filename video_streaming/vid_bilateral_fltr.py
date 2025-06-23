# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py

import cv2
import numpy as np

class BilateralFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.display_window = "Live Stream / Image"  # Use existing main window
        self.trackbar_window = "Trackbars"

        self.d = 5
        self.max_d = 15
        self.sigmaColor = 50
        self.max_sigmaColor = 200
        self.sigmaSpace = 50
        self.max_sigmaSpace = 200

        self.filtered_image = None
        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)

        self.setup_window()

    def setup_window(self):
        # Create only trackbar window
        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 120)

        cv2.createTrackbar("d", self.trackbar_window, self.d, self.max_d, self.on_trackbar)
        cv2.createTrackbar("sigmaColor", self.trackbar_window, self.sigmaColor, self.max_sigmaColor, self.on_trackbar)
        cv2.createTrackbar("sigmaSpace", self.trackbar_window, self.sigmaSpace, self.max_sigmaSpace, self.on_trackbar)

        self.on_trackbar(None)

    def on_trackbar(self, val):
        self.d = cv2.getTrackbarPos("d", self.trackbar_window)
        self.sigmaColor = cv2.getTrackbarPos("sigmaColor", self.trackbar_window)
        self.sigmaSpace = cv2.getTrackbarPos("sigmaSpace", self.trackbar_window)

        if self.d < 1:
            self.d = 1

        self.filtered_image = cv2.bilateralFilter(self.original_img, self.d, self.sigmaColor, self.sigmaSpace)

        cv2.imshow(self.display_window, self.filtered_image)

    def run(self):
        print("Press 's' to save, or 'i' to ignore changes.")
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                print("Filtered image saved.")
                break
            elif key == ord('i'):
                print("Changes ignored.")
                self.filtered_image = None
                break
        cv2.destroyWindow(self.trackbar_window)

