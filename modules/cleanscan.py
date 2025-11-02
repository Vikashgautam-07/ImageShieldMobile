import cv2
import os

def blur_faces(image_path, output_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        blurred = cv2.GaussianBlur(face, (99, 99), 30)
        image[y:y+h, x:x+w] = blurred

    cv2.imwrite(output_path, image)
    return output_path, len(faces)