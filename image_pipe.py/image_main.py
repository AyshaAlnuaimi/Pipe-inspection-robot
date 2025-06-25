import tkinter as tk
from PIL import Image, ImageTk
from image_noise_reduction import median_filtering, bilateral_filtering, gaussian_filtering, wavelet_denoising, nlm_denoising
from image_edge_detection import EdgeDetection



class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Pipe Image")
        self.image_path = r"C:\Users\User\Desktop\ChatGPTImage.png"

        self.original_image = Image.open(self.image_path)  # keep original
        self.pil_image = self.original_image.copy()        # working copy
        self.tk_image = ImageTk.PhotoImage(self.pil_image)

        self.image_window = None
        self.image_label = None

        self.setup_ui()
        self.show_image_window(title="Original Image", image=self.tk_image)

    def setup_ui(self):
        tk.Label(self.root, text="Choose Technique for Noise Reduction:").pack(pady=10)
        tk.Button(self.root, text="Median Filtering", command=lambda: self.apply_filter(median_filtering, "Median Filtered Image")).pack(pady=5)
        tk.Button(self.root, text="Bilateral Filtering", command=lambda: self.apply_filter(bilateral_filtering, "Bilateral Filtered Image")).pack(pady=5)
        tk.Button(self.root, text="Reset Image", command=self.reset_image).pack(pady=5)
        tk.Button(self.root, text="Next", command=self.go_to_edge_detection).pack(pady=10)


    def show_image_window(self, title="Filtered Image", image=None):
        if image is None:
            image = self.tk_image

        if self.image_window is None or not self.image_window.winfo_exists():
            self.image_window = tk.Toplevel(self.root)
            self.image_window.title(title)
            self.image_label = tk.Label(self.image_window, image=image)
            self.image_label.image = image
            self.image_label.pack()
        else:
            self.image_label.configure(image=image)
            self.image_label.image = image
            self.image_window.title(title)

    def apply_filter(self, filter_func, title):
        self.pil_image = filter_func(self.pil_image)
        filtered_tk = ImageTk.PhotoImage(self.pil_image)
        self.tk_image = filtered_tk  # update reference
        self.show_image_window(title=title, image=filtered_tk)

    def reset_image(self):
        print("Resetting to original image")
        self.pil_image = self.original_image.copy()
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
        self.show_image_window(title="Original Image", image=self.tk_image)
        
    def go_to_edge_detection(self):
        EdgeDetection(self.root, self.pil_image, self.update_image_display)

    def update_image_display(self, new_pil_image, title="Updated Image"):
        self.pil_image = new_pil_image
        self.tk_image = ImageTk.PhotoImage(new_pil_image)
        self.show_image_window(title=title, image=self.tk_image)



# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()
