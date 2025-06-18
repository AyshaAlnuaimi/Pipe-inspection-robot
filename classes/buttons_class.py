import tkinter as tk
from PIL import Image, ImageTk
import threading


# main.py

from median_fltr_class import MedianFilterApp
from bilateral_fltr_class import BilateralFilterApp
from gaussian_fltr import GaussianFilterApp
from non_local_means_class import NonLocalMeansFilterApp


class NoiseReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noise Reduction Techniques")
        self.image_path = r"C:\Users\User\Desktop\screenshot_video_streaming.png"
        self.pil_image = Image.open(self.image_path)
        self.image = ImageTk.PhotoImage(self.pil_image)

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Choose Technique for Noise reduction:").pack(pady=10)

        tk.Button(self.root, text="Median Filtering", command=self.median_filtering).pack(pady=5)
        tk.Button(self.root, text="Bilateral Filtering", command=self.bilateral_filtering).pack(pady=5)
        tk.Button(self.root, text="Gaussian Filtering", command=self.gaussian_filtering).pack(pady=5)
        tk.Button(self.root, text="Wavelet Denoising", command=self.wavelet_denoising).pack(pady=5)
        tk.Button(self.root, text="Non-Local Means Denoising", command=self.nlm_denoising).pack(pady=5)

    def show_image_window(self, title="Filtered Image"):
        window = tk.Toplevel(self.root)
        window.title(title)
        image_label = tk.Label(window, image=self.image)
        image_label.image = self.image  # Keep reference
        image_label.pack()

    # --- Filter Method Callbacks (Placeholders for now) ---
    def median_filtering(self):
        print("Launching Median Filter App")
        app = MedianFilterApp(self.image_path)
        app.run()


    def bilateral_filtering(self):
        print("Bilateral Filtering")
        # threading.Thread(target=self.show_image_window, args=("Bilateral Filtered Image",), daemon=True).start()
        app = BilateralFilterApp(self.image_path)
        app.run()


    def gaussian_filtering(self):
        print("Gaussian Filtering")
        # threading.Thread(target=self.show_image_window, args=("Gaussian Filtered Image",), daemon=True).start()
        app = GaussianFilterApp(self.image_path)
        app.run()

    def wavelet_denoising(self):
        print("Wavelet Denoising")
        threading.Thread(target=self.show_image_window, args=("Wavelet Denoised Image",), daemon=True).start()

    def nlm_denoising(self):
        print("Non-Local Means Denoising")
        # threading.Thread(target=self.show_image_window, args=("NLM Denoised Image",), daemon=True).start()
        app = NonLocalMeansFilterApp(self.image_path)
        app.run()

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = NoiseReductionApp(root)
    root.mainloop()
