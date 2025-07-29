import cv2
import numpy as np

class MedianFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.display_window = "Live Stream"
        self.trackbar_window = "Trackbars"
        self.ksize = 5
        self.max_ksize = 31
        self.filtered_image = None
        self.original_img = cv2.imread(self.image_path)
        self.save_filter = False  # <== New flag
        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 100)
        cv2.createTrackbar("ksize", self.trackbar_window, self.ksize, self.max_ksize, self.median_filtering)
        self.median_filtering(self.ksize)

    def median_filtering(self, val):
        k = cv2.getTrackbarPos("ksize", self.trackbar_window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        self.ksize = k
        self.filtered_image = cv2.medianBlur(self.original_img, k)
        cv2.imshow(self.display_window, self.filtered_image)

    def run(self):
        print(" Press 's' to save, or 'i' to ignore the filter.")
        while True:
            key = cv2.waitKey(100) & 0xFF
            if key == ord('s'):
                print(f" Filter saved with ksize={self.ksize}")
                self.save_filter = True
                break
            elif key == ord('i'):
                print(" Filter ignored.")
                self.filtered_image = None
                self.save_filter = False
                break
            if cv2.getWindowProperty(self.trackbar_window, cv2.WND_PROP_VISIBLE) < 1:
                print(" Window closed without choice. Ignoring.")
                self.filtered_image = None
                self.save_filter = False
                break
        cv2.destroyWindow(self.trackbar_window)
