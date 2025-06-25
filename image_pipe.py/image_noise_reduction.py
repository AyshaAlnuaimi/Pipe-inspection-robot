import numpy as np
import cv2
from PIL import Image


def median_filtering(pil_img):
    print("Applying Median Filter")
    img_np = np.array(pil_img)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    dst = cv2.medianBlur(img_np, 5)
    dst_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    return Image.fromarray(dst_rgb)


def bilateral_filtering(pil_img):
    print("Applying Bilateral Filter")

    # Convert PIL image to NumPy array
    img_np = np.array(pil_img)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Apply bilateral filter
    dst = cv2.bilateralFilter(img_np, d=9, sigmaColor=75, sigmaSpace=75)

    # Convert back to PIL image
    dst_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    filtered_pil = Image.fromarray(dst_rgb)

    return filtered_pil



def gaussian_filtering(pil_img):
    print("Gaussian Filtering - To Be Implemented")
    return pil_img


def wavelet_denoising(pil_img):
    print("Wavelet Denoising - To Be Implemented")
    return pil_img


def nlm_denoising(pil_img):
    print("Non-Local Means Denoising - To Be Implemented")
    return pil_img
