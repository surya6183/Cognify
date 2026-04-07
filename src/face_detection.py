import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [33, 160, 158, 133, 153, 144]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def get_eye_coords(landmarks, indices, w, h):
    return np.array([(landmarks[i].x * w, landmarks[i].y * h) for i in indices])

def get_head_angle(landmarks):
    left = landmarks[33].x
    right = landmarks[263].x
    return float(right - left)

class FaceAnalyzer:
    def __init__(self):
        self.mesh = mp_face_mesh.FaceMesh(
    	    refine_landmarks=False,   # faster
            max_num_faces=1
        )

    def process(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.mesh.process(rgb)

        # ❗ NO FACE CASE
        if not res.multi_face_landmarks:
            return {
                "blink_rate": 0.0,
                "gaze_center": 0,
                "head_angle": 0.0,
                "face_detected": 0
            }

        lm = res.multi_face_landmarks[0].landmark

        eye = get_eye_coords(lm, LEFT_EYE, w, h)
        ear = eye_aspect_ratio(eye)

        # Better blink detection
        if ear < 0.21:
            blink_rate = 1.0
        else:
            blink_rate = 0.0


        eye_x = lm[33].x

        if 0.35 < eye_x < 0.65:
            gaze_center = 1
        else:
            gaze_center = 0
        head_angle = get_head_angle(lm)
        # If head turned too much → distraction
        if abs(head_angle) > 0.15:
            gaze_center = 0

        return {
            "blink_rate": blink_rate,
            "gaze_center": gaze_center,
            "head_angle": head_angle,
            "face_detected": 1
        }