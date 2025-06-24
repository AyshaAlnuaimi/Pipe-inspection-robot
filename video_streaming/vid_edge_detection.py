import tkinter as tk
import cv2
from det_Canny_edge import CannyEdgeDetector

class EdgeDetectionApp:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.canny_detector = CannyEdgeDetector()


    def setup_ui(self):
        self.clear_root()
        tk.Label(self.root, text="Choose Technique for Edge Detection:").pack(pady=10)
        tk.Button(self.root, text="Apply Canny Edge", command=self.enable_canny).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=10)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def enable_canny(self):
        edge_frame = self.canny_detector.apply(self.frame)
        cv2.imshow("Live Stream", edge_frame)


    def stream_video_with_canny(self):
        cap = cv2.VideoCapture(self.stream_url)
        if not cap.isOpened():
            print("[ERROR] Cannot open video stream.")
            return

        print("[INFO] Canny Edge Detection Running. Press 'q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if self.apply_canny and self.canny_detector:
                frame = self.canny_detector.apply(frame)

            cv2.imshow("Canny Edge Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
