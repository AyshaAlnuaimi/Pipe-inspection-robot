
# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py


import cv2
import numpy as np

class NonLocalMeansFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.display_window = "Live Stream / Image"  # Use the shared main window
        self.trackbar_window = "Trackbars"

        self.h = 10
        self.hColor = 10
        self.templateWindowSize = 7
        self.searchWindowSize = 21

        self.filtered_image = None
        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)

        self.init_done = False
        self.setup_window()

    def setup_window(self):
        # Only create the trackbar window
        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 500, 150)

        cv2.createTrackbar("h", self.trackbar_window, self.h, 50, self.on_trackbar)
        cv2.createTrackbar("hColor", self.trackbar_window, self.hColor, 50, self.on_trackbar)
        cv2.createTrackbar("templateWindowSize", self.trackbar_window, self.templateWindowSize, 21, self.on_trackbar)
        cv2.createTrackbar("searchWindowSize", self.trackbar_window, self.searchWindowSize, 35, self.on_trackbar)

        self.init_done = True
        self.on_trackbar()

    def on_trackbar(self, val=None):
        if not self.init_done:
            return

        self.h = cv2.getTrackbarPos("h", self.trackbar_window)
        self.hColor = cv2.getTrackbarPos("hColor", self.trackbar_window)
        self.templateWindowSize = cv2.getTrackbarPos("templateWindowSize", self.trackbar_window)
        self.searchWindowSize = cv2.getTrackbarPos("searchWindowSize", self.trackbar_window)

        # Enforce odd sizes and minimum thresholds
        if self.templateWindowSize % 2 == 0: self.templateWindowSize += 1
        if self.templateWindowSize < 3: self.templateWindowSize = 3
        if self.searchWindowSize % 2 == 0: self.searchWindowSize += 1
        if self.searchWindowSize < 7: self.searchWindowSize = 7

        self.filtered_image = cv2.fastNlMeansDenoisingColored(
            self.original_img, None, self.h, self.hColor,
            self.templateWindowSize, self.searchWindowSize
        )

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

