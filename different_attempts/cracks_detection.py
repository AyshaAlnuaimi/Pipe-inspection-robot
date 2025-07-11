
#I import this code from:
#https://github.com/shomnathsomu/crack-detection-opencv/blob/master/CrackDetection.py
#I did some modifications 

import numpy as np
import cv2

# Open video stream
cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization to enhance contrast
    equalized = cv2.equalizeHist(gray)

    # Apply Gaussian Blur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(equalized, (5, 5), 1.5)

    # Canny Edge Detection with adjusted thresholds
    edges = cv2.Canny(blurred, 30, 100)

    # Optional: Morphological closing to connect broken lines
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # ORB feature detection (to highlight possible crack areas)
    orb = cv2.ORB_create(nfeatures=1500)
    keypoints, descriptors = orb.detectAndCompute(closing, None)
    featuredImg = cv2.drawKeypoints(closing, keypoints, None)
    
    
    

    # Display windows
    cv2.imshow("Original", frame)
    cv2.imshow("Canny Edges", edges)
    cv2.imshow("Crack Detection", featuredImg)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
