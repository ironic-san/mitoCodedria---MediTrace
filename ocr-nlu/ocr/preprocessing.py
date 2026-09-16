import cv2
import numpy as np


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Prepare an image for OCR.
    """

    if image is None:
        raise ValueError("Invalid image")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    denoised = cv2.GaussianBlur(
        gray,
        (3, 3),
        0,
    )

    # Adaptive thresholding
    thresholded = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )

    return thresholded