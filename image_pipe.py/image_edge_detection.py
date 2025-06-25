import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2

class EdgeDetection:
    def __init__(self, parent_root, pil_image, update_display_callback):
        self.root = tk.Toplevel(parent_root)
        self.root.title("Edge Detection")

        self.original_pil = pil_image
        self.gray_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
        self.update_display_callback = update_display_callback  # Function from MainPage to update image

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Choose Edge Detection:").pack(pady=10)

        tk.Button(self.root, text="Canny Edge", command=self.apply_canny_edge).pack(pady=5)
        # Add more edge detection options if needed

    def apply_canny_edge(self):
        print("Applying Canny Edge Detection")
        blurred = cv2.GaussianBlur(self.gray_image, (5, 5), 1.4)
        edges = cv2.Canny(blurred, 50, 150)

        # Convert back to PIL for display
        edge_pil = Image.fromarray(edges)
        self.update_display_callback(edge_pil, "Canny Edge Applied")
