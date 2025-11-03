import cv2
import numpy as np
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def remove_sensitive_content(pil_image):
    """
    Detect faces and blur them for privacy.
    Input: PIL Image
    Output: PIL Image with blurred faces
    """
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = img[y:y+h, x:x+w]
        face = cv2.GaussianBlur(face, (99, 99), 30)
        img[y:y+h, x:x+w] = face
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
