from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    pptx = request.files.get('pptx_file')

    # Validate file presence and extension
    if not pptx or not pptx.filename.endswith('.pptx'):
        return "Please upload a valid .pptx file.", 400

    # Secure the filename
    filename = secure_filename(pptx.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = input_path.replace('.pptx', '.pdf')

    # Save the uploaded file
    pptx.save(input_path)

    # Convert using LibreOffice
    try:
        subprocess.run([
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            '--headless',
            '--convert-to', 'pdf',
            input_path,
            '--outdir', UPLOAD_FOLDER
        ], check=True)
    except subprocess.CalledProcessError:
        return "Conversion failed. Please check the file or LibreOffice setup.", 500

    # Return the converted PDF
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "PDF file not found after conversion.", 500

if __name__ == '__main__':
    app.run(debug=True)