import cv2
import numpy as np
#https://medium.com/@rajilini/laplacian-of-gaussian-filter-log-for-image-processing-c2d1659d5d2


class SobelEdgeDetector:
    def __init__(self):
        self.ksize = 3
        self.trackbar_window = "Sobel Trackbars"

        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 100)
        cv2.createTrackbar("Kernel Size", self.trackbar_window, self.ksize, 7, lambda x: None)

    def apply(self, frame):
        if cv2.getWindowProperty(self.trackbar_window, cv2.WND_PROP_VISIBLE) >= 1:
            ksize = cv2.getTrackbarPos("Kernel Size", self.trackbar_window)
            # Ensure kernel size is odd and >= 1
            self.ksize = max(1, ksize if ksize % 2 == 1 else ksize + 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self.ksize)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self.ksize)

        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        magnitude = np.uint8(255 * magnitude / np.max(magnitude))

        return magnitude
