import tkinter as tk
import cv2
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

        # External dependencies (to be set later)
        self.cap = None
        self.root = None
        self.current_image_path = ""
        self.original_image_path = ""
        self.current_frame = None


    def show_video_stream(self):
        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                #if any if the filters applied
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

    # def apply_canny_edge(self):
    #     print("[INFO] Skipping noise reduction. Enabling Canny Edge Detection...")
    #     self.apply_canny = True
    #     self.canny_detector = CannyEdgeDetector()
    
    
    
    
class GUI:

    def __init__(self):
        self.main_menu = tk.Tk()
        self.main_menu.minsize(300, 150)
        self.main_menu.title("Computer Vision")
        # Set up video capture
        self.cap = None
        self.cap = cv2.VideoCapture("http://192.168.3.5:8000/video")
        self.current_frame = None
        self.current_image_path = "captured_frame.png"
        self.original_image_path = "original_frame.png"

        # Create one instance of NoiseReductionApp
        self.logic = NoiseReductionApp(self.main_menu)
        self.logic.cap = self.cap  # share video stream with logic
        self.logic.root = self.main_menu  # allow logic to manipulate the GUI
        self.logic.current_image_path = self.current_image_path
        self.logic.original_image_path = self.original_image_path

        # Start video streaming (if desired)
        self.logic.show_video_stream()
  
        # Launch the filter selection menu
        self.filter_menu()

        self.main_menu.mainloop()


    def clear_main_menu(self):
        for widget in self.main_menu.winfo_children():
            widget.destroy()

    def filter_menu(self):
        self.clear_main_menu()
        tk.Label(self.main_menu, text="Choose one Noise reduction Technique").pack()        

        tk.Button(self.main_menu, text="Median filter", command=self.logic.apply_median_filter).pack()
        tk.Button(self.main_menu, text="Bilateral filter",  command=self.logic.apply_bilateral_filter).pack()
        tk.Button(self.main_menu, text="Gaussian filter",  command=self.logic.apply_gaussian_filter).pack()
        tk.Button(self.main_menu, text="Reset image",  command=self.logic.reset_image).pack()
        tk.Button(self.main_menu, text="Next", command=self.edge_detection_menu).pack()

    def edge_detection_menu(self):
        self.clear_main_menu()
        tk.Label(self.main_menu, text="Choose one Edge detection").pack()

        # tk.Button(self.main_menu, text="Canny edge detection", command=self.logic.apply_canny_edge).pack()
        tk.Button(self.main_menu, text="Canny edge detection").pack()
        tk.Button(self.main_menu, text="Laplacian edge detection").pack()
        tk.Button(self.main_menu, text="Sobel edge detection").pack()
        tk.Button(self.main_menu, text="Back", command=self.filter_menu).pack()
        tk.Button(self.main_menu, text="Next", command=self.failure_detection).pack()

    def failure_detection(self):
        self.clear_main_menu()
        tk.Label(self.main_menu, text="Failure detection running...").pack()
        tk.Button(self.main_menu, text="Back", command=self.edge_detection_menu).pack()

# Run the app
GUI()
