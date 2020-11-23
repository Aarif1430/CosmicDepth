from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from cosmicdepth import db
from cosmicdepth.models import Post
from cosmicdepth.models import CsvFile
from cosmicdepth.posts.forms import PostForm
from werkzeug import secure_filename
import pandas as pd
import numpy as np
import io

posts = Blueprint('posts', __name__)


@posts.route("/post/display", methods=['GET', 'POST'])
@login_required
def display():
    table = []
    items = CsvFile.query.all()
    for rows in items:
        table.append([rows.name, rows.data])
    data = pd.DataFrame(table, columns=['Name', 'Rank']).sort_values(by=['Rank'], ascending=False)
    data['ID'] = list(range(1, len(data)+1))
    return render_template('leader_board.html', items=data.to_dict('records'))


@posts.route("/post/upload", methods=['GET', 'POST'])
@login_required
def file_upload():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('file_upload.html', title='New Post',
                           form=form, legend='New Post')

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in {'csv'}


@posts.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        df = pd.read_csv(io.BytesIO(file.read()), delim_whitespace=False, header=None)
        df.columns = df.iloc[0]
        df = df[1:]
        accuracy = np.sum(df['class'] == df['class'], axis=0) / len(df['class']) + round(np.random.random(),2)
        found_user = CsvFile.query.filter_by(name=current_user.email).first()
        user = found_user.name if found_user else 'abc'
        if user == current_user.email:
            found_user.data = accuracy
        else:
            user = CsvFile(name=current_user.email, data=accuracy)
            db.session.add(user)
        db.session.commit()
        flash('Your file was successfully uploaded', 'success')
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('error'))