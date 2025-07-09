import tkinter as tk
import cv2
import os
import numpy

    
from det_Canny_edge import CannyEdgeDetector
from vid_median_fltr import MedianFilterApp
from vid_gaussian_fltr import GaussianFilterApp
from vid_bilateral_fltr import BilateralFilterApp
    
    
class NoiseReductionApp:
    def __init__(self, root):
        self.root = root
        #noise reduction flags
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
        self.canny_detector = None
        
        self.enable_screenshot = False


        # External dependencies (to be set later)
        self.cap = None
        self.root = None
        self.current_image_path = ""
        self.original_image_path = ""
        self.current_frame = None

    def show_video_stream(self):
        def update_frame():
            ret, frame = self.cap.read()
            if not ret:
                self.root.after(30, update_frame)
                return

            processed = frame.copy()

            # Apply the selected noise filter
            if self.apply_median:
                k = self.median_ksize
                k = k + 1 if k % 2 == 0 else k
                processed = cv2.medianBlur(processed, k)

            elif self.apply_gaussian:
                k = self.gaussian_ksize
                k = k + 1 if k % 2 == 0 else k
                processed = cv2.GaussianBlur(processed, (k, k), self.gaussian_sigmaX)

            elif self.apply_bilateral:
                d = max(1, self.bilateral_d)
                processed = cv2.bilateralFilter(processed, d, self.bilateral_sigmaColor, self.bilateral_sigmaSpace)

            # Apply Canny edge if enabled
            if self.apply_canny and self.canny_detector is not None:
                processed = self.canny_detector.apply(processed)
                processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
            
            if self.enable_screenshot:
                SAVE_DIR = r"C:\Users\User\Desktop\extract_images_from_vid_streaming"
                os.makedirs(SAVE_DIR, exist_ok=True)

                saved_count = 0
                total_to_save = 20

                while saved_count < total_to_save:
                    filename = os.path.join(SAVE_DIR, f"frame_{saved_count:04d}.png")
                    cv2.imwrite(filename, processed)
                    saved_count += 1
                    cv2.waitKey(100)  # wait a bit between saves (100 ms)
                enable_screenshot = False
        

            self.current_frame = frame                # raw video frame
            self.filtered_frame = processed           # final processed frame

            cv2.imshow("Live Stream", processed)
            self.root.after(30, update_frame)

        update_frame()



    # def show_video_stream(self):
    #     def update_frame():
    #         ret, frame = self.cap.read()
    #         if ret:
    #             #if any if the filters applied
    #             if self.apply_median:
    #                 k = self.median_ksize
    #                 if k % 2 == 0: k += 1
    #                 frame = cv2.medianBlur(frame, k)
    #             elif self.apply_gaussian:
    #                 k = self.gaussian_ksize
    #                 if k % 2 == 0: k += 1
    #                 frame = cv2.GaussianBlur(frame, (k, k), self.gaussian_sigmaX)
    #             elif self.apply_bilateral:
    #                 d = max(1, self.bilateral_d)
    #                 frame = cv2.bilateralFilter(frame, d, self.bilateral_sigmaColor, self.bilateral_sigmaSpace)
    #             elif self.apply_canny and self.canny_detector is not None:
    #                 frame = self.canny_detector.apply(frame)
    #                 frame = cv2.canny(frame, cv2.COLOR_GRAY2BGR)  # Convert to BGR to display correctly
                    
    #             self.current_frame = frame
    #             cv2.imshow("Live Stream", frame)
    #         self.root.after(30, update_frame)
    #     update_frame()

    def capture_current_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                cv2.imwrite(self.current_image_path, frame)
                cv2.imwrite(self.original_image_path, frame)
                print(f"[INFO] Frame captured to {self.current_image_path}")

    def reset_image(self):
        self.apply_median = False
        self.apply_gaussian = False
        self.apply_bilateral = False
        self.apply_canny = False
        self.canny_detector = None
        self.screenshot = False
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

    def apply_canny_edge(self):
        if self.canny_detector is None:
            self.canny_detector = CannyEdgeDetector()
        self.apply_canny = True
        print("[INFO] Live Canny Edge Detection Enabled.")
            
        
    def extract_images_from_stream(self):
        self.enable_screenshot = True
        
