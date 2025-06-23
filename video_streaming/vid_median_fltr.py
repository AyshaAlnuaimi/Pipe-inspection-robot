import cv2
import numpy as np

class MedianFilterApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.display_window = "Live Stream / Image"  # Reuse the main window
        self.trackbar_window = "Trackbars"
        self.ksize = 5
        self.max_ksize = 31
        self.filtered_image = None
        self.original_img = cv2.imread(self.image_path)
        print("Image shape:", self.original_img.shape)
        self.setup_window()

    def setup_window(self):
        # Do NOT create a new image window — reuse the existing one
        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 100)
        cv2.createTrackbar("ksize", self.trackbar_window, self.ksize, self.max_ksize, self.median_filtering)

    def median_filtering(self, val):
        k = cv2.getTrackbarPos("ksize", self.trackbar_window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        self.ksize = k
        self.filtered_image = cv2.medianBlur(self.original_img, self.ksize)
        cv2.imshow(self.display_window, self.filtered_image)  # Update same image window

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
        cv2.destroyWindow(self.trackbar_window)  # Only close the trackbar window
