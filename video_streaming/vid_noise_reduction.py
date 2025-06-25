# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import cv2
# from vid_median_fltr import MedianFilterApp
# from vid_gaussian_fltr import GaussianFilterApp  # Your module
# from vid_bilateral_fltr import BilateralFilterApp  # Adjust import
# from vid_edge_detection import EdgeDetectionApp


# class NoiseReductionApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Noise Reduction Techniques")
#         self.cap = cv2.VideoCapture("http://192.168.3.5:8000/video")
#         self.current_frame = None
#         self.processed_image_path = None
#         self.current_image_path = "captured_frame.png"
#         self.original_image_path = "original_frame.png"

#         self.apply_median = False        # ✅ FIXED: initialize filter state inside the class
#         self.median_ksize = 5
        
#         self.apply_gaussian = False  # ✅ Add this
#         self.gaussian_ksize = 5
#         self.gaussian_sigmaX = 1.5
        
#         self.apply_bilateral = False
#         self.bilateral_d = 5
#         self.bilateral_sigmaColor = 50
#         self.bilateral_sigmaSpace = 50
        
    
#         self.show_video_stream()
#         self.setup_ui()

#     def show_video_stream(self):
#         def update_frame():
#             ret, frame = self.cap.read()
#             if ret:
#                 if self.apply_median:
#                     k = self.median_ksize
#                     if k % 2 == 0:
#                         k += 1
#                     frame = cv2.medianBlur(frame, k)

#                 elif self.apply_gaussian:
#                     k = self.gaussian_ksize
#                     if k % 2 == 0:
#                         k += 1
#                     frame = cv2.GaussianBlur(frame, (k, k), self.gaussian_sigmaX)

#                 elif self.apply_bilateral:
#                     d = max(1, self.bilateral_d)
#                     frame = cv2.bilateralFilter(frame, d, self.bilateral_sigmaColor, self.bilateral_sigmaSpace)
#                 self.current_frame = frame
#                 cv2.imshow("Live Stream", frame)
#             self.root.after(30, update_frame)
#         update_frame()


#     def capture_current_frame(self):
#         if self.cap is not None:
#             ret, frame = self.cap.read()
#             if ret:
#                 self.current_frame = frame
#                 cv2.imwrite(self.current_image_path, self.current_frame)
#                 cv2.imwrite(self.original_image_path, self.current_frame)
#                 print(f"[INFO] Frame captured to {self.current_image_path}")

#     def setup_ui(self):
#         self.clear_root()
#         tk.Label(self.root, text="Choose Technique for Noise Reduction (Optional):").pack(pady=10)
#         tk.Button(self.root, text="Apply Median Filter", command=self.apply_median_filter).pack(pady=5)
#         tk.Button(self.root, text="Apply GAussian Filter", command=self.apply_gaussian_filter).pack(pady=5)
#         tk.Button(self.root, text="Apply Bilateral Filter", command=self.apply_bilateral_filter).pack(pady=5)
#         tk.Button(self.root, text="Reset to Original", command=self.reset_image).pack(pady=5)
#         tk.Button(self.root, text="Skip", command=self.skip_processing).pack(pady=5)

#     def clear_root(self):
#         for widget in self.root.winfo_children():
#             widget.destroy()

#     def reset_image(self):
#         self.apply_median = False
#         self.apply_gaussian = False
#         self.apply_bilateral = False
#         print("[INFO] Reset to original stream (no filters applied).")



#     def apply_median_filter(self):
#         self.capture_current_frame()
#         app = MedianFilterApp(self.current_image_path)
#         app.run()

#         if app.save_filter and app.filtered_image is not None:
#             cv2.imwrite(self.current_image_path, app.filtered_image)  # ✅ Save filtered frame
#             self.apply_median = True
#             self.median_ksize = app.ksize
#             print(f"[INFO] Live stream now using median filter with ksize={self.median_ksize}")
#         else:
#             print("[INFO] Filter discarded.")


    
#     def apply_gaussian_filter(self):
#         self.capture_current_frame()
#         app = GaussianFilterApp(self.current_image_path)
#         app.run()

#         if app.save_filter and app.filtered_image is not None:
#             cv2.imwrite(self.current_image_path, app.filtered_image)  # ✅ Save filtered frame
#             self.apply_gaussian = True
#             self.gaussian_ksize = app.ksize
#             self.gaussian_sigmaX = app.sigmaX
#             self.filtered_image = app.filtered_image  # Optional
#             print(f"[INFO] Applied Gaussian filter with ksize={app.ksize}, sigmaX={app.sigmaX}")
#         else:
#             print("[INFO] Gaussian filter not applied.")

#     def apply_bilateral_filter(self):
#         self.capture_current_frame()
#         app = BilateralFilterApp(self.current_image_path)
#         app.run()

#         if app.save_filter and app.filtered_image is not None:
#             self.apply_median = False
#             self.apply_gaussian = False
#             cv2.imwrite(self.current_image_path, app.filtered_image)  # ✅ Save filtered frame
#             self.apply_bilateral = True
#             self.bilateral_d = app.d
#             self.bilateral_sigmaColor = app.sigmaColor
#             self.bilateral_sigmaSpace = app.sigmaSpace
#             print(f"[INFO] Applied bilateral filter (d={app.d}, sigmaColor={app.sigmaColor}, sigmaSpace={app.sigmaSpace})")
#         else:
#             print("[INFO] Bilateral filter not applied.")
            
#     def skip_processing(self):
#         print("[INFO] Skipping noise reduction. Moving to edge detection...")
#         # Pass the last filtered frame
#         edge_app = EdgeDetectionApp(self.root, self.current_frame)
#         edge_app.setup_ui()



            
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = NoiseReductionApp(root)
#     root.mainloop()


import tkinter as tk
import cv2
from det_Canny_edge import CannyEdgeDetector
from vid_median_fltr import MedianFilterApp
from vid_gaussian_fltr import GaussianFilterApp
from vid_bilateral_fltr import BilateralFilterApp

class NoiseReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noise Reduction Techniques")
        self.cap = cv2.VideoCapture("http://192.168.3.5:8000/video")
        self.current_frame = None
        self.current_image_path = "captured_frame.png"
        self.original_image_path = "original_frame.png"

        self.apply_median = False
        self.median_ksize = 5

        self.apply_gaussian = False
        self.gaussian_ksize = 5
        self.gaussian_sigmaX = 1.5

        self.apply_bilateral = False
        self.bilateral_d = 5
        self.bilateral_sigmaColor = 50
        self.bilateral_sigmaSpace = 50

        self.apply_canny = False
        self.canny_detector = None  # Will be created after skip

        self.show_video_stream()
        self.setup_ui()

    def show_video_stream(self):
        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                if self.apply_median:
                    k = self.median_ksize
                    if k % 2 == 0: k += 1
                    frame = cv2.medianBlur(frame, k)
                elif self.apply_gaussian:
                    k = self.gaussian_ksize
                    if k % 2 == 0: k += 1
                    frame = cv2.GaussianBlur(frame, (k, k), self.gaussian_sigmaX)
                elif self.apply_bilateral:
                    d = max(1, self.bilateral_d)
                    frame = cv2.bilateralFilter(frame, d, self.bilateral_sigmaColor, self.bilateral_sigmaSpace)

                # Apply canny if enabled
                if self.apply_canny and self.canny_detector:
                    frame = self.canny_detector.apply(frame)

                self.current_frame = frame
                cv2.imshow("Live Stream", frame)
            self.root.after(30, update_frame)
        update_frame()

    def capture_current_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                cv2.imwrite(self.current_image_path, frame)
                cv2.imwrite(self.original_image_path, frame)
                print(f"[INFO] Frame captured to {self.current_image_path}")

    def setup_ui(self):
        self.clear_root()
        tk.Label(self.root, text="Choose Technique for Noise Reduction (Optional):").pack(pady=10)
        tk.Button(self.root, text="Apply Median Filter", command=self.apply_median_filter).pack(pady=5)
        tk.Button(self.root, text="Apply Gaussian Filter", command=self.apply_gaussian_filter).pack(pady=5)
        tk.Button(self.root, text="Apply Bilateral Filter", command=self.apply_bilateral_filter).pack(pady=5)
        tk.Button(self.root, text="Reset to Original", command=self.reset_image).pack(pady=5)
        tk.Button(self.root, text="Apply canny edge", command=self.skip_processing).pack(pady=5)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def reset_image(self):
        self.apply_median = False
        self.apply_gaussian = False
        self.apply_bilateral = False
        self.apply_canny = False
        self.canny_detector = None
        print("[INFO] Reset to original stream (no filters or edge detection).")

    def apply_median_filter(self):
        self.capture_current_frame()
        app = MedianFilterApp(self.current_image_path)
        app.run()
        if app.save_filter and app.filtered_image is not None:
            cv2.imwrite(self.current_image_path, app.filtered_image)
            self.apply_median = True
            self.median_ksize = app.ksize
            print(f"[INFO] Applied Median Filter with ksize={app.ksize}")
        else:
            print("[INFO] Filter discarded.")

    def apply_gaussian_filter(self):
        self.capture_current_frame()
        app = GaussianFilterApp(self.current_image_path)
        app.run()
        if app.save_filter and app.filtered_image is not None:
            cv2.imwrite(self.current_image_path, app.filtered_image)
            self.apply_gaussian = True
            self.gaussian_ksize = app.ksize
            self.gaussian_sigmaX = app.sigmaX
            print(f"[INFO] Applied Gaussian Filter with ksize={app.ksize}, sigmaX={app.sigmaX}")
        else:
            print("[INFO] Gaussian filter not applied.")

    def apply_bilateral_filter(self):
        self.capture_current_frame()
        app = BilateralFilterApp(self.current_image_path)
        app.run()
        if app.save_filter and app.filtered_image is not None:
            self.apply_median = False
            self.apply_gaussian = False
            cv2.imwrite(self.current_image_path, app.filtered_image)
            self.apply_bilateral = True
            self.bilateral_d = app.d
            self.bilateral_sigmaColor = app.sigmaColor
            self.bilateral_sigmaSpace = app.sigmaSpace
            print(f"[INFO] Applied Bilateral Filter (d={app.d}, sigmaColor={app.sigmaColor}, sigmaSpace={app.sigmaSpace})")
        else:
            print("[INFO] Bilateral filter not applied.")

    def skip_processing(self):
        print("[INFO] Skipping noise reduction. Enabling Canny Edge Detection...")
        self.apply_canny = True
        self.canny_detector = CannyEdgeDetector()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoiseReductionApp(root)
    root.mainloop()
