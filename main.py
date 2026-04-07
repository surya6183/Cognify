import cv2
import time

from src.face_detection import FaceAnalyzer
from src.activity_tracking import ActivityTracker
from src.feature_extraction import build_feature_vector
from src.prediction_engine import predict

cap = cv2.VideoCapture(0)

face = FaceAnalyzer()
activity = ActivityTracker()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    face_data = face.process(frame)
    activity_data = activity.get_features()

    features = build_feature_vector(face_data, activity_data)
    result = predict(features)

    cv2.putText(frame, f"Focus: {result['focus_score']}%", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f"Cognitive: {result['cognitive_load']}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.imshow("CognifyAI", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    time.sleep(2)

cap.release()
cv2.destroyAllWindows()