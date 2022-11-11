from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import os
from werkzeug.utils import secure_filename
from flask import Flask, session, url_for, request, flash, redirect, render_template
from flask_restful import Api, Resource, reqparse, abort
import soundfile as sf

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'wav'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
api = Api(app)

audios = {}

def abort_if_filename_doesnt_exit(filename):
    if filename not in audios:
        abort(404, message="filename not found...")
def abort_if_filename_already_exit(filename):
    if filename in audios:
        abort(409, message="filename already exists...")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def abort_if_unsupported_type(filename):
    if not allowed_file(filename):
        return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        # Abort if file's extension type is not supported
        abort_if_unsupported_type(file.filename)
        # Abort if a file with the same name exists
        abort_if_filename_already_exit(file.filename)
        filename = secure_filename(file.filename)

        # Store the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Store metadata
        f = sf.SoundFile(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        audios[filename] = {
            "duration (s)": f.frames / f.samplerate
        }
        # return redirect(url_for('download_file', name=filename))
        return redirect(url_for('download', name=filename), code=301)

@app.route("/download", methods=['GET'])
def download():
    args = request.args
    if "name" in args:
        abort_if_filename_doesnt_exit(args["name"])
        return render_template("download.html", filename='uploads/' + args["name"])
    return "Must specify a filename to be downloaded", 404
@app.route("/list", methods=['GET'])
def list():
    args = request.args
    matches = {}
    # Only support maxduration at this point
    if "maxduration" in args:
        for filename, audio in audios.items():
            if audio["duration (s)"] <= float(args["maxduration"]):
                matches[filename] = audio
    else:
        matches = audios
    return render_template("list.html", matches=matches)

@app.route("/info", methods=['GET'])
def info():
    args = request.args
    if "name" in args:
        abort_if_filename_doesnt_exit(args["name"])
        match = audios[args["name"]]
    else:
        match = ""
    return render_template("info.html", match=match)

if __name__ == '__main__':
    # clean uploads/ on rebooting server
    # create if not exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    else:
        for f in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, f))
    app.run(debug=True)
