import os
from app import app, db
from flask import render_template, request, redirect, url_for
from dystic import builder

ROOT = os.path.expanduser(app.config['OROOT'])


@app.route('/o/post', methods=["GET", "POST"])
def opost():
    if request.method == 'POST':
        if request.form['password'] == app.config['NINJA_CLAN_SIGN']:
            post_body = request.form['body']
            post_folder = request.form['path']
            if '.' in post_folder:
                return "Cannot contain dots in folder path.", 403
            folder = os.path.abspath(os.path.join(ROOT, post_folder))
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(os.path.abspath(os.path.join(folder, os.path.basename(folder) + '.md')), 'w') as f:
                f.write(post_body)
            build(folder)
            return redirect(url_for('index'))
    return render_template('opost.html')


def build(folder, root=ROOT):
    b = builder.Builder(root)
    b.build_dir(folder)
    b.build_index(folder)
    if os.path.abspath(root) != os.path.abspath(os.path.join(root, folder)):
        b.build_index(os.path.join(folder, os.pardir))
