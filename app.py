# app.py
from flask import Flask

app = Flask(__name__)
command = "OFF"

@app.route('/')
def home():
    return f"""
        <h2>ESP32 Remote Control</h2>
        <p>Current command: {command}</p>
        <a href='/set-command/ON'>Turn ON</a> |
        <a href='/set-command/OFF'>Turn OFF</a>
    """

@app.route('/set-command/<cmd>')
def set_command(cmd):
    global command
    if cmd.upper() in ["ON", "OFF"]:
        command = cmd.upper()
        return f" Command set to: {command}"
    else:
        return " Invalid command", 400

@app.route('/get-command')
def get_command():
    return command

if __name__ == '__main__':
    app.run()
