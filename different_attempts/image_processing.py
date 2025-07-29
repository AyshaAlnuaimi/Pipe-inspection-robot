import cv2

# Load image
image = cv2.imread("camera_reading/photo_1.jpg")
if image is None:
    print("Failed to load image.")
    exit()

# Convert to grayscale first
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply CLAHE (adaptive contrast enhancement)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
enhanced_gray = clahe.apply(gray)

# Apply Canny edge detection
edges = cv2.Canny(enhanced_gray, 50, 150)

# Resize for display
target_width = 800
scale = target_width / image.shape[1]
resized_orig = cv2.resize(image, (target_width, int(image.shape[0] * scale)))
resized_edges = cv2.resize(edges, (target_width, int(edges.shape[0] * scale)))

# Show
cv2.imshow("Original Image", resized_orig)
cv2.imshow("CLAHE + Canny", resized_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(picam2.capture_metadata())  # Shows actual resolution and settings

