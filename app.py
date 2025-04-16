from flask import Flask, request, render_template
from datetime import datetime
import pytz
from datetime import datetime

# Cấu hình múi giờ Việt Nam
vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

app = Flask(__name__)

# Biến toàn cục để lưu trạng thái LED
led_status = "OFF"
esp_status = "Hello" # Trạng thái thật do ESP32 phản hồi
history = [  # Dữ liệu mặc định để hiển thị thử trên trang /history
    {"time": "2025-04-15 10:00:00", "status": "ON"},
    {"time": "2025-04-15 10:05:00", "status": "OFF"},
    {"time": "2025-04-15 10:10:00", "status": "ON"},
]

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

    print("Received JSON:", data)

    status = data.get("status")

    if status in ["ON", "OFF"]:
        timestamp = datetime.now(vietnam_tz).strftime("%Y-%m-%d %H:%M:%S")
        esp_status = status  # <--- Lưu lại trạng thái thực tế từ ESP32
        history.append({"time": timestamp, "status": status})
        print(f"[{timestamp}] ESP32 reported: {status}")
        return "Status recorded", 200
    return "Invalid status", 400

@app.route('/get-real-status')
def get_real_status():
    return esp_status


@app.route('/history')
def view_history():
    return render_template("history.html", logs=history)

if __name__ == '__main__':
    app.run(debug=True)
