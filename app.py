from flask import Flask, render_template, request, send_from_directory
import os
import tempfile
import re
import psutil
import subprocess

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 7 * 1024 * 1024  # 7MB

DOWNLOAD_FOLDER = "/mnt/c/Users/Lavav/Documents/SwiftPrinterWebApp-main/SwiftPrinterWebApp-main/downloads"
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def increment_runs():
    if not os.path.exists("runs.txt"):
        with open("runs.txt", "w") as f:
            f.write("0")
    with open('runs.txt', 'r') as file:
        content = file.read().strip()
        current_number = int(content) if content.isdigit() else 0
    new_number = current_number + 1
    with open('runs.txt', 'w') as file:
        file.write(str(new_number))

def process_file(file_path):
    script_path = os.path.abspath('./worker6.sh')
    script_dir = os.path.dirname(script_path)
    try:
        r = subprocess.run([script_path, file_path], check=True, cwd=script_dir)
        print(r)
    except subprocess.CalledProcessError as e:
        print(f"Error executing worker script: {e}")

def format_time(hours):
    hours = float(hours.strip())
    hours_int = int(hours)
    minutes = int((hours - hours_int) * 60)
    return f"{hours_int}h {minutes}m"

def sanitize_filename(filename):
    return re.sub(r'[^\w\-.]', '_', filename)

@app.route('/')
def upload_form():
    runs = "0"
    if os.path.exists("runs.txt"):
        with open("runs.txt", "r", encoding="UTF-8") as file:
            runs = file.readline().strip()
    cpu = psutil.cpu_percent(0.3)
    return render_template('upload.html', runs=runs, cpu=cpu)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        temp_dir = tempfile.mkdtemp()
        filename = sanitize_filename(file.filename.replace(" ", "_"))
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)

        process_file(file_path)

        # the zip name is same as uploaded file + .zip in DOWNLOAD_FOLDER
        data_file = f"{filename}.zip"
        zip_full_path = os.path.join(app.config['DOWNLOAD_FOLDER'], data_file)
        if not os.path.isfile(zip_full_path):
            return "Processed zip file not found", 404

        time_str = "1.5"
        time_file_path = os.path.join(temp_dir, "time.txt")
        if os.path.isfile(time_file_path):
            with open(time_file_path, "r", encoding="UTF-8") as time_file:
                time_str = time_file.readline().strip()

        increment_runs()
        return render_template('download.html', data_file=data_file, ETA=format_time(time_str))

@app.route('/downloads/<path:filename>')
def download_file(filename):
    # serve from the downloads folder matching worker.sh zip output
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

@app.errorhandler(413)
def request_entity_too_large(error):
    return "File is too large. Maximum file size is 7MB.", 413

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=63080)
