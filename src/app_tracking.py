import win32gui
import time

class AppTracker:
    def __init__(self):
        self.last_app = None
        self.start_time = time.time()
        self.usage = {}

    def update(self):
        try:
            window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except:
            window = "Unknown"

        now = time.time()

        if self.last_app:
            duration = now - self.start_time
            self.usage[self.last_app] = self.usage.get(self.last_app, 0) + duration

        self.last_app = window
        self.start_time = now

    def get_usage(self):
        return self.usage