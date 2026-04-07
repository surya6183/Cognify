import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import cv2
import pandas as pd
import time

from src.face_detection import FaceAnalyzer
from src.activity_tracking import ActivityTracker
from src.feature_extraction import build_feature_vector
from src.app_tracking import AppTracker
from src.data_logger import DataLogger

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(layout="wide")
st.title("🧠 CognifyAI - Focus & Productivity Monitor")

# ----------------------------
# SESSION LOGGER FIX (IMPORTANT)
# ----------------------------
if "logger" not in st.session_state:
    st.session_state.logger = DataLogger()

logger = st.session_state.logger

# ----------------------------
# INIT
# ----------------------------
cap = cv2.VideoCapture(0)
face = FaceAnalyzer()
activity = ActivityTracker()
app_tracker = AppTracker()

# ----------------------------
# SAVE BUTTON
# ----------------------------
if st.button("💾 Save Session Data"):
    if len(logger.data) > 0:
        logger.save()
        st.success("Session data saved successfully")
    else:
        st.warning("No data collected yet")

# Debug (optional)
st.write("Logged rows:", len(logger.data))

# ----------------------------
# UI LAYOUT
# ----------------------------
col1, col2 = st.columns(2)

frame_placeholder = col1.empty()
metrics_placeholder = col2.empty()
chart_placeholder = st.empty()
app_usage_placeholder = st.empty()

# ----------------------------
# GRAPH SETUP
# ----------------------------
focus_history = []
chart_data = pd.DataFrame(columns=["Focus"])
chart = chart_placeholder.line_chart(chart_data)

frame_count = 0
last_update_time = time.time()

# ----------------------------
# FOCUS LOGIC
# ----------------------------
def compute_focus(features):
    blink, gaze, head, face, typing, mouse_move, mouse_click, idle = features

    if face == 0:
        return 0, "Absent"

    score = 100

    if gaze == 0:
        score -= 25
    if blink == 1:
        score -= 15
    if abs(head) > 0.15:
        score -= 15

    if idle > 5:
        score -= 30
    if typing < 1:
        score -= 10
    if mouse_move < 1:
        score -= 10

    score = max(0, min(100, score))

    if score > 70:
        label = "Low"
    elif score > 40:
        label = "Medium"
    else:
        label = "High"

    return score, label

# ----------------------------
# PRODUCTIVITY SCORE
# ----------------------------
def compute_productivity(focus_score, activity_data, usage):

    typing = activity_data["typing_speed"]
    mouse = activity_data["mouse_movement"]
    idle = activity_data["idle_time"]

    score = focus_score * 0.5
    score += min(20, typing * 2 + mouse)

    if idle > 5:
        score -= 20
    elif idle > 3:
        score -= 10

    productive_apps = ["code", "pycharm", "notepad", "jupyter"]
    distracting_apps = ["youtube", "instagram", "facebook", "game"]

    for app in usage:
        name = app.lower()
        if any(p in name for p in productive_apps):
            score += 5
        elif any(d in name for d in distracting_apps):
            score -= 5

    return int(max(0, min(100, score)))

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:

    ret, frame = cap.read()
    if not ret:
        st.error("Webcam not detected")
        break

    frame = cv2.resize(frame, (480, 360))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_count += 1

    # Show video
    frame_placeholder.image(frame_rgb)

    # Skip frames for performance
    if frame_count % 3 != 0:
        continue

    # ----------------------------
    # FEATURES
    # ----------------------------
    face_data = face.process(frame)
    activity_data = activity.get_features()
    app_tracker.update()
    usage = app_tracker.get_usage()

    features = build_feature_vector(face_data, activity_data)

    # ----------------------------
    # SCORES
    # ----------------------------
    focus_score, cognitive_load = compute_focus(features)
    productivity_score = compute_productivity(focus_score, activity_data, usage)

    # ----------------------------
    # LOG DATA (NOW WORKS ✅)
    # ----------------------------
    logger.log(features, focus_score, productivity_score, cognitive_load)

    # ----------------------------
    # GRAPH UPDATE
    # ----------------------------
    current_time = time.time()

    if current_time - last_update_time > 0.8:

        focus_history.append(focus_score)

        if len(focus_history) > 30:
            focus_history.pop(0)

        smoothed = int(sum(focus_history[-5:]) / min(len(focus_history), 5))
        chart.add_rows(pd.DataFrame({"Focus": [smoothed]}))

        last_update_time = current_time

    # ----------------------------
    # METRICS
    # ----------------------------
    with metrics_placeholder.container():

        st.metric("Focus Score", f"{focus_score}%")
        st.metric("Productivity Score", f"{productivity_score}%")

        if cognitive_load == "Low":
            st.success("Focused")
        elif cognitive_load == "Medium":
            st.warning("Distracted")
        elif cognitive_load == "High":
            st.error("Fatigue Detected")
        else:
            st.info("No User")

        if productivity_score > 75:
            st.success("Highly Productive")
        elif productivity_score > 50:
            st.warning("Moderately Productive")
        else:
            st.error("Low Productivity")

    # ----------------------------
    # APP USAGE
    # ----------------------------
    if usage:
        app_usage_placeholder.subheader("💻 App Usage")
        app_usage_placeholder.bar_chart(usage)