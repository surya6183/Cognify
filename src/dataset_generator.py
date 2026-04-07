import pandas as pd
import random
import os

data = []

for _ in range(1000):
    # Face-related features
    blink = round(random.uniform(0.1, 0.5), 2)
    gaze = random.choice([0, 1])
    head = round(random.uniform(0.01, 0.7), 2)
    face = random.choice([0, 1])  # NEW

    # Activity features
    typing = round(random.uniform(0.1, 6), 2)
    mouse_move = round(random.uniform(0.1, 5), 2)
    mouse_click = round(random.uniform(0.1, 3), 2)
    idle = round(random.uniform(1, 12), 2)

    # 🔥 Label logic (important)
    if face == 0:
        label = "Absent"
    elif typing > 4 and idle < 3 and gaze == 1:
        label = "Low"
    elif typing > 1.5 and idle < 6:
        label = "Medium"
    else:
        label = "High"

    data.append([
        blink,
        gaze,
        head,
        face,
        typing,
        mouse_move,
        mouse_click,
        idle,
        label
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "blink_rate",
    "gaze_center",
    "head_angle",
    "face_detected",
    "typing_speed",
    "mouse_movement",
    "mouse_click_rate",
    "idle_time",
    "label"
])

# Save correctly (absolute path)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "behavioral_dataset.csv")

df.to_csv(data_path, index=False)

print("Dataset generated successfully (1000 rows with mouse + keyboard + face + Absent)")