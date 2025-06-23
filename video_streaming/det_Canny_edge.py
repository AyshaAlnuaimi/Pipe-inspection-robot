import cv2
import numpy as np

class CannyEdgeDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.original_img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.edges = None
        self.back_requested = False

    def apply_canny(self):
        self.edges = cv2.Canny(self.original_img, 50, 150)
        cv2.imshow("Live Stream / Image", self.edges)

    def run(self):
        self.apply_canny()
        print("[INFO] Press 'b' to go back, or any other key to continue...")

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('b'):
                self.back_requested = True
                break
            elif key != 255:  # any other key
                break
