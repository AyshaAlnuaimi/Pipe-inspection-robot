import cv2

cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    # Apply Canny Edge Detection
    edges = cv2.Canny(frame, threshold1=50, threshold2=150)

    # Example processing: just show it
    cv2.imshow("Original Stream", frame)
    cv2.imshow("grayscale", gray)
    cv2.imshow("Canny Edges", edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
