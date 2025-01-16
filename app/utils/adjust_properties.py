import cv2
import numpy as np


def adjust_image_properties(image, brightness, sharpness, contrast):
    # Adjust brightness
    if brightness > 50:
        image = cv2.convertScaleAbs(image, alpha=1, beta=(brightness - 50))
    elif brightness < 50:
        image = cv2.convertScaleAbs(image, alpha=1, beta=(brightness - 50))

    # Adjust sharpness
    if sharpness > 50:
        sharpness_filter = np.array([[-1, -1, -1], [-1, 9 + (sharpness - 50), -1], [-1, -1, -1]])
        image = cv2.filter2D(image, -1, sharpness_filter)
    elif sharpness < 50:
        sharpness_filter = np.array([[1, 1, 1], [1, 9 - (50 - sharpness), 1], [1, 1, 1]])
        image = cv2.filter2D(image, -1, sharpness_filter)

    # Adjust contrast
    if contrast > 50:
        image = cv2.convertScaleAbs(image, alpha=(contrast / 50), beta=0)
    elif contrast < 50:
        image = cv2.convertScaleAbs(image, alpha=(contrast / 50), beta=0)

    return image