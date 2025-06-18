import cv2
import numpy as np

class MedianFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.window = "Noise reduction"
        self.ksize = 5
        self.max_ksize = 31
        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)
        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)
        cv2.createTrackbar("ksize", self.window, self.ksize, self.max_ksize, self.median_filtering)

    def median_filtering(self, val):
        k = cv2.getTrackbarPos("ksize", self.window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        self.ksize = k
        filtered = cv2.medianBlur(self.original_img, self.ksize)
        cv2.imshow(self.window, filtered)

    def run(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Usage
# Replace with your local image path
# app = MedianFilterApp(r"C:\Users\User\Desktop\screenshot_video_streaming.png")
# app.run()
