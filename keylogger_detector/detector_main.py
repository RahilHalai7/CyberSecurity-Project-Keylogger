import psutil
import os
import socket

# Define suspicious patterns
SUSPICIOUS_KEYWORDS = ['keylogger', 'pynput', 'keyboard', 'logger', 'input']
SUSPICIOUS_DIRS = ['AppData', 'Temp', 'Roaming']

def is_suspicious_process(proc):
    try:
        name = proc.name().lower()
        exe = proc.exe().lower()
        cmdline = " ".join(proc.cmdline()).lower()

        # Check for suspicious keywords
        if any(keyword in name or keyword in cmdline for keyword in SUSPICIOUS_KEYWORDS):
            return True

        # Check for suspicious directories
        if any(dir_name.lower() in exe for dir_name in SUSPICIOUS_DIRS):
            return True

    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False

    return False

def list_suspicious_processes():
    print("\n🔍 Scanning for suspicious keylogger-like processes...\n")
    flagged = []

    for proc in psutil.process_iter(['pid', 'name']):
        if is_suspicious_process(proc):
            name = proc.info.get('name', 'Unknown')
            pid = proc.info.get('pid', '?')
            print(f"⚠️  Suspicious Process: {name} (PID: {pid})")
            flagged.append({'name': name, 'pid': pid})

    if not flagged:
        print("✅ No suspicious keylogger-like processes found.")
    else:
        print(f"\n🚨 Total Suspicious Processes Found: {len(flagged)}")

    return flagged

def list_open_ports():
    print("\n🌐 Scanning open network connections (may indicate remote logging):\n")
    connections = []

    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_ESTABLISHED:
            try:
                proc = psutil.Process(conn.pid)
                port_info = {
                    'pid': conn.pid,
                    'name': proc.name(),
                    'port': conn.laddr.port,
                    'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                }
                print(f"📡 Port {port_info['port']} → PID: {port_info['pid']} ({port_info['name']}) → Remote: {port_info['remote']}")
                connections.append(port_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    if not connections:
        print("✅ No established suspicious connections found.")
    else:
        print(f"\n🔐 Total Active Connections: {len(connections)}")

    return connections

if __name__ == "__main__":
    suspicious = list_suspicious_processes()
    open_ports = list_open_ports()
