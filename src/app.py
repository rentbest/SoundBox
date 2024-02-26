from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os
import mimetypes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_AUDIO_TYPES'] = {'audio/mpeg', 'audio/ogg', 'audio/wav'}


@app.route('/')
def index():
    files = [f for f in os.listdir(
        app.config['UPLOAD_FOLDER']) if not f.startswith('.')]
    return render_template('index.html', files=files)


@app.route('/uploads')
def list_files_route():
    files = [f for f in os.listdir(
        app.config['UPLOAD_FOLDER']) if not f.startswith('.')]
    return jsonify({'files': files})


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file type'})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if allowed_audio_type(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({'error': 'Invalid audio file type'})


def allowed_file(filename):
    return '.' in filename and mimetypes.guess_type(filename)[0] in app.config['ALLOWED_AUDIO_TYPES']


def allowed_audio_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type in app.config['ALLOWED_AUDIO_TYPES']


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=8888, debug=True)
