import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import shutil
from vid_median_fltr import MedianFilterApp
from vid_bilateral_fltr import BilateralFilterApp
from vid_gaussian_fltr import GaussianFilterApp
from vid_non_local_mean_fltr import NonLocalMeansFilterApp
from det_Canny_edge import CannyEdgeDetector


class NoiseReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noise Reduction Techniques")

        # Uncomment the next line to use live video stream instead of an image
        self.cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

        #for image
        # self.original_image_path = r"C:\Users\User\Desktop\screenshot_video_streaming.png"
        # self.processed_image_path = None
        # self.current_image_path = self.original_image_path

        # self.pil_image = Image.open(self.original_image_path)
        # self.image = ImageTk.PhotoImage(self.pil_image)

        # # Always show the original/processed image
        # cv2.imshow("Live Stream / Image", cv2.imread(self.current_image_path))

        # self.setup_ui()
    
    
    # ---------video -----------------  
        self.current_frame = None
        self.processed_image_path = None
        self.current_image_path = "captured_frame.png"

        self.show_video_stream()
        self.setup_ui()
        
    def show_video_stream(self):
        # Start reading frames in a separate loop
        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                cv2.imshow("Live Stream / Image", frame)
            self.root.after(30, update_frame)  # Schedule next update

        update_frame()

    def capture_current_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                cv2.imwrite(self.current_image_path, self.current_frame)
                print(f"[INFO] Frame captured to {self.current_image_path}")

    # --------------------------------  

    def setup_ui(self):
        self.clear_root()
        tk.Label(self.root, text="Choose Technique for Noise Reduction (Optional):").pack(pady=10)

        tk.Button(self.root, text="Median Filtering", command=self.median_filtering).pack(pady=5)
        tk.Button(self.root, text="Bilateral Filtering", command=self.bilateral_filtering).pack(pady=5)
        tk.Button(self.root, text="Gaussian Filtering", command=self.gaussian_filtering).pack(pady=5)
        tk.Button(self.root, text="Non-Local Means Denoising", command=self.nlm_denoising).pack(pady=5)
        tk.Button(self.root, text="Reset to Original", command=self.reset_image).pack(pady=5)
        tk.Button(self.root, text="Skip", command=self.go_to_image_detection).pack(pady=5)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def save_processed_image(self, image):
        path = "processed_image.png"
        cv2.imwrite(path, image)
        self.processed_image_path = path
        self.current_image_path = path
        print(f"Processed image saved to {path}")
        cv2.imshow("Live Stream / Image", image)  # Update displayed image

    def reset_image(self):
        self.current_image_path = self.original_image_path
        self.pil_image = Image.open(self.original_image_path)
        self.image = ImageTk.PhotoImage(self.pil_image)
        print("[INFO] Reset to original image.")
        cv2.imshow("Live Stream / Image", cv2.imread(self.original_image_path))


   #---------------image--------------------
    def median_filtering(self):
        print("Launching Median Filter App")
        app = MedianFilterApp(self.current_image_path)
        app.run()
        if hasattr(app, 'filtered_image') and app.filtered_image is not None:
            self.save_processed_image(app.filtered_image)

    def bilateral_filtering(self):
        print("Bilateral Filtering")
        app = BilateralFilterApp(self.current_image_path)
        app.run()
        if hasattr(app, 'filtered_image') and app.filtered_image is not None:
            self.save_processed_image(app.filtered_image)

    def gaussian_filtering(self):
        print("Gaussian Filtering")
        app = GaussianFilterApp(self.current_image_path)
        app.run()
        if hasattr(app, 'filtered_image') and app.filtered_image is not None:
            self.save_processed_image(app.filtered_image)

    def nlm_denoising(self):
        print("Non-Local Means Denoising")
        app = NonLocalMeansFilterApp(self.current_image_path)
        app.run()
        if hasattr(app, 'filtered_image') and app.filtered_image is not None:
            self.save_processed_image(app.filtered_image)
    #--------------------------------------------------------


    def canny_detection(self):
        self.capture_current_frame()  # Ensure latest frame is saved
        print("Running Canny edge detector")
        app = CannyEdgeDetector(self.current_image_path)
        app.run()

        if app.back_requested:
            # Restore previous image
            cv2.imshow("Live Stream / Image", cv2.imread(self.current_image_path))
            self.setup_ui()  # Go back to noise reduction options
        else:
            # Stay in detection screen or take other action
            print("[INFO] Canny completed.")

#-----------------------------------------------------------




    # def canny_detection(self):
    #     print("Running Canny edge detector")
    #     app = CannyEdgeDetector(self.current_image_path)
    #     app.run()

    #     if app.back_requested:
    #         # Restore previous image
    #         cv2.imshow("Live Stream / Image", cv2.imread(self.current_image_path))
    #         self.setup_ui()  # Go back to noise reduction options
    #     else:
    #         # Stay in detection screen or take other action
    #         print("[INFO] Canny completed.")
    
    def go_to_image_detection(self):
        self.clear_root()
        tk.Label(self.root, text="Choose Technique for Image Detection:").pack(pady=10)

        tk.Button(self.root, text="Canny edge detector", command=self.canny_detection, width=30).pack(pady=5)
        tk.Button(self.root, text="Gradient-based edge detector", command=lambda: print("Gradient-based edge detector"), width=30).pack(pady=5)
        tk.Button(self.root, text="Laplacian of Gaussian", command=lambda: print("Laplacian of Gaussian"), width=30).pack(pady=5)
        tk.Button(self.root, text="SIFT", command=lambda: print("SIFT"), width=30).pack(pady=5)
        tk.Button(self.root, text="Harris corner detector", command=lambda: print("Harris corner detector"), width=30).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.setup_ui, width=30).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = NoiseReductionApp(root)
    root.mainloop()
