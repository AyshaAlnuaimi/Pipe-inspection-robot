import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading


class NoiseReductionTechnique:
    def __init__(self, image_path):
        self.image_path = image_path
        self.original_img = cv2.imread(self.image_path)
        self.original_gray = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.window = "Noise Reduction"
        self.setup_parameters()
        self.build_gui()

    def setup_parameters(self):
        self.ksize = 5
        self.max_ksize = 31

        self.d = 1
        self.max_d = 15

        self.sigmaColor = 1
        self.max_sigmaColor = 200

        self.sigmaSpace = 1
        self.max_sigmaSpace = 200

        self.gaussian_filtering_ksize = 5
        self.sigmaX = 1.5

        self.wavelet_levels = 2

        self.h = 10
        self.hColor = 10
        self.templateWindowSize = 7
        self.searchWindowSize = 21

    def run_in_thread(self, target):
        threading.Thread(target=target, daemon=True).start()

    def show_image(self, image):
        cv2.imshow(self.window, image)

    def median_filtering(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)
        cv2.createTrackbar("ksize", self.window, self.ksize, self.max_ksize, self.update_median)

    def update_median(self, val=None):
        k = cv2.getTrackbarPos("ksize", self.window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        filtered = cv2.medianBlur(self.original_img, k)
        self.show_image(filtered)

    def bilateral_filtering(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)
        cv2.createTrackbar("d", self.window, self.d, self.max_d, self.update_bilateral)
        cv2.createTrackbar("sigmaColor", self.window, self.sigmaColor, self.max_sigmaColor, self.update_bilateral)
        cv2.createTrackbar("sigmaSpace", self.window, self.sigmaSpace, self.max_sigmaSpace, self.update_bilateral)

    def update_bilateral(self, val=None):
        d = cv2.getTrackbarPos("d", self.window)
        sigmaColor = cv2.getTrackbarPos("sigmaColor", self.window)
        sigmaSpace = cv2.getTrackbarPos("sigmaSpace", self.window)
        if d < 1: d = 1
        filtered = cv2.bilateralFilter(self.original_img, d, sigmaColor, sigmaSpace)
        self.show_image(filtered)

    def gaussian_filtering(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)
        cv2.createTrackbar("ksize", self.window, self.ksize, 31, self.update_gaussian)
        cv2.createTrackbar("sigmaX", self.window, int(self.sigmaX * 10), 100, self.update_gaussian)

    def update_gaussian(self, val=None):
        k = cv2.getTrackbarPos("ksize", self.window)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        sigma = cv2.getTrackbarPos("sigmaX", self.window)
        sigmaX = sigma / 10.0
        filtered = cv2.GaussianBlur(self.original_img, (k, k), sigmaX)
        self.show_image(filtered)

    def wavelet_filtering(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_gray)
        cv2.createTrackbar("Levels", self.window, self.wavelet_levels, 5, self.update_wavelet)

    def update_wavelet(self, val=None):
        levels = cv2.getTrackbarPos("Levels", self.window)
        if levels < 1:
            levels = 1
        if levels > 5:
            levels = 5
        denoised = self.wavelet_approx_denoising(self.original_gray, levels)
        self.show_image(denoised)

    def wavelet_approx_denoising(self, image, levels=2):
        gaussian_pyramid = [image]
        for i in range(levels):
            gaussian_pyramid.append(cv2.pyrDown(gaussian_pyramid[-1]))
        laplacian_pyramid = []
        for i in range(levels, 0, -1):
            upsampled = cv2.pyrUp(gaussian_pyramid[i])
            upsampled = cv2.resize(upsampled, (gaussian_pyramid[i-1].shape[1], gaussian_pyramid[i-1].shape[0]))
            laplacian = cv2.subtract(gaussian_pyramid[i-1], upsampled)
            laplacian_pyramid.append(laplacian)
        threshold = np.sqrt(2 * np.log(image.size))
        denoised_laplacian_pyramid = [cv2.threshold(l, threshold, 255, cv2.THRESH_TOZERO)[1] for l in laplacian_pyramid]
        reconstructed = gaussian_pyramid[-1]
        for i in range(levels-1, -1, -1):
            upsampled = cv2.pyrUp(reconstructed)
            upsampled = cv2.resize(upsampled, (denoised_laplacian_pyramid[i].shape[1], denoised_laplacian_pyramid[i].shape[0]))
            reconstructed = cv2.add(upsampled, denoised_laplacian_pyramid[i])
        return np.clip(reconstructed, 0, 255).astype(np.uint8)

    def non_local_means_filtering(self):
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window, 800, 600)
        cv2.imshow(self.window, self.original_img)
        cv2.createTrackbar("h", self.window, self.h, 50, self.update_nlm)
        cv2.createTrackbar("hColor", self.window, self.hColor, 50, self.update_nlm)
        cv2.createTrackbar("templateWindowSize", self.window, self.templateWindowSize, 21, self.update_nlm)
        cv2.createTrackbar("searchWindowSize", self.window, self.searchWindowSize, 35, self.update_nlm)

    def update_nlm(self, val=None):
        h = cv2.getTrackbarPos("h", self.window)
        hColor = cv2.getTrackbarPos("hColor", self.window)
        templateWindowSize = cv2.getTrackbarPos("templateWindowSize", self.window)
        searchWindowSize = cv2.getTrackbarPos("searchWindowSize", self.window)
        if templateWindowSize % 2 == 0: templateWindowSize += 1
        if searchWindowSize % 2 == 0: searchWindowSize += 1
        if templateWindowSize < 3: templateWindowSize = 3
        if searchWindowSize < 7: searchWindowSize = 7
        filtered = cv2.fastNlMeansDenoisingColored(self.original_img, None, h, hColor, templateWindowSize, searchWindowSize)
        self.show_image(filtered)

    def build_gui(self):
        self.root = tk.Tk()
        self.root.title("Noise Reduction GUI")
        ttk.Label(self.root, text="Select Filtering Method").pack(pady=10)

        ttk.Button(self.root, text="Median Filtering", command=lambda: self.run_in_thread(self.median_filtering)).pack(pady=5)
        ttk.Button(self.root, text="Bilateral Filtering", command=lambda: self.run_in_thread(self.bilateral_filtering)).pack(pady=5)
        ttk.Button(self.root, text="Gaussian Filtering", command=lambda: self.run_in_thread(self.gaussian_filtering)).pack(pady=5)
        ttk.Button(self.root, text="Wavelet Denoising", command=lambda: self.run_in_thread(self.wavelet_filtering)).pack(pady=5)
        ttk.Button(self.root, text="Non-Local Means Denoising", command=lambda: self.run_in_thread(self.non_local_means_filtering)).pack(pady=5)

        self.root.mainloop()

# Replace with your actual image path when running locally
app = NoiseReductionTechnique(r"C:\Users\Aysha.Alnuaimi\Downloads\inpipe_image.jpg")
