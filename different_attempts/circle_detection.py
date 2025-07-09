# I imported this code from:
#     https://www.geeksforgeeks.org/python/circle-detection-using-opencv-python/
# i did some modifications on it

# import cv2
# import numpy as np

# # Open video stream
# cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     # Convert to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Apply Canny edge detection (optional if you meant "candy edge")
#     edges = cv2.Canny(gray, 100, 200)

#     # Optionally blur the grayscale image for HoughCircles
#     gray_blurred = cv2.blur(gray, (3, 3))

#     # Hough Circle Detection
#     detected_circles = cv2.HoughCircles(gray_blurred,
#                                         cv2.HOUGH_GRADIENT, 1, 20,
#                                         param1=50, param2=30,
#                                         minRadius=1, maxRadius=40)

#     # Draw detected circles
#     if detected_circles is not None:
#         detected_circles = np.uint16(np.around(detected_circles))
#         for pt in detected_circles[0, :]:
#             a, b, r = pt[0], pt[1], pt[2]
#             cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
#             cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

#     # Show the result
#     cv2.imshow("Detected Circles", frame)
#     # Optional: show Canny edge result
#     # cv2.imshow("Canny Edge", edges)

#     # Break loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Clean up
# cap.release()
# cv2.destroyAllWindows()



#https://stackoverflow.com/questions/60637120/detect-circles-in-opencv

import cv2
import numpy as np

# Open video stream
cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    blur = cv2.medianBlur(gray, 11)

    # Otsu's thresholding
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Morphological opening
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    # Find contours
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) > 5 and 1000 < area < 500000:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(frame, (int(x), int(y)), int(r), (36, 255, 12), 2)

    # Show windows
    cv2.imshow('Threshold', thresh)
    cv2.imshow('Opening', opening)
    cv2.imshow('Detected Circles', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
