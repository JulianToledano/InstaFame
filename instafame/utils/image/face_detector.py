import cv2
import numpy as np


class FaceDetector:
    """Simple haarcascade detector does not work well..."""
    def __init__(self, frontal_face_model, profile_face_model):
        self._frontal_face_model = cv2.CascadeClassifier(frontal_face_model)
        self._profile_face_model = cv2.CascadeClassifier(profile_face_model)

    def _face_detector(self, img_path, model):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = model.detectMultiScale(gray, 1.3, 5)
        if type(faces) is not tuple:
            return faces.shape[0]
        return 0

    def detect_faces(self, img_path):
        total_frontal_faces = self._face_detector(img_path,
                                                  self._frontal_face_model)
        total_profile_faces = self._face_detector(img_path,
                                                  self._profile_face_model)
        return total_frontal_faces, total_profile_faces
