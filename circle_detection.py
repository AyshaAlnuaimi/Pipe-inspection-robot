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

    # Apply Canny edge detection (optional if you meant "candy edge")
    edges = cv2.Canny(gray, 100, 200)

    # Optionally blur the grayscale image for HoughCircles
    gray_blurred = cv2.blur(gray, (3, 3))

    # Hough Circle Detection
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 20,
                                        param1=50, param2=30,
                                        minRadius=1, maxRadius=40)

    # Draw detected circles
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

    # Show the result
    cv2.imshow("Detected Circles", frame)
    # Optional: show Canny edge result
    # cv2.imshow("Canny Edge", edges)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
