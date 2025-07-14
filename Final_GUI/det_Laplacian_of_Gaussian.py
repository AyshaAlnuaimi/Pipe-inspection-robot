import cv2
import numpy as np

class LoGEdgeDetector:
    def __init__(self):
        self.sigma = 2.0
        self.trackbar_window = "LoG Trackbars"

        cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.trackbar_window, 400, 100)
        cv2.createTrackbar("Sigma x10", self.trackbar_window, int(self.sigma * 10), 50, lambda x: None)

    def apply(self, frame):
        # Get sigma from trackbar (scale by /10 to allow float input)
        if cv2.getWindowProperty(self.trackbar_window, cv2.WND_PROP_VISIBLE) >= 1:
            raw_sigma = cv2.getTrackbarPos("Sigma x10", self.trackbar_window)
            self.sigma = max(0.1, raw_sigma / 10.0)  # Avoid sigma=0


            # i commented this as it wasn't showing any results at the beggining but now its worling 
        # Convert to grayscale if needed
        # if len(frame.shape) == 3:
        #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # else:
        #     gray = frame.copy()

        # Compute LoG kernel size based on sigma
        size = int(6 * self.sigma + 1)
        if size % 2 == 0:
            size += 1

        x, y = np.meshgrid(np.arange(-size//2 + 1, size//2 + 1),
                           np.arange(-size//2 + 1, size//2 + 1))
        kernel = -(1/(np.pi * self.sigma**4)) * (
            1 - ((x**2 + y**2) / (2 * self.sigma**2))
        ) * np.exp(-(x**2 + y**2) / (2 * self.sigma**2))
        kernel = kernel / np.sum(np.abs(kernel))

        # Apply LoG using OpenCV's filter2D
        result = cv2.filter2D(gray, -1, kernel)
        result = cv2.convertScaleAbs(result)
        # Normalize to 0–255
        result = 255 * (result - np.min(result)) / (np.max(result) - np.min(result))
        result = result.astype(np.uint8)
        return result

# import cv2
# import numpy as np
# from scipy.ndimage import convolve

# class LoGEdgeDetector:
#     def __init__(self):
#         self.sigma = 2.0
#         self.trackbar_window = "LoG Trackbars"

#         cv2.namedWindow(self.trackbar_window, cv2.WINDOW_NORMAL)
#         cv2.resizeWindow(self.trackbar_window, 400, 100)
#         cv2.createTrackbar("Sigma x10", self.trackbar_window, int(self.sigma * 10), 50, lambda x: None)

#     def apply(self, frame):
#         # Get sigma from trackbar
#         if cv2.getWindowProperty(self.trackbar_window, cv2.WND_PROP_VISIBLE) >= 1:
#             raw_sigma = cv2.getTrackbarPos("Sigma x10", self.trackbar_window)
#             self.sigma = max(0.1, raw_sigma / 10.0)

#         # Convert to grayscale
#         if len(frame.shape) == 3:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         else:
#             gray = frame.copy()

#         # Generate LoG kernel
#         size = int(6 * self.sigma + 1)
#         if size % 2 == 0:
#             size += 1

#         x, y = np.meshgrid(np.arange(-size//2 + 1, size//2 + 1),
#                         np.arange(-size//2 + 1, size//2 + 1))
#         kernel = -(1 / (np.pi * self.sigma**4)) * (
#             1 - ((x**2 + y**2) / (2 * self.sigma**2))
#         ) * np.exp(-(x**2 + y**2) / (2 * self.sigma**2))
#         kernel = kernel / np.sum(np.abs(kernel))

#         # Apply LoG
#         result = convolve(gray.astype(np.float32), kernel, mode='reflect')

#         # Normalize to 0–255
#         result = 255 * (result - np.min(result)) / (np.max(result) - np.min(result))
#         result = result.astype(np.uint8)

#         # Apply binary thresholding (adjust threshold as needed)
#         _, binary = cv2.threshold(result, 30, 255, cv2.THRESH_BINARY)

#         return binary
