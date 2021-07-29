import os
from flask import Flask, render_template, request, redirect
from inference import get_prediction
import shutil
import glob

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

