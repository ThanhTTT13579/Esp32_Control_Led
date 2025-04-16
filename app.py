from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

# Biến toàn cục để lưu trạng thái LED
led_status = "OFF"
esp_status = "UNKNOWN" # Trạng thái thật do ESP32 phản hồi
history = []           # Lịch sử hoạt động

@app.route('/')
def index():
    return render_template("index.html", status=esp_status)

@app.route('/set-command/<cmd>')
def set_command(cmd):
    global led_status
    if cmd.upper() in ["ON", "OFF"]:
        led_status = cmd.upper()
        return f"Command set to {led_status}"
    return "Invalid command", 400

@app.route('/get-command')
def get_command():
    return led_status

@app.route('/report-status', methods=['POST'])
def report_status():
    global esp_status
    data = request.get_json()
    status = data.get("status")

    if status in ["ON", "OFF"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        esp_status = status  # <--- Lưu lại trạng thái thực tế từ ESP32
        history.append({"time": timestamp, "status": status})
        print(f"[{timestamp}] ESP32 reported: {status}")
        return "Status recorded", 200
    return "Invalid status", 400

@app.route('/history')
def view_history():
    return render_template("history.html", logs=history)

if __name__ == '__main__':
    app.run(debug=True)
