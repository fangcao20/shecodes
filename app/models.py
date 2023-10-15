from datetime import datetime
from hashlib import md5

from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login, app


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    phone_number = db.Column(db.String(12), index=True)
    work_place = db.Column(db.String(255), index=True)
    description = db.Column(db.String(1000))
    year = db.Column(db.Integer, index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', foreign_keys='Post.user_id', lazy='dynamic')
    sponsored_posts = db.relationship('Post', backref='sponsor', foreign_keys='Post.sponsor_id', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        name = self.name.replace(' ', '+')
        if self.role == 'Nhà hảo tâm':
            return 'https://ui-avatars.com/api/?name={}&size={}'.format(
                name, size)
        else:
            return 'https://ui-avatars.com/api/background=D2E0FB?name={}&size={}'.format(
                name, size)

    def sponsor_posts(self):
        return Post.query.filter(Post.user_id == self.id, Post.sponsor_id is not null).count()

post_hashtag = db.Table('post_hashtag',
                        db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                        db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id'))
                        )
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT)
    content = db.Column(db.TEXT)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hashtags = db.relationship('Hashtag', secondary=post_hashtag, backref='hashtags', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.content)

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'content': self.content, 'timestamp': self.timestamp,
            'sponsor': self.sponsor.name if self.sponsor is not None else '', 'hashtags': [x.content for x in self.hashtags], 'role': self.author.role,
            'author': self.author.name, 'avatar': self.author.avatar(36), 'username': self.author.username
        }


class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), index=True)
    posts = db.relationship('Post', secondary=post_hashtag, backref='posts', lazy='dynamic')

    def __repr__(self):
        return '<Hashtag {}>'.format(self.content)


