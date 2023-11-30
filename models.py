"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_image_url = 'https://images.unsplash.com/photo-1533738363-b7f9aef128ce?q=80&w=2835&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_first_name = db.Column(db.Text, nullable=False)
    user_last_name = db.Column(db.Text, nullable=False)
    user_image = db.Column(db.Text, nullable=False, default=default_image_url)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.user_first_name} {self.user_last_name}"
    

class Post(db.Model):

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    post_title = db.Column(db.Text, nullable = False)
    post_content = db.Column(db.Text, nullable = False)
    post_created_at = db.Column(db.DateTime, nullable = False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    @property
    def friendly_date(self):
        return self.post_created_at.strftime("%a %b %-d %Y, %-I:%M %p")
