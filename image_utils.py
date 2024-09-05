import cv2
from PIL import Image
import base64
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def capture_image_from_webcam(cap):
    success, frame = cap.read()
    if success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        logger.info("Image captured successfully from webcam")
        return pil_image
    else:
        logger.error("Failed to capture image from webcam")
        return None

def pil_to_base64(pil_image):
    try:
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logger.info("Image successfully converted to base64")
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        logger.error(f"Error converting image to base64: {e}")
        return None
