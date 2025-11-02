import cv2
import numpy as np

def apply_noiseguard(image_path, output_path, mode="pixelate", intensity=10):
    image = cv2.imread(image_path)

    if mode == "pixelate":
        h, w = image.shape[:2]
        temp = cv2.resize(image, (w // intensity, h // intensity), interpolation=cv2.INTER_LINEAR)
        result = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

    elif mode == "blur":
        k = intensity if intensity % 2 == 1 else intensity + 1
        result = cv2.GaussianBlur(image, (k, k), 0)

    elif mode == "noise":
        noise = np.random.normal(0, intensity, image.shape).astype(np.uint8)
        result = cv2.add(image, noise)

    else:
        result = image

    cv2.imwrite(output_path, result)
    return output_path, mode