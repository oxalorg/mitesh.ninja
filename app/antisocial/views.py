from app import app, db
from app.antisocial.models import *
from app.upload.views import UploadFileHandler
from flask import render_template, request, redirect, url_for
import html
import re


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        post_body = request.form['body']
        print(post_body)
        return post_body
    return """
    <form class="" action="" method="post">
            <textarea name="body" rows="8" cols="40"></textarea><br>
            <input type="file" name="file[]" value="" multiple><br>
            <input type="submit" name="submit" value=""><br>
    </form>
    """


@app.route('/antisocial', methods=['GET'])
def antisocial():
    posts = Post.query.order_by(Post.creation_time.desc()).limit(10).all()
    return render_template('antisocial.html', posts=posts)


@app.route('/antisocial/post', methods=["GET", "POST"])
def antipost():
    if request.method == 'POST':
        if request.form['password'] == app.config['NINJA_CLAN_SIGN']:
            r = '<br />'
            post_body = request.form['body']
            newlines = re.compile(r'[\n(\n\r)\r(\r\n)]{2,}')
            post_body = re.sub(newlines, '\n', post_body)
            post_body = re.sub(r'[\n(\n\r)\r(\r\n)]*$', '', post_body)
            post_body = html.escape(post_body).replace(
                '\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)
            p = Post(post_body)
            db.session.add(p)
            db.session.flush([p])
            if request.files:
                post_files = request.files.getlist('file[]')
                uploaded_files = UploadFileHandler(post_files).upload_all()
                for link in uploaded_files:
                    up = PostFiles(p.id, link)
                    db.session.add(up)
            db.session.commit()
            return redirect(url_for('antisocial'))
    return render_template('antipost.html')
