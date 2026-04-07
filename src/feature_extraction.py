def build_feature_vector(face_data, activity_data):
    return [
        face_data["blink_rate"],
        face_data["gaze_center"],
        face_data["head_angle"],
        face_data["face_detected"],
        activity_data["typing_speed"],
        activity_data["mouse_movement"],      # NEW
        activity_data["mouse_click_rate"],    # NEW
        activity_data["idle_time"]
    ]