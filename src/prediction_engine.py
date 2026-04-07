import joblib

model = joblib.load("models/cognitive_model.pkl")

def predict(features):
    blink, gaze, head, face, typing, mouse_move, mouse_click, idle = features

    #Nouser
    if face == 0:
        return {
            "focus_score": 0,
            "cognitive_load": "Absent"
        }

    score = 100

    if gaze == 0:
        score -= 30

    if blink == 1:
        score -= 20

    if idle > 5:
        score -= 30

    if typing < 1:
        score -= 10

    score = max(0, score)

    # ML prediction (secondary)
    pred = model.predict([features])[0]

    return {
        "focus_score": score,
        "cognitive_load": pred
    }