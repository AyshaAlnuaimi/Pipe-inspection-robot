import cv2
import numpy as np

class GaussianFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.display_window = "Live Stream"
        self.trackbar_window = "Trackbars"

        self.ksize = 5
        self.sigmaX = 1.5
        self.max_ksize = 31
        self.max_sigma = 100

        self.filtered_image = None
        self.save_filter = False  # ✅ New flag
        self.original_img = cv2.imread(self.image_path)

        self.init_done = False
        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 100)
        cv2.createTrackbar("ksize", self.trackbar_window, self.ksize, self.max_ksize, self.update_filter)
        cv2.createTrackbar("sigmaX", self.trackbar_window, int(self.sigmaX * 10), self.max_sigma, self.update_filter)
        self.init_done = True
        self.update_filter()

    def update_filter(self, val=None):
        if not self.init_done:
            return

        k = cv2.getTrackbarPos("ksize", self.trackbar_window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        self.ksize = k

        sigma = cv2.getTrackbarPos("sigmaX", self.trackbar_window)
        self.sigmaX = sigma / 10.0

        self.filtered_image = cv2.GaussianBlur(
            self.original_img,
            (self.ksize, self.ksize),
            self.sigmaX
        )
        cv2.imshow(self.display_window, self.filtered_image)

    def run(self):
        print("[INFO] Press 's' to save, or 'i' to ignore.")
        while True:
            key = cv2.waitKey(100) & 0xFF
            if key == ord('s'):
                self.save_filter = True
                print(f"[INFO] Saved Gaussian filter with ksize={self.ksize}, sigmaX={self.sigmaX}")
                break
            elif key == ord('i'):
                self.filtered_image = None
                self.save_filter = False
                print("[INFO] Ignored Gaussian filter.")
                break
            if cv2.getWindowProperty(self.trackbar_window, cv2.WND_PROP_VISIBLE) < 1:
                print("[INFO] Window closed. Ignoring filter.")
                self.filtered_image = None
                self.save_filter = False
                break
        cv2.destroyWindow(self.trackbar_window)
