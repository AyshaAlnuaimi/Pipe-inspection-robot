# import cv2
# import numpy as np

# # I got the code for the trackbar from this youtube link
# #https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# #https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py
# #brightness im + offset
# #contrast   im*contrast
# #im *contrast + brightness
# image_path = r"C:\Users\Aysha.Alnuaimi\Downloads\inpipe_image.jpg"
# img = cv2.imread(image_path)
# im = np.float32(img/255)

# window = 'Noise reduction'
# contrast = 10
# max_contrast = 100
# brightness = 0
# max_brightness = 100

# def change_contrast(val):
# 	global contrast
# 	contrast = val/10
# 	perform_operation()

# def change_brightness(val):
# 	global brightness 
# 	brightness = val/100
# 	perform_operation()

# def perform_operation():
# 	im1 = im*contrast + brightness
# 	cv2.imshow(window, im1)

# # Allow resizing
# cv2.namedWindow(window, cv2.WINDOW_NORMAL)
# cv2.resizeWindow(window, 800, 600)  # Resize to 800x600

# cv2.imshow(window, im)
# cv2.createTrackbar("Contrast", window, contrast, max_contrast, change_contrast)
# cv2.createTrackbar("Brightness", window, brightness, max_brightness, change_brightness)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


#Image prossing
#Noise reduction
# - Mean f iltering 
#----------------------------------
# Median filtering 

# I got this code from this source: 
# https://www.geeksforgeeks.org/computer-vision/noise-removing-technique-in-computer-vision/
# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
# import requests
# from PIL import Image
# from io import BytesIO


# # Open the image using PIL
# img = Image.open(BytesIO(img_data))

# # Convert the PIL image to a numpy array
# img = np.array(img)

# # If the image is in RGB, no need for conversion, else convert from BGR to RGB
# if img.shape[2] == 3:  # Check if it's RGB
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # Removing noise in the image using Median Filtering
# dst = cv2.medianBlur(img, 5)  # 5 is the kernel size (must be an odd number)

# # Plotting the source and destination images
# plt.figure(figsize=(12, 6))
# plt.subplot(121), plt.imshow(img), plt.title('Original Image')
# plt.subplot(122), plt.imshow(dst), plt.title('Denoised Image (Median Filter)')
# plt.show()
#----------------------------------

# Bilateral filtering:

# I got this code from this source: 
# https://www.geeksforgeeks.org/computer-vision/noise-removing-technique-in-computer-vision/

# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
# import requests
# from PIL import Image
# from io import BytesIO

# # Image URL
# url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmKTFI_7r2TKR0sknfK_7GJX8sHItxbf-zh_jOJIBde2-L69K29IAzFLrD&s"

# # Fetch the image from the URL
# response = requests.get(url)
# img_data = response.content

# # Open the image using PIL
# img = Image.open(BytesIO(img_data))

# # Convert the PIL image to a numpy array
# img = np.array(img)

# # If the image is in RGB, no need for conversion, else convert from BGR to RGB
# if img.shape[2] == 3:  # Check if it's RGB
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # Removing noise in the image using Bilateral Filtering
# dst = cv2.bilateralFilter(img, 9, 75, 75)  # Parameters: d, sigmaColor, sigmaSpace

# # Plotting the source and destination images
# plt.figure(figsize=(12, 6))
# plt.subplot(121), plt.imshow(img), plt.title('Original Image')
# plt.subplot(122), plt.imshow(dst), plt.title('Denoised Image (Bilateral Filter)')
# plt.show()
 
 
#-------------------------------------------------------
# - domain filtering 
#Contrast enhancement
#Color space conversion


#------------------------------
import cv2
import numpy as np

# I got the code for the trackbar from this youtube link
# https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py

image_path = r"C:\Users\Aysha.Alnuaimi\Downloads\inpipe_image.jpg"
img = cv2.imread(image_path)
original_img = img.copy()  # To keep the original safe
print("Image shape:", original_img.shape)


ksize = 5
max_ksize = 31

d = 1
max_d = 15

sigmaColor = 1
max_sigmaColor = 200

sigmaSpace = 1
max_sigmaSpace = 200

gaussian_filtering_ksize = 5
sigmaX = 1.5

wavelet_levels = 2
window = "Noise reduction"
original_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Must be grayscale

h = 10
hColor = 10
templateWindowSize = 7
searchWindowSize = 21

# def median_filtering(val):
#     global ksize
#     k = cv2.getTrackbarPos("ksize", window)
#     if k % 2 == 0:
#         k += 1
#     if k < 1:
#         k = 1
#     ksize = k
#     filtered = cv2.medianBlur(original_img, ksize)
#     cv2.imshow(window, filtered)

# def bilateral_filtering(val=None):
#     global d, sigmaColor, sigmaSpace
#     d = cv2.getTrackbarPos("d", window)
#     if d < 1:
#         d = 1
#     sigmaColor = cv2.getTrackbarPos("sigmaColor", window)
#     sigmaSpace = cv2.getTrackbarPos("sigmaSpace", window)
#     filtered = cv2.bilateralFilter(original_img, d, sigmaColor, sigmaSpace)
#     cv2.imshow(window, filtered)

# def gaussian_filtering(val=None):
#     global gaussian_filtering_ksize, sigmaX

#     #  Read current values from trackbars
#     k = cv2.getTrackbarPos("ksize", window)
#     if k % 2 == 0:
#         k += 1
#     if k < 1:
#         k = 1
#     gaussian_filtering_ksize = k

#     sigma = cv2.getTrackbarPos("sigmaX", window)
#     sigmaX = sigma / 10.0  # Convert to float, e.g., 25 → 2.5

#     filtered = cv2.GaussianBlur(original_img, (gaussian_filtering_ksize, gaussian_filtering_ksize), sigmaX)
#     cv2.imshow(window, filtered)

# def wavelet_approx_denoising(image, levels=2):
#     # Create Gaussian pyramid
#     gaussian_pyramid = [image]
#     for i in range(levels):
#         gaussian_pyramid.append(cv2.pyrDown(gaussian_pyramid[-1]))

#     # Create Laplacian pyramid
#     laplacian_pyramid = []
#     for i in range(levels, 0, -1):
#         upsampled = cv2.pyrUp(gaussian_pyramid[i])
#         upsampled = cv2.resize(upsampled, (gaussian_pyramid[i-1].shape[1], gaussian_pyramid[i-1].shape[0]))
#         laplacian = cv2.subtract(gaussian_pyramid[i-1], upsampled)
#         laplacian_pyramid.append(laplacian)

#     # Apply thresholding to reduce noise
#     threshold = np.sqrt(2 * np.log(image.size))
#     denoised_laplacian_pyramid = [cv2.threshold(l, threshold, 255, cv2.THRESH_TOZERO)[1] for l in laplacian_pyramid]

#     # Reconstruct
#     reconstructed = gaussian_pyramid[-1]
#     for i in range(levels-1, -1, -1):
#         upsampled = cv2.pyrUp(reconstructed)
#         upsampled = cv2.resize(upsampled, (denoised_laplacian_pyramid[i].shape[1], denoised_laplacian_pyramid[i].shape[0]))
#         reconstructed = cv2.add(upsampled, denoised_laplacian_pyramid[i])

#     return np.clip(reconstructed, 0, 255).astype(np.uint8)

# def wavelet_filtering(val=None):
#     global wavelet_levels, original_gray

#     # Get current level from the trackbar
#     levels = cv2.getTrackbarPos("Levels", window)
#     if levels < 1:
#         levels = 1
#     if levels > 5:  # To prevent excessive downsampling
#         levels = 5
#     wavelet_levels = levels

#     # Apply wavelet-like denoising
#     denoised = wavelet_approx_denoising(original_gray, levels)
#     cv2.imshow(window, denoised)

def non_local_means_filtering(val=None):
    global h, hColor, templateWindowSize, searchWindowSize

    h = cv2.getTrackbarPos("h", window)
    hColor = cv2.getTrackbarPos("hColor", window)
    templateWindowSize = cv2.getTrackbarPos("templateWindowSize", window)
    searchWindowSize = cv2.getTrackbarPos("searchWindowSize", window)

    # Ensure odd and minimum values
    if templateWindowSize % 2 == 0: templateWindowSize += 1
    if searchWindowSize % 2 == 0: searchWindowSize += 1
    if templateWindowSize < 3: templateWindowSize = 3
    if searchWindowSize < 7: searchWindowSize = 7

    filtered = cv2.fastNlMeansDenoisingColored(original_img, None, h, hColor, templateWindowSize, searchWindowSize)
    cv2.imshow(window, filtered)



# Window setup
cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window, 800, 600)

# Initial image
cv2.imshow(window, original_img)

# Choose one method to test at a time:
# --- Median filter ---
# cv2.createTrackbar("ksize", window, ksize, max_ksize, median_filtering)

# --- Bilateral filter ---
# cv2.createTrackbar("d", window, d, max_d, bilateral_filtering)
# cv2.createTrackbar("sigmaColor", window, sigmaColor, max_sigmaColor, bilateral_filtering)
# cv2.createTrackbar("sigmaSpace", window, sigmaSpace, max_sigmaSpace, bilateral_filtering)

#---- Gaussian Filter ---
# cv2.createTrackbar("ksize", window, ksize, 31, gaussian_filtering)
# cv2.createTrackbar("sigmaX", window, int(sigmaX * 10), 100, gaussian_filtering)
# gaussian_filtering()

#---- Wavelet Denoising ---
# cv2.createTrackbar("Levels", window, wavelet_levels, 5, wavelet_filtering)
# wavelet_filtering()

# cv2.createTrackbar("h", window, h, 50, non_local_means_filtering)
# cv2.createTrackbar("hColor", window, hColor, 50, non_local_means_filtering)
# cv2.createTrackbar("templateWindowSize", window, templateWindowSize, 21, non_local_means_filtering)
# cv2.createTrackbar("searchWindowSize", window, searchWindowSize, 35, non_local_means_filtering)
# non_local_means_filtering()

cv2.waitKey(0)
cv2.destroyAllWindows()
