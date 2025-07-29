import tkinter as tk
import cv2
import os
import numpy as np

    
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
        self.screenshot_count = 0
        self.total_screenshots_to_save = 20
        
        self.failure_detection_flag = False

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
                self.gray_edges = self.canny_detector.apply(processed)  # ← grayscale image
                processed = cv2.cvtColor(self.gray_edges, cv2.COLOR_GRAY2BGR)

                # processed = self.canny_detector.apply(processed)
                # processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
            
            if self.enable_screenshot and self.screenshot_count < self.total_screenshots_to_save:
                SAVE_DIR = r"C:\Users\User\Desktop\extract_images_from_vid_streaming"
                os.makedirs(SAVE_DIR, exist_ok=True)

                filename = os.path.join(SAVE_DIR, f"frame_{self.screenshot_count:04d}.png")
                cv2.imwrite(filename, processed)
                self.screenshot_count += 1
                cv2.waitKey(1000) 

                if self.screenshot_count >= self.total_screenshots_to_save:
                    self.enable_screenshot = False
                    print(" Done saving 20 screenshots.")
            
            
            #-------------------------------------------------------------------        
            # if self.failure_detection_flag:
            #     # Use gray_edges directly (from earlier) for contour detection
            #    if hasattr(self, "gray_edges") and self.gray_edges is not None:
            #     contours, _ = cv2.findContours(self.gray_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #     height, width = processed.shape[:2]
            #     for c in contours:
            #         x, y, w, h = cv2.boundingRect(c)
            #         area = cv2.contourArea(c)
            #         if h > (height // 2):
            #             continue
            #         if area < 150:
            #             continue

            #         cv2.rectangle(processed, (x, y), (x + w, y + h), (0, 0, 255), 1)
            #         cv2.drawContours(processed, [c], -1, (0, 255, 0), 1)
            
            if self.failure_detection_flag:
                if hasattr(self, "gray_edges") and self.gray_edges is not None:
                    # Apply morphological closing to connect broken edges
                    kernel = np.ones((3, 3), np.uint8)  # You can tweak this size (e.g., (5,5))
                    closed_edges = cv2.morphologyEx(self.gray_edges, cv2.MORPH_CLOSE, kernel)

                    # Now use the closed version for contour detection
                    contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    height, width = processed.shape[:2]
                    for c in contours:
                        x, y, w, h = cv2.boundingRect(c)
                        area = cv2.contourArea(c)
                        if h > (height // 2):
                            continue
                        if area < 150:
                            continue

                        cv2.rectangle(processed, (x, y), (x + w, y + h), (0, 0, 255), 1)
                        cv2.drawContours(processed, [c], -1, (0, 255, 0), 1)


            #-------------------------------------------------------------------------------
            
            self.current_frame = frame                # raw video frame
            self.filtered_frame = processed           # final processed frame

            cv2.imshow("Live Stream", processed)
            self.root.after(30, update_frame)

        update_frame()

    def capture_current_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                cv2.imwrite(self.current_image_path, frame)
                cv2.imwrite(self.original_image_path, frame)
                print(f" Frame captured to {self.current_image_path}")

    def reset_image(self):
        self.apply_median = False
        self.apply_gaussian = False
        self.apply_bilateral = False
        self.apply_canny = False
        self.canny_detector = None
        self.screenshot = False
        print(" Reset to original stream (no filters or edge detection).")

    def apply_median_filter(self):
        self.capture_current_frame()
        app = MedianFilterApp(self.current_image_path)
        app.run()
        if app.save_filter and app.filtered_image is not None:
            cv2.imwrite(self.current_image_path, app.filtered_image)
            self.apply_median = True
            self.median_ksize = app.ksize
            print(f" Applied Median Filter with ksize={app.ksize}")
        else:
            print(" Filter discarded.")

    def apply_gaussian_filter(self):
        self.capture_current_frame()
        app = GaussianFilterApp(self.current_image_path)
        app.run()
        if app.save_filter and app.filtered_image is not None:
            cv2.imwrite(self.current_image_path, app.filtered_image)
            self.apply_gaussian = True
            self.gaussian_ksize = app.ksize
            self.gaussian_sigmaX = app.sigmaX
            print(f" Applied Gaussian Filter with ksize={app.ksize}, sigmaX={app.sigmaX}")
        else:
            print(" Gaussian filter not applied.")

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
            print(f" Applied Bilateral Filter (d={app.d}, sigmaColor={app.sigmaColor}, sigmaSpace={app.sigmaSpace})")
        else:
            print(" Bilateral filter not applied.")

    def apply_canny_edge(self):
        if self.canny_detector is None:
            self.canny_detector = CannyEdgeDetector()
        self.apply_canny = True
        print(" Live Canny Edge Detection Enabled.")
            
        
        
    def apply_failure_detection(self):
        self.failure_detection_flag = True
        
    def extract_images_from_stream(self):
        self.enable_screenshot = True
        
