import cv2 as cv
import numpy as np

# https://stackoverflow.com/questions/67865452/the-problem-of-using-opencv-to-do-crack-detection


# Load the Canny edge image (single channel)
src = cv.imread("frame_0000.png", cv.IMREAD_GRAYSCALE)

# Optional: convert to color for visualization
vis = cv.cvtColor(src, cv.COLOR_GRAY2BGR)

# Find contours on binary edge map
contours, hierarchy = cv.findContours(src, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

height, width = src.shape[:2]
for c in contours:
    x, y, w, h = cv.boundingRect(c)
    area = cv.contourArea(c)
    if h > (height // 2):
        continue
    if area < 150:
        continue
    cv.rectangle(vis, (x, y), (x + w, y + h), (0, 0, 255), 1)
    cv.drawContours(vis, [c], -1, (0, 255, 0), 1)

# Show and save result
cv.imshow("result", vis)
cv.imwrite("result.jpg", vis)
cv.waitKey(0)
cv.destroyAllWindows()
