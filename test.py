import cv2

cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Example processing: just show it
    cv2.imshow("Pi Camera Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
