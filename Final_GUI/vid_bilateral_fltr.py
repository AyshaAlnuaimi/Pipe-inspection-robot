# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py
import cv2
import numpy as np

class BilateralFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.display_window = "Live Stream"
        self.trackbar_window = "Trackbars"

        self.d = 5
        self.max_d = 15
        self.sigmaColor = 50
        self.max_sigmaColor = 200
        self.sigmaSpace = 50
        self.max_sigmaSpace = 200

        self.filtered_image = None
        self.save_filter = False 
        self.original_img = cv2.imread(self.image_path)

        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 120)

        cv2.createTrackbar("d", self.trackbar_window, self.d, self.max_d, self.on_trackbar)
        cv2.createTrackbar("sigmaColor", self.trackbar_window, self.sigmaColor, self.max_sigmaColor, self.on_trackbar)
        cv2.createTrackbar("sigmaSpace", self.trackbar_window, self.sigmaSpace, self.max_sigmaSpace, self.on_trackbar)

        self.on_trackbar(None)

    def on_trackbar(self, val):
        self.d = max(1, cv2.getTrackbarPos("d", self.trackbar_window))
        self.sigmaColor = cv2.getTrackbarPos("sigmaColor", self.trackbar_window)
        self.sigmaSpace = cv2.getTrackbarPos("sigmaSpace", self.trackbar_window)

        self.filtered_image = cv2.bilateralFilter(
            self.original_img, self.d, self.sigmaColor, self.sigmaSpace
        )

        cv2.imshow(self.display_window, self.filtered_image)

    def run(self):
        while True:
            key = cv2.waitKey(100) & 0xFF
            if key == ord('s'):
                self.save_filter = True
                print(f"[INFO] Bilateral filter saved (d={self.d}, sigmaColor={self.sigmaColor}, sigmaSpace={self.sigmaSpace})")
                break
            elif key == ord('i'):
                self.save_filter = False
                self.filtered_image = None
                print("[INFO] Bilateral filter ignored.")
                break
            if cv2.getWindowProperty(self.trackbar_window, cv2.WND_PROP_VISIBLE) < 1:
                self.save_filter = False
                self.filtered_image = None
                print("[INFO] Trackbar window closed. Filter ignored.")
                break

        cv2.destroyWindow(self.trackbar_window)
