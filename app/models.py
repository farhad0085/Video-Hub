from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager


# this will handle user session, so we don't need to do anything
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Integer, default=0)

    # create a one to many relationship between trainer and customers
    videos = db.relationship('Video', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}')"

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String(120))
    video_link = db.Column(db.String(120))
    video_description = db.Column(db.String(300))
    video_thumb = db.Column(db.String(50), default='default.png')
    uploaded_time = db.Column(db.DateTime, default=datetime.now)
    modified_time = db.Column(db.DateTime, default=datetime.now)

    # this is the column with which we are creating the relation with user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Video('{self.id}','{self.video_title}','{self.video_link}')"
