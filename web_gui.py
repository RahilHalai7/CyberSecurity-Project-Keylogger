from flask import Flask, render_template_string, request, jsonify
import subprocess
import threading
import os

app = Flask(__name__)

# --- HTML/CSS GUI ---
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Keylogger & Detector Control Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }
        .container { max-width: 700px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #ccc; padding: 32px; }
        h1 { text-align: center; color: #333; }
        .controls { display: flex; justify-content: space-around; margin-bottom: 30px; }
        button { padding: 12px 24px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer; transition: background 0.2s; }
        button.start { background: #4CAF50; color: #fff; }
        button.stop { background: #f44336; color: #fff; }
        button:disabled { background: #aaa; }
        .log-section { margin-top: 30px; }
        pre { background: #222; color: #eee; padding: 16px; border-radius: 6px; max-height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Keylogger & Detector Control Panel</h1>
        <div class="controls">
            <div>
                <button id="start-keylogger" class="start">Start Keylogger</button>
                <button id="stop-keylogger" class="stop">Stop Keylogger</button>
            </div>
            <div>
                <button id="start-detector" class="start">Start Detector</button>
                <button id="stop-detector" class="stop">Stop Detector</button>
            </div>
        </div>
        <div class="log-section">
            <h2>Keylogger Log</h2>
            <button onclick="fetchLog()">Refresh Log</button>
            <pre id="log-content">Loading...</pre>
        </div>
    </div>
    <script>
        function fetchLog() {
            fetch('/log')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('log-content').textContent = data.log;
                });
        }
        document.getElementById('start-keylogger').onclick = function() {
            fetch('/start_keylogger', {method: 'POST'}).then(fetchLog);
        };
        document.getElementById('stop-keylogger').onclick = function() {
            fetch('/stop_keylogger', {method: 'POST'}).then(fetchLog);
        };
        document.getElementById('start-detector').onclick = function() {
            fetch('/start_detector', {method: 'POST'});
        };
        document.getElementById('stop-detector').onclick = function() {
            fetch('/stop_detector', {method: 'POST'});
        };
        // Auto-refresh log every 5 seconds
        setInterval(fetchLog, 5000);
        fetchLog();
    </script>
</body>
</html>
'''

# --- Process management ---
keylogger_proc = None
detector_proc = None

def start_keylogger():
    global keylogger_proc
    if keylogger_proc is None:
        keylogger_proc = subprocess.Popen(['python', 'main.py'])

def stop_keylogger():
    global keylogger_proc
    if keylogger_proc is not None:
        keylogger_proc.terminate()
        keylogger_proc = None

def start_detector():
    global detector_proc
    if detector_proc is None:
        detector_proc = subprocess.Popen(['python', 'keylogger_detector/detector_main.py'])

def stop_detector():
    global detector_proc
    if detector_proc is not None:
        detector_proc.terminate()
        detector_proc = None

# --- Flask routes ---
@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/log')
def get_log():
    if os.path.exists('log.txt'):
        with open('log.txt', 'r', encoding='utf-8') as f:
            log = f.read()[-5000:]  # Show last 5000 chars
    else:
        log = ''
    return jsonify({'log': log})

@app.route('/start_keylogger', methods=['POST'])
def start_keylogger_route():
    threading.Thread(target=start_keylogger).start()
    return ('', 204)

@app.route('/stop_keylogger', methods=['POST'])
def stop_keylogger_route():
    stop_keylogger()
    return ('', 204)

@app.route('/start_detector', methods=['POST'])
def start_detector_route():
    threading.Thread(target=start_detector).start()
    return ('', 204)

@app.route('/stop_detector', methods=['POST'])
def stop_detector_route():
    stop_detector()
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 