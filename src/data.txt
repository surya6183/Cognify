import pandas as pd
import os

class DataLogger:
    def __init__(self):
        self.data = []

    def log(self, features, focus, productivity, label):
        self.data.append(features + [focus, productivity, label])

    def save(self):
        df = pd.DataFrame(self.data, columns=[
            "blink_rate",
            "gaze_center",
            "head_angle",
            "face_detected",
            "typing_speed",
            "mouse_movement",
            "mouse_click_rate",
            "idle_time",
            "focus_score",
            "productivity_score",
            "cognitive_load"
        ])

        os.makedirs("data", exist_ok=True)
        df.to_csv("data/session_log.csv", index=False)

        print("Saved → data/session_log.csv")