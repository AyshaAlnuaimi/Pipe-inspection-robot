import tkinter as tk
import cv2
    
    
from vid_noise_reduction2 import NoiseReductionApp

    
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
        tk.Label(self.main_menu, text="Press 's' to save or 'i' to ignor the change").pack()        
     

        tk.Button(self.main_menu, text="Median filter", command=self.logic.apply_median_filter).pack()
        tk.Button(self.main_menu, text="Bilateral filter",  command=self.logic.apply_bilateral_filter).pack()
        tk.Button(self.main_menu, text="Gaussian filter",  command=self.logic.apply_gaussian_filter).pack()
        tk.Button(self.main_menu, text="Reset image",  command=self.logic.reset_image).pack()
        tk.Button(self.main_menu, text="Next", command=self.edge_detection_menu).pack()

    def edge_detection_menu(self):
        self.clear_main_menu()
        tk.Label(self.main_menu, text="Choose one Edge detection").pack()

        # tk.Button(self.main_menu, text="Canny edge detection", command=self.logic.apply_canny_edge).pack()
        tk.Button(self.main_menu, text="Canny edge detection",  command=self.logic.apply_canny_edge).pack()
        tk.Button(self.main_menu, text="Sobel edge detection",  command=self.logic.apply_sobel_edge).pack()
        tk.Button(self.main_menu, text="LoG edge detection",  command=self.logic.apply_log_edge).pack()

        # tk.Button(self.main_menu, text="Laplacian edge detection").pack()
        # tk.Button(self.main_menu, text="Sobel edge detection").pack()
        tk.Button(self.main_menu, text="Back", command=self.filter_menu).pack()
        tk.Button(self.main_menu, text="Next", command=self.take_screenshot).pack()

    def take_screenshot(self):
        self.clear_main_menu()
        #tk.Label(self.main_menu, text="Press start to start taking photos").pack()
        #tk.Button(self.main_menu, text="Start", command=self.logic.extract_images_from_stream).pack()
        tk.Button(self.main_menu, text="Start", command=self.logic.apply_failure_detection).pack()
        tk.Button(self.main_menu, text="Back", command=self.edge_detection_menu).pack()
        
    
# Run the app
GUI()
