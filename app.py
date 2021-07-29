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

@app.route('/', methods=["GET", 'POST'])
def home_page():
    return render_template('index.html')

@app.route('/files', methods=['GET', 'POST'])
def upload_folder():
    if request.method == 'POST':
        if 'files' not in request.files:
            print("redirection - pas d'input folder")
            return redirect('/')
        files = request.files.getlist('files')
        if files == '':
            print('redirection - pas de filename dans folder')
            return redirect('/')
        result = []
        for file in files:
            class_name, class_id, filename = read_file(file)
            if class_name == 404:
                return redirect('/')
            result.append({'class_name': class_name, 'class_id': class_id, 'filename': filename})
        return render_template('result.html', data=result)
    return redirect('/')

if __name__ == '__main__':
    if os.path.isdir(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    os.mkdir(UPLOAD_FOLDER)
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
