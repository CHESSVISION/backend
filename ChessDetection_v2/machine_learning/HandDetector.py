from ChessDetection_v2.machine_learning.MachineLearning import MachineLearning
from config import settings
import cv2
import numpy as np


def is_found_navy_blue(image, pixel_threshold=500):
    """
    Detects if the specified dark navy-blue color (e.g., watch strap color)
    is present in the image.

    Parameters:
        image (numpy.ndarray): Input image in BGR color space.
        pixel_threshold (int): Minimum number of matching pixels required
                               to return True.

    Returns:
        bool: True if the navy-blue pixels exceed the threshold, False otherwise.
    """
    # Convert from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # ---------------------------------------------------
    #   Adjust these values as needed for your image
    # ---------------------------------------------------
    # Approx. range for dark navy-blue in HSV
    # H ranges from 0 to 179 in OpenCV
    # S, V range from 0 to 255
    lower_navy = np.array([90, 50, 20], dtype=np.uint8)
    upper_navy = np.array([120, 255, 120], dtype=np.uint8)

    # Create a mask where pixels in the range are white, else black
    mask = cv2.inRange(hsv_image, lower_navy, upper_navy)

    # Morphological operations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    # Count the number of non-zero pixels (i.e., pixels within the navy range)
    navy_pixels = cv2.countNonZero(mask)

    # Debug print
    print(f"Detected navy-blue pixels: {navy_pixels}")

    # Check if it exceeds the given threshold
    #
    # hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv_image, lower_navy, upper_navy)
    # cv2.imshow("Original", image)
    # cv2.imshow("Navy Mask", mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return navy_pixels > pixel_threshold


if __name__ == '__main__':
    # Load your image
    image = cv2.imread('chess_watch.jpg')  # <-- Replace with your actual filename
    if image is None:
        print("Error: Image not found or unable to load.")
    else:
        if is_found_navy_blue(image):
            print("Navy-blue watch strap color detected!")
        else:
            print("Navy-blue watch strap color NOT detected.")


class HandDetector(MachineLearning):

    def __init__(self):
        super().__init__(settings.hand_detector_model)

    def found_hand_detected(self, image):
        return is_found_navy_blue(image)

    # def found_hand_detected(self, image):
    #     self.set_image(image)
    #     return self.get_detections().xyxy.size != 0


hand_detector = HandDetector()
