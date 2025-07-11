
#I import this code from:
#https://github.com/shomnathsomu/crack-detection-opencv/blob/master/CrackDetection.py
#I did some modifications 
import numpy as np
import cv2

# Open video stream
cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

if not cap.isOpened():
    print("Failed to open video stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization to enhance contrast
    equalized = cv2.equalizeHist(gray)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(equalized, (5, 5), 1.5)

    # Canny Edge Detection
    edges = cv2.Canny(blurred, 30, 100)

    # Convert Canny edges to BGR so we can draw colored shapes
    vis = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Use edges for contour detection (not gray!)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    height, width = gray.shape[:2]
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if h > (height // 2):
            continue
        if area < 150:
            continue
        cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.drawContours(vis, [c], -1, (0, 255, 0), 1)

    # Show result
    cv2.imshow("Crack Detection", vis)

    # Save frame (optional, or save only on keypress)
    # cv2.imwrite("result.jpg", vis)

    # Break loop on key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
