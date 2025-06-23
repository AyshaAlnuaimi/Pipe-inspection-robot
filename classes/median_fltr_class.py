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



# import cv2
# import numpy as np

# class MedianFilterApp:
#     def __init__(self, video_url):
#         self.video_url = video_url
#         self.window = "Noise reduction"
#         self.ksize = 5
#         self.max_ksize = 31
#         self.cap = cv2.VideoCapture(self.video_url)
#         self.current_frame = None
#         self.init_done = False  # Prevent early callback errors
#         self.setup_window()

#     def setup_window(self):
#         cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
#         cv2.resizeWindow(self.window, 1280, 720)

#         # Create trackbar AFTER window is created
#         cv2.createTrackbar("ksize", self.window, self.ksize, self.max_ksize, self.median_filtering)
#         self.init_done = True

#     def median_filtering(self, val=None):
#         if not self.init_done or self.current_frame is None:
#             return
#         k = cv2.getTrackbarPos("ksize", self.window)
#         if k % 2 == 0:
#             k += 1
#         if k < 1:
#             k = 1
#         self.ksize = k
#         filtered = cv2.medianBlur(self.current_frame, self.ksize)
#         cv2.imshow(self.window, filtered)

#     def run(self):
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 print("Failed to grab frame")
#                 break

#             self.current_frame = frame.copy()
#             self.median_filtering()  # Apply filtering
#             if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
#                 break

#         self.cap.release()
#         cv2.destroyAllWindows()


# app = MedianFilterApp("http://192.168.3.5:8000/video")
# app.run()