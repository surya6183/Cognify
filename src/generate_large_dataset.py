import pandas as pd
import random
import os

# ----------------------------
# CONFIG
# ----------------------------
ROWS = 3000

data = []

for _ in range(ROWS):

    # ----------------------------
    # REALISTIC FEATURE GENERATION
    # ----------------------------
    blink_rate = random.choice([0, 1])

    gaze_center = random.choice([0, 1])

    head_angle = round(random.uniform(-0.3, 0.3), 3)

    face_detected = random.choice([0, 1])

    typing_speed = round(random.uniform(0, 6), 2)
    typing_speed += random.uniform(-0.5, 0.5)  # noise

    mouse_movement = round(random.uniform(0, 5), 2)
    mouse_movement += random.uniform(-0.3, 0.3)  # noise

    mouse_click_rate = round(random.uniform(0, 3), 2)

    idle_time = round(random.uniform(0, 12), 2)
    idle_time += random.uniform(-1, 1)  # noise

    # clamp values
    typing_speed = max(0, typing_speed)
    mouse_movement = max(0, mouse_movement)
    idle_time = max(0, idle_time)

    # ----------------------------
    # LABEL LOGIC (NON-DETERMINISTIC)
    # ----------------------------
    if face_detected == 0:
        label = "Absent"

    else:
        # base score (similar to your system)
        score = 100

        if gaze_center == 0:
            score -= random.randint(20, 30)

        if blink_rate == 1:
            score -= random.randint(10, 20)

        if abs(head_angle) > 0.15:
            score -= random.randint(10, 20)

        if idle_time > 6:
            score -= random.randint(25, 35)
        elif idle_time > 3:
            score -= random.randint(10, 20)

        if typing_speed < 1:
            score -= random.randint(5, 15)

        if mouse_movement < 1:
            score -= random.randint(5, 15)

        # ----------------------------
        # ADD CLASS OVERLAP
        # ----------------------------
        if score > 70:
            label = random.choice(["Low", "Medium"])
        elif score > 40:
            label = random.choice(["Medium", "High"])
        else:
            label = "High"

        # ----------------------------
        # RANDOM LABEL NOISE (IMPORTANT)
        # ----------------------------
        if random.random() < 0.1:
            label = random.choice(["Low", "Medium", "High"])

    # ----------------------------
    # STORE DATA
    # ----------------------------
    data.append([
        blink_rate,
        gaze_center,
        head_angle,
        face_detected,
        typing_speed,
        mouse_movement,
        mouse_click_rate,
        idle_time,
        label
    ])

# ----------------------------
# SAVE DATASET
# ----------------------------
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

os.makedirs("data", exist_ok=True)
df.to_csv("data/behavioral_dataset.csv", index=False)

print("✅ Dataset generated successfully (REALISTIC)")