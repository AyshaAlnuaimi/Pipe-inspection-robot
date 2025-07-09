# https://www.pythonguis.com/tutorials/create-buttons-in-tkinter/

import tkinter as tk
from PIL import Image, ImageTk  # <-- Import Pillow

root = tk.Tk()
root.title("Noise Reduction Techniques")

image_path = r"C:\Users\User\Desktop\screenshot_video_streaming.png"

# Load JPG image using PIL
pil_image = Image.open(image_path)
image = ImageTk.PhotoImage(pil_image)

def turn_tv_on():
    window = tk.Toplevel(root)
    window.title("TV")
    original_image = tk.Label(window, image=image)
    original_image.image = image  # Prevent garbage collection
    original_image.pack()

def Median_Filtering_button():
    print("Median Filtering")

def Bilateral_Filtering_button():
    print("Bilateral Filtering")

def Gaussian_Filtering_button():
    print("Gaussian Filtering")

def Wavelet_Denoising_button():
    print("Wavelet Denoising")

def Non_Local_Means_Denoising_button():
    print("Non-Local Means Denoising")

# UI Label
volume = tk.Label(root, text="Choose Technique for Noise reduction:")
volume.pack(pady=10)

# Buttons
btn_median = tk.Button(root, text="Median Filtering", command=Median_Filtering_button)
# in command make it for exmaple command=turn_tv_on it will display the image when button pressed
btn_median.pack(pady=5)


btn_bilateral = tk.Button(root, text="Bilateral Filtering", command=Bilateral_Filtering_button)
btn_bilateral.pack(pady=5)

btn_gaussian = tk.Button(root, text="Gaussian Filtering", command=Gaussian_Filtering_button)
btn_gaussian.pack(pady=5)

btn_wavelet = tk.Button(root, text="Wavelet Denoising", command=Wavelet_Denoising_button)
btn_wavelet.pack(pady=5)

btn_nlm = tk.Button(root, text="Non-Local Means Denoising", command=Non_Local_Means_Denoising_button)
btn_nlm.pack(pady=5)

# Optionally show the image in a separate window
# turn_tv_on()

root.mainloop()
