
# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py
import cv2
import numpy as np

class NonLocalMeansFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.window = "Noise reduction"
        self.init_done = False  # 🔒 Flag to avoid early callback errors

        self.h = 10
        self.hColor = 10
        self.templateWindowSize = 7
        self.searchWindowSize = 21

        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)

        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)

        cv2.createTrackbar("h", self.window, self.h, 50, self.non_local_means_filtering)
        cv2.createTrackbar("hColor", self.window, self.hColor, 50, self.non_local_means_filtering)
        cv2.createTrackbar("templateWindowSize", self.window, self.templateWindowSize, 21, self.non_local_means_filtering)
        cv2.createTrackbar("searchWindowSize", self.window, self.searchWindowSize, 35, self.non_local_means_filtering)

        self.init_done = True  # ✅ Enable callbacks
        self.non_local_means_filtering()

    def non_local_means_filtering(self, val=None):
        if not self.init_done:
            return  # 🛑 Prevent early callback errors

        self.h = cv2.getTrackbarPos("h", self.window)
        self.hColor = cv2.getTrackbarPos("hColor", self.window)
        self.templateWindowSize = cv2.getTrackbarPos("templateWindowSize", self.window)
        self.searchWindowSize = cv2.getTrackbarPos("searchWindowSize", self.window)

        # Adjust for constraints
        if self.templateWindowSize % 2 == 0: self.templateWindowSize += 1
        if self.searchWindowSize % 2 == 0: self.searchWindowSize += 1
        if self.templateWindowSize < 3: self.templateWindowSize = 3
        if self.searchWindowSize < 7: self.searchWindowSize = 7

        filtered = cv2.fastNlMeansDenoisingColored(
            self.original_img, None, self.h, self.hColor,
            self.templateWindowSize, self.searchWindowSize
        )
        cv2.imshow(self.window, filtered)

    def run(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()
