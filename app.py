"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:K1ashmir!@localhost:5432/blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def home_page():

    return redirect('/users/index.html')

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

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')









