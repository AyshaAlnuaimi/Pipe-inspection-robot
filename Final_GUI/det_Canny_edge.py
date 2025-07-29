import cv2

class CannyEdgeDetector:
    def __init__(self):
        self.low_threshold = 50
        self.high_threshold = 150
        self.trackbar_window = "Canny Trackbars"

        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 600, 100)
        cv2.createTrackbar("Low Threshold", self.trackbar_window, self.low_threshold, 255, lambda x: None)
        cv2.createTrackbar("High Threshold", self.trackbar_window, self.high_threshold, 255, lambda x: None)

    def apply(self, frame):
        # Only update thresholds if window is open
        if cv2.getWindowProperty(self.trackbar_window, cv2.WND_PROP_VISIBLE) >= 1:
            self.low_threshold = cv2.getTrackbarPos("Low Threshold", self.trackbar_window)
            self.high_threshold = cv2.getTrackbarPos("High Threshold", self.trackbar_window)

        # Always apply Canny edge with the last known values
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, self.low_threshold, self.high_threshold)
        return edges

