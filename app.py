import os
from flask import Flask, render_template, request, redirect
from inference import get_prediction
import shutil
import glob

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def read_file(file):
    img_bytes = file.read()
    class_name, class_id = get_prediction(image_bytes=img_bytes)
    len_glob = len(glob.glob('static/uploads/*.*'))
    filename = f"{len_glob}_{class_name}_{file.filename.split('/')[-1]}"
    file.seek(0)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return class_name, class_id, filename