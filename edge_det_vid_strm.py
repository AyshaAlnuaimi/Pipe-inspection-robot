# import cv2
# import numpy as np

# # Open video stream
# cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

# # Sigma values to test
# sigma_values = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5]

# # Resize helper
# def resize(img, size=(300, 200)):
#     return cv2.resize(img, size)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray_eq = cv2.equalizeHist(gray)

#     processed_images = []

#     for sigma in sigma_values:
#         # Apply Gaussian blur
        
#         # Pseudo logic: kernel size based on sigma
#         ksize = int(6 * sigma + 1)
#         if ksize % 2 == 0:  # Ensure odd size
#             ksize += 1

#         blur = cv2.GaussianBlur(gray_eq, (ksize, ksize), sigma)
        
#         # Canny edge detection
#         edges = cv2.Canny(blur, 20, 60)

#         # Dilation (optional)
#         kernel = np.ones((2, 2), np.uint8)
#         edges_dilated = cv2.dilate(edges, kernel, iterations=1)

#         # Label and convert to BGR
#         label = f"σ = {sigma}"
#         labeled = cv2.putText(cv2.cvtColor(edges_dilated, cv2.COLOR_GRAY2BGR),
#                               label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
#                               0.7, (0, 255, 0), 2)

#         # Resize and store
#         resized = resize(labeled)
#         processed_images.append(resized)

#     # Layout in a 2-row grid
#     row1 = np.hstack(processed_images[:3])
#     row2 = np.hstack(processed_images[3:])

#     # Pad row2 if needed
#     if len(processed_images[3:]) < 3:
#         for _ in range(3 - len(processed_images[3:])):
#             blank = np.zeros_like(resized)
#             row2 = np.hstack([row2, blank])

#     final_grid = np.vstack([row1, row2])

#     # Show result
#     cv2.imshow("video streaming Sigma: [0.1, 0.5, 1.0, 1.5, 2.0, 2.5]", final_grid)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# #----------------------------------------------------------------------

# #the same as the top code but this with video
# import cv2
# import numpy as np

# cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

# # Resize helper
# def resize(img, size=(300, 200)):
#     return cv2.resize(img, size)

# # Generate a blank placeholder image
# def placeholder(text, size=(300, 200)):
#     blank = np.zeros((size[1], size[0], 3), dtype=np.uint8)
#     return cv2.putText(blank, text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray_eq = cv2.equalizeHist(gray)
#     output_images = []

#     # 1. Canny
#     canny = cv2.Canny(gray_eq, 50, 150)
#     canny_bgr = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
#     canny_bgr = cv2.putText(canny_bgr, "Canny", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
#     output_images.append(resize(canny_bgr))

#     # 2. Gradient-based (Sobel)
#     sobelx = cv2.Sobel(gray_eq, cv2.CV_64F, 1, 0, ksize=3)
#     sobely = cv2.Sobel(gray_eq, cv2.CV_64F, 0, 1, ksize=3)
#     sobel_combined = cv2.magnitude(sobelx, sobely)
#     sobel_combined = cv2.convertScaleAbs(sobel_combined)
#     sobel_bgr = cv2.cvtColor(sobel_combined, cv2.COLOR_GRAY2BGR)
#     sobel_bgr = cv2.putText(sobel_bgr, "Gradient (Sobel)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
#     output_images.append(resize(sobel_bgr))

#     # 3. Laplacian of Gaussian
#     blurred = cv2.GaussianBlur(gray_eq, (3, 3), 0.5)
#     laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
#     laplacian = cv2.convertScaleAbs(laplacian)
#     laplacian_bgr = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
#     laplacian_bgr = cv2.putText(laplacian_bgr, "Laplacian of Gaussian", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
#     output_images.append(resize(laplacian_bgr))

#     # 4. SIFT
#     try:
#         sift = cv2.SIFT_create()
#         kp = sift.detect(gray_eq, None)
#         sift_img = cv2.drawKeypoints(frame, kp, None)
#         sift_img = cv2.putText(sift_img, "SIFT", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
#         output_images.append(resize(sift_img))
#     except:
#         output_images.append(placeholder("SIFT Not Available"))

#     # 5. Harris Corner
#     harris = cv2.cornerHarris(np.float32(gray_eq), 2, 3, 0.04)
#     harris = cv2.dilate(harris, None)
#     harris_img = frame.copy()
#     harris_img[harris > 0.01 * harris.max()] = [0, 0, 255]
#     harris_img = cv2.putText(harris_img, "Harris Corner", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
#     output_images.append(resize(harris_img))

#     # 6. SURF
#     try:
#         surf = cv2.xfeatures2d.SURF_create(400)
#         kp_surf, _ = surf.detectAndCompute(gray_eq, None)
#         surf_img = cv2.drawKeypoints(frame, kp_surf, None)
#         surf_img = cv2.putText(surf_img, "SURF", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
#         output_images.append(resize(surf_img))
#     except:
#         output_images.append(placeholder("SURF Not Available"))

#     # Layout: 2 rows of 3
#     row1 = np.hstack(output_images[:3])
#     row2 = np.hstack(output_images[3:])
#     final_grid = np.vstack([row1, row2])

#     # Show result
#     cv2.imshow("video streaming: 1-canny, 2-Gradient-based (Sobel), 3-Laplacian of Gaussian, 4-SIFT, 5-Harris Corner, 6-SURF ", final_grid)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# #----------------------------------------------------------------------

import cv2
import numpy as np

# Open video stream
cap = cv2.VideoCapture("http://192.168.3.5:8000/video")

# Sigma values to test
sigma_values = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5]

# Resize helper
def resize(img, size=(300, 200)):
    return cv2.resize(img, size)

# Placeholder for unavailable features
def placeholder(text, size=(300, 200)):
    blank = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    return cv2.putText(blank, text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_eq = cv2.equalizeHist(gray)

    # # ----------- Window 1: Sigma Variation with Canny -----------
    # processed_sigma = []

    # for sigma in sigma_values:
    #     ksize = int(6 * sigma + 1)
    #     if ksize % 2 == 0:
    #         ksize += 1

    #     blur = cv2.GaussianBlur(gray_eq, (ksize, ksize), sigma)
    #     edges = cv2.Canny(blur, 20, 60)
    #     edges_dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)

    #     label = f"σ = {sigma}"
    #     labeled = cv2.putText(cv2.cvtColor(edges_dilated, cv2.COLOR_GRAY2BGR),
    #                           label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    #     processed_sigma.append(resize(labeled))

    # row1 = np.hstack(processed_sigma[:3])
    # row2 = np.hstack(processed_sigma[3:])
    # if len(processed_sigma[3:]) < 3:
    #     for _ in range(3 - len(processed_sigma[3:])):
    #         row2 = np.hstack([row2, np.zeros_like(processed_sigma[0])])
    # grid_sigma = np.vstack([row1, row2])

    # ----------- Window 2: Feature Detectors -----------
    feature_images = []

    # 1. Canny
    canny = cv2.Canny(gray_eq, 50, 150)
    canny_bgr = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    canny_bgr = cv2.putText(canny_bgr, "Canny", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    feature_images.append(resize(canny_bgr))

    # 2. Gradient-based (Sobel)
    sobelx = cv2.Sobel(gray_eq, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_eq, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = cv2.convertScaleAbs(cv2.magnitude(sobelx, sobely))
    sobel_bgr = cv2.cvtColor(sobel_combined, cv2.COLOR_GRAY2BGR)
    sobel_bgr = cv2.putText(sobel_bgr, "Gradient (Sobel)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    feature_images.append(resize(sobel_bgr))

    # 3. Laplacian of Gaussian
    lap_blur = cv2.GaussianBlur(gray_eq, (3, 3), 0.5)
    laplacian = cv2.convertScaleAbs(cv2.Laplacian(lap_blur, cv2.CV_64F))
    lap_bgr = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
    lap_bgr = cv2.putText(lap_bgr, "Laplacian of Gaussian", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    feature_images.append(resize(lap_bgr))

    # 4. SIFT
    try:
        sift = cv2.SIFT_create()
        kp = sift.detect(gray_eq, None)
        sift_img = cv2.drawKeypoints(frame, kp, None)
        sift_img = cv2.putText(sift_img, "SIFT", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        feature_images.append(resize(sift_img))
    except:
        feature_images.append(placeholder("SIFT Not Available"))

    # 5. Harris Corner
    harris = cv2.cornerHarris(np.float32(gray_eq), 2, 3, 0.04)
    harris = cv2.dilate(harris, None)
    harris_img = frame.copy()
    harris_img[harris > 0.01 * harris.max()] = [0, 0, 255]
    harris_img = cv2.putText(harris_img, "Harris Corner", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    feature_images.append(resize(harris_img))

    # 6. SURF
    try:
        surf = cv2.xfeatures2d.SURF_create(400)
        kp_surf, _ = surf.detectAndCompute(gray_eq, None)
        surf_img = cv2.drawKeypoints(frame, kp_surf, None)
        surf_img = cv2.putText(surf_img, "SURF", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        feature_images.append(resize(surf_img))
    except:
        feature_images.append(placeholder("SURF Not Available"))

    # Create 2-row layout
    feat_row1 = np.hstack(feature_images[:3])
    feat_row2 = np.hstack(feature_images[3:])
    grid_features = np.vstack([feat_row1, feat_row2])

    # ----------- Display Both Windows -----------
    # cv2.imshow("video streaming Sigma: " + str(sigma_values), grid_sigma)
    cv2.imshow("Feature Comparison: Canny, Sobel, LoG, SIFT, Harris, SURF", grid_features)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
