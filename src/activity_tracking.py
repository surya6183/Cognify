from pynput import keyboard, mouse
import time
import threading

class ActivityTracker:
    def __init__(self):
        self.key_count = 0
        self.mouse_moves = 0
        self.mouse_clicks = 0
        self.last_activity = time.time()

        # Keyboard listener
        self.k_listener = keyboard.Listener(on_press=self.on_key)
        self.k_listener.start()

        # Mouse listener
        self.m_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        self.m_listener.start()

    def on_key(self, key):
        self.key_count += 1
        self.last_activity = time.time()

    def on_move(self, x, y):
        self.mouse_moves += 1
        self.last_activity = time.time()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_clicks += 1
            self.last_activity = time.time()

    def get_features(self):
        now = time.time()

        idle_time = now - self.last_activity

        typing_speed = self.key_count / 5.0      # approx per interval
        mouse_movement = self.mouse_moves / 5.0
        mouse_click_rate = self.mouse_clicks / 5.0

        # reset counters
        self.key_count = 0
        self.mouse_moves = 0
        self.mouse_clicks = 0

        return {
            "typing_speed": typing_speed,
            "mouse_movement": mouse_movement,
            "mouse_click_rate": mouse_click_rate,
            "idle_time": idle_time
        }