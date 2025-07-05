# https://stackoverflow.com/questions/67865452/the-problem-of-using-opencv-to-do-crack-detection

# import cv2 as cv
# import numpy as np

# src = cv.imread("canny_edge_result.png")
# cv.imshow("input", src)

# gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

# se = cv.getStructuringElement(cv.MORPH_RECT, (10, 10), (-1, -1))
# binary = cv.morphologyEx(binary, cv.MORPH_OPEN, se)
# cv.imshow("binary", binary)

# contours,hierachy=cv.findContours(binary,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
# height, width = src.shape[:2]
# for c in range(len(contours)):
#     x, y, w, h = cv.boundingRect(contours[c])
#     area = cv.contourArea(contours[c])
#     if h > (height//2):
#         continue
#     if area < 150:
#         continue
#     cv.rectangle(src, (x, y), (x+w, y+h), (0, 0, 255), 1, 8, 0)
#     cv.drawContours(src, contours, c, (0, 255, 0), 1, 8)

# cv.imshow("result", src)
# cv.imwrite("result.jpg", src)

# cv.waitKey(0)
# cv.destroyAllWindows()
import cv2
import numpy as np

# Load image
image = cv2.imread("Screenshot.png")
if image is None:
    print("[ERROR] Could not load image.")
    exit()

# Convert to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define fixed HSV range for crack-like regions
# NOTE: You may need to tweak these values based on your image
lower = np.array([0, 0, 30])     # low hue, low saturation, dark value
upper = np.array([180, 60, 120]) # full hue range, low saturation, mid-dark value

# Create mask
mask = cv2.inRange(hsv, lower, upper)

# Apply mask to original image
result = cv2.bitwise_and(image, image, mask=mask)

# Show outputs
cv2.imshow("Original", image)
cv2.imshow("Crack Mask", mask)
cv2.imshow("Detected Crack", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
