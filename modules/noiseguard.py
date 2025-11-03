import cv2
import numpy as np
from PIL import Image

def add_privacy_noise(pil_image, mode="pixelate", intensity=10):
    """
    Apply pixelation, noise, or blur filters for privacy.
    """
    img = np.array(pil_image)

    if mode == "pixelate":
        small = cv2.resize(img, (img.shape[1] // intensity, img.shape[0] // intensity))
        result = cv2.resize(small, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
    elif mode == "blur":
        k = intensity if intensity % 2 == 1 else intensity + 1
        result = cv2.GaussianBlur(img, (k, k), 0)
    elif mode == "noise":
        noise = np.random.randint(0, intensity, img.shape, dtype='uint8')
        result = cv2.add(img, noise)
    else:
        result = img

    return Image.fromarray(result)
