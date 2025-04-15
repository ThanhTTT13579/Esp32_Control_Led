from flask import Flask, jsonify

app = Flask(__name__)
command = "OFF"

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Remote Control</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body class="bg-light text-center">
        <div class="container mt-5">
            <h2 class="mb-4">ESP32 Remote Control</h2>
            <h4>Current command: <span id="status">{command}</span></h4>
            <div class="mt-4">
                <button class="btn btn-success btn-lg me-2" onclick="sendCommand('ON')">Turn ON</button>
                <button class="btn btn-danger btn-lg" onclick="sendCommand('OFF')">Turn OFF</button>
            </div>
        </div>

        <script>
            function sendCommand(cmd) {{
                $.get('/set-command/' + cmd, function(data) {{
                    // Sau khi set command xong, yêu cầu lại trạng thái
                    $.get('/get-command', function(updatedStatus) {{
                        $('#status').text(updatedStatus);
                    }});
                }});
            }}

            // Cập nhật trạng thái mỗi 5 giây
            setInterval(function() {{
                $.get('/get-command', function(data) {{
                    $('#status').text(data);
                }});
            }}, 5000);
        </script>
    </body>
    </html>
    """

@app.route('/set-command/<cmd>')
def set_command(cmd):
    global command
    if cmd.upper() in ["ON", "OFF"]:
        command = cmd.upper()
        return f"Command set to: {command}"
    else:
        return "Invalid command", 400

@app.route('/get-command')
def get_command():
    return command

if __name__ == '__main__':
    app.run(debug=True)
