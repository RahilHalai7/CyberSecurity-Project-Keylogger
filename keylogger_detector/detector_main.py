import psutil
import os
import socket

# Suspicious keywords often used in keyloggers
SUSPICIOUS_KEYWORDS = ['keylogger', 'pynput', 'keyboard', 'logger', 'input']

# Suspicious directories
SUSPICIOUS_DIRS = ['AppData', 'Temp', 'Roaming']

def is_suspicious_process(proc):
    try:
        name = proc.name().lower()
        exe = proc.exe().lower()
        cmdline = " ".join(proc.cmdline()).lower()

        # Keyword check
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in name or keyword in cmdline:
                return True

        # Suspicious directory check
        for dir_name in SUSPICIOUS_DIRS:
            if dir_name.lower() in exe:
                return True

    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False

    return False

def list_suspicious_processes():
    print("🔍 Scanning for suspicious keylogger-like processes...\n")
    flagged = []
    for proc in psutil.process_iter(['pid', 'name']):
        if is_suspicious_process(proc):
            print(f"⚠️  Suspicious Process: {proc.info['name']} (PID: {proc.info['pid']})")
            flagged.append(proc.info)
    if not flagged:
        print("✅ No suspicious keylogger-like processes found.")
    return flagged

def list_open_ports():
    print("\n🔍 Listing open ports (may indicate remote logging):\n")
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_ESTABLISHED:
            try:
                proc = psutil.Process(conn.pid)
                print(f"📡 Port: {conn.laddr.port} → PID: {conn.pid} ({proc.name()})")
            except:
                continue

if __name__ == "__main__":
    list_suspicious_processes()
    list_open_ports()

