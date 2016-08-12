import os
from app import app, db
from flask import render_template, request, redirect, url_for
from dystic import builder

ROOT = os.path.expanduser(app.config['OROOT'])
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'docx', 'ppt', 'mp4', 'mp3', 'wav', 'avi'])


def get_file_extension(filename):
    ext = os.path.splitext(filename)[1]
    if ext.startswith('.'):
        # splitext may contain a . separator
        ext = ext[1:]
    return ext


def allowed_file(filename):
    return '.' in filename and \
           get_file_extension(filename).lower() in ALLOWED_EXTENSIONS


@app.route('/post', methods=["GET", "POST"])
def opost():
    if request.method == 'POST':
        if request.form['password'] == app.config['NINJA_CLAN_SIGN']:
            post_body = request.form['body']
            post_folder = request.form['path']
            other_folders = post_folder.split('/')[-1]
            if '.' in post_folder:
                return "Cannot contain dots in folder path.", 403
            folder = os.path.abspath(os.path.join(ROOT, post_folder))
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(
                    os.path.abspath(os.path.join(folder, os.path.basename(folder) + '.md')),
                    'w',
                    encoding='UTF-8',
                    errors='replace') as f:
                f.write(post_body)
            build(folder, other_folders)
            try:
                files = request.files.getlist('file[]')
                for f in files:
                    if f:
                        filename = f.filename
                        file_path = os.path.abspath(os.path.join(folder, filename))
                        f.save(file_path)
            except:
                print("Error occurred while parsing files.")
            return redirect(url_for('index'))
    return render_template('opost.html')


def build(folder, other_folders, root=ROOT):
    b = builder.Builder(root)
    b.build_dir(folder)
    b.build_index(folder)
    parent = os.path.join(folder, os.pardir)
    rewrite_flag = True
    if os.path.abspath(root) != os.path.abspath(os.path.join(root, folder)):
        while os.path.abspath(root) != os.path.abspath(parent):
            if rewrite_flag or 'index.html' not in os.listdir(parent):
                b.build_index(parent)
                rewrite_flag = False
            parent = os.path.join(parent, os.pardir)
