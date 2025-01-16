import cv2
from fastapi import HTTPException

from utils.adjust_properties import adjust_image_properties


async def process_image(file_path: str, brightness: str, sharpness: str, contrast: str):
    """
    Converts an image to black and white.
    """
    image = cv2.imread(file_path)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    image = adjust_image_properties(image, int(brightness), int(sharpness), int(contrast))

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, encoded_image = cv2.imencode(".png", gray_image)

    return encoded_image
