
# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py


import cv2
import numpy as np

class GaussianFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.display_window = "Live Stream / Image"  # Reuse main image window
        self.trackbar_window = "Trackbars"

        self.gaussian_filtering_ksize = 5
        self.sigmaX = 1.5
        self.init_done = False
        self.filtered_image = None

        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)

        self.setup_window()

    def setup_window(self):
        # Only setup trackbars (image already displayed in main)
        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 100)
        cv2.createTrackbar("ksize", self.trackbar_window, self.gaussian_filtering_ksize, 31, self.gaussian_filtering)
        cv2.createTrackbar("sigmaX", self.trackbar_window, int(self.sigmaX * 10), 100, self.gaussian_filtering)

        self.init_done = True
        self.gaussian_filtering()

    def gaussian_filtering(self, val=None):
        if not self.init_done:
            return

        k = cv2.getTrackbarPos("ksize", self.trackbar_window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        self.gaussian_filtering_ksize = k

        sigma = cv2.getTrackbarPos("sigmaX", self.trackbar_window)
        self.sigmaX = sigma / 10.0

        self.filtered_image = cv2.GaussianBlur(
            self.original_img,
            (self.gaussian_filtering_ksize, self.gaussian_filtering_ksize),
            self.sigmaX
        )
        cv2.imshow(self.display_window, self.filtered_image)  # Update main window

    def run(self):
        print("Press 's' to save, or 'q' to quit without saving.")
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                if self.filtered_image is not None:
                    print("Filtered image saved.")
                break
            elif key == ord('q'):
                self.filtered_image = None
                print("Exiting without saving.")
                break
        cv2.destroyWindow(self.trackbar_window)  # Only close the control window
