"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:K1ashmir!@localhost:5432/blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '12234joijwef'

connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def home_page():

    posts = Post.query.order_by(Post.post_created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/users')
def show_users():
    users = User.query.order_by(User.user_last_name, User.user_first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def add_new_user_form():
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():
    new_user = User(
        user_first_name = request.form['user_first_name'],
        user_last_name = request.form['user_last_name'],
        user_image = request.form['user_image'] or None)
    
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added. Huzzah!")

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_list_users(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_users(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_users(user_id):
    user = User.query.get_or_404(user_id)
    user.user_first_name = request.form['user_first_name']
    user.user_last_name = request.form['user_last_name']
    user.user_image = request.form['user_image']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited. Heck yeah!")

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted. See ya {user.full_name}!")

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(post_title = request.form['post_title'],
                    post_content = request.form['post_content'],
                    user=user)
    
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.post_title}' has been added. oooo yeah buddy!")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.post_title = request.form['post_title']
    post.post_content = request.form['post_content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.post_title}' has been edited. Take a looksie loo!")

    return redirect(f"users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.post_title}' has been deleted. Buh bye {post.post_title}!")

    return redirect(f"/users/{post.user_id}")











