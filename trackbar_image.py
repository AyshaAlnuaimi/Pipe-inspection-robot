# import cv2
# import numpy as np

# # I got the code for the trackbar from this youtube link
# #https://www.youtube.com/watch?v=lCKvzUKhcJo&t=7s
# #https://github.com/nickredsox/youtube/blob/master/DIP_CV/trackbar/trackbar.py
# #brightness im + offset
# #contrast   im*contrast
# #im *contrast + brightness
# image_path = r"C:\Users\User\Desktop\screenshot_video_streaming.png"
# img = cv2.imread(image_path)
# im = np.float32(img/255)

# window = 'Lilly'
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

# cv2.imshow(window, im)
# cv2.createTrackbar("Contrast", window, contrast, max_contrast, change_contrast)
# cv2.createTrackbar("Brightness", window, brightness, max_brightness, change_brightness)
# cv2.waitKey(0)


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




