from flask import Flask, request, render_template

app = Flask(__name__)

# Biến toàn cục để lưu trạng thái LED
led_status = "OFF"

@app.route('/')
def index():
    return render_template("index.html", status=led_status)

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

if __name__ == '__main__':
    app.run(debug=True)
