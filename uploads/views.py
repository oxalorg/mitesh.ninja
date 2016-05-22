import os
import random
import string
import fcntl

import threading
from queue import Queue
from flask import request, redirect, url_for, send_from_directory, send_file, render_template, flash
import logging
from uploads import app
from werkzeug import secure_filename

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
logging.basicConfig(level=logging.DEBUG)

class UploadFileHandler:
    def __init__(self, files):
        self.files = files
        self.uploaded_list = []

    def upload_all(self):
        for file in self.files:
            if file:
                filename = UploadFileHandler.generate_unique_filename(
                    file.filename)
                if UploadFileHandler.allowed_file(file.filename):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                           filename))
                    self.uploaded_list.append(url_for('uploaded_file',
                                                      filename=filename,
                                                      _external=True))
                else:
                    flash(
                        'One or more file types is not supported. Hence not uploaded.')
        return self.uploaded_list

    @staticmethod
    def generate_unique_filename(filename):
        while True:
            unique_filename = ''.join(
                random.choice(string.ascii_letters) for _ in range(
                    10)) + '.' + UploadFileHandler.get_file_extension(filename)
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],
                                           unique_filename)):
                continue
            return unique_filename

    @staticmethod
    def get_file_extension(filename):
        return filename.rsplit('.', 1)[1]

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               UploadFileHandler.get_file_extension(filename) in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        uploaded_files = UploadFileHandler(files).upload_all()
        UploadCountHandler(len(uploaded_files))
        return render_template('show_uploaded_list.html',
                               uploaded_files=uploaded_files)
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


def update_count():
    while not q.empty():
        with open(app.config['COUNT_FILE'], 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            temp_text = f.read()
            if temp_text == '':
                count = 0
            else:
                count = int(temp_text)
            logging.debug('count = {}'.format(count))
            f.seek(0)
            f.truncate()
            up_count = q.get()
            logging.debug('q.get() count = {}'.format(up_count))
            f.write(str(count + up_count))
            fcntl.flock(f, fcntl.LOCK_UN)
            q.task_done()


q = Queue()


class UploadCountHandler:
    thr = None

    def __init__(self, count):
        logging.debug("Added to queue")
        q.put(count)
        if self.thr is None or not self.thr.is_alive():
            self.thr = threading.Thread(target=update_count).start()

