import psutil

# More precise keywords
SUSPICIOUS_KEYWORDS = [
    'keylogger', 'pynput', 'keyboard.listener',
    'intercept', 'keystroke', 'spyware'
]

# Common safe programs — skip these to avoid false positives
WHITELISTED_PROCESSES = [
    'code.exe', 'chrome.exe', 'msedge.exe', 'msedgewebview2.exe',
    'textinputhost.exe', 'python.exe', 'wpscenter.exe',
    'explorer.exe', 'nvcontainer.exe', 'svchost.exe'
]

# Suspicious directories
SUSPICIOUS_DIRS = ['AppData', 'Temp', 'Roaming']


def is_suspicious_process(proc):
    try:
        name = proc.name().lower()
        exe = proc.exe().lower()
        cmdline = " ".join(proc.cmdline()).lower()

        # ✅ Whitelist check
        if name in WHITELISTED_PROCESSES:
            return False

        # ✅ Keyword check
        if any(keyword in name or keyword in cmdline for keyword in SUSPICIOUS_KEYWORDS):
            return True

        # ✅ Directory check
        if any(dir_name.lower() in exe for dir_name in SUSPICIOUS_DIRS):
            return True

    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False

    return False


def list_suspicious_processes():
    flagged = []

    for proc in psutil.process_iter(['pid', 'name']):
        if is_suspicious_process(proc):
            name = proc.info.get('name', 'Unknown')
            pid = proc.info.get('pid', '?')
            flagged.append({'name': name, 'pid': pid})

    return flagged


def list_open_ports():
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
                connections.append(port_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    return connections


# Optional standalone run
if __name__ == "__main__":
    print("\n🔍 Scanning for suspicious keylogger-like processes...\n")
    suspicious = list_suspicious_processes()
    if not suspicious:
        print("✅ No suspicious keylogger-like processes found.")
    else:
        for proc in suspicious:
            print(f"⚠️  Suspicious Process: {proc['name']} (PID: {proc['pid']})")
        print(f"\n🚨 Total Suspicious Processes Found: {len(suspicious)}")

    print("\n🌐 Scanning open network connections (may indicate remote logging):\n")
    open_ports = list_open_ports()
    if not open_ports:
        print("✅ No established suspicious connections found.")
    else:
        for conn in open_ports:
            print(f"📡 Port {conn['port']} → PID: {conn['pid']} ({conn['name']}) → Remote: {conn['remote']}")
        print(f"\n🔐 Total Active Connections: {len(open_ports)}")
