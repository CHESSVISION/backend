import cv2
import numpy as np

# Define the lower and upper HSV boundaries for "navy" color
lower_navy = np.array([90, 50, 20], dtype=np.uint8)
upper_navy = np.array([120, 255, 120], dtype=np.uint8)

# Convert each HSV value to BGR for display.
# OpenCV's cvtColor requires an image, so we create a 1x1 image with the HSV value.
lower_bgr = cv2.cvtColor(np.uint8([[lower_navy]]), cv2.COLOR_HSV2BGR)[0][0]
upper_bgr = cv2.cvtColor(np.uint8([[upper_navy]]), cv2.COLOR_HSV2BGR)[0][0]

print("Lower navy (BGR):", lower_bgr)
print("Upper navy (BGR):", upper_bgr)

# Create images (100x100 pixels) filled with the converted colors.
img_lower = np.full((100, 100, 3), lower_bgr, dtype=np.uint8)
img_upper = np.full((100, 100, 3), upper_bgr, dtype=np.uint8)

# Display the images in separate windows.
cv2.imshow("Lower Navy Color", img_lower)
cv2.imshow("Upper Navy Color", img_upper)

cv2.waitKey(0)
cv2.destroyAllWindows()
