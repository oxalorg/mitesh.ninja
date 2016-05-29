import json
import os
import random
import string
import logging

from flask import request, url_for, send_from_directory, render_template, flash
from werkzeug import secure_filename

from app.upload import models
from app import db, app

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
logging.basicConfig(level=logging.DEBUG)


# Research if using class is the best method in this scenario?
# I can import this class in other modules and get my uploads done
# rather easily. So for the time being, this seems perfect.
class UploadFileHandler:
    def __init__(self, files):
        """
        :param files: list of werkzeug FileStorage objects.
        """
        self.files = files
        self.uploaded_list = []

    # TODO: Fix this function. Too messy.
    def upload_all(self):
        """
        :return: list of urls of uploaded files.
        """
        flag = False
        for file in self.files:
            if file:
                filename = UploadFileHandler.generate_unique_filename(
                    file.filename)
                if UploadFileHandler.allowed_file(file.filename):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                             filename)
                    file.save(file_path)
                    file_size = os.stat(file_path).st_size
                    file_details = models.FileDetails(
                        secure_filename(file.filename), filename, file_size,
                        file_path)
                    db.session.add(file_details)
                    self.uploaded_list.append(url_for('uploaded_file',
                                                      filename=filename,
                                                      _external=True))
                else:
                    flag = True
        if flag is True:
            flash('One or more file extensions not supported.')
        db.session.commit()
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
        ext = os.path.splitext(filename)[1]
        if ext.startswith('.'):
            # splitext may contain a . separator
            ext = ext[1:]
        return ext

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               UploadFileHandler.get_file_extension(filename).lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form['password'] == app.config['NINJA_CLAN_SIGN']:
            files = request.files.getlist('file[]')
            uploaded_files = UploadFileHandler(files).upload_all()
            if len(uploaded_files) > 0:
                return json.dumps({'files': uploaded_files,
                                   'count': len(uploaded_files)})
            else:
                return json.dumps({'success': 0})
        else:
            return render_template('disgrace.html'), 401
    return render_template('upload.html')


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
