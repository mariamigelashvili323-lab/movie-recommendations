


from datetime import datetime
from ext import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="User")
    gender = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True, default="default_1.jpg")

class MovieCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(300), nullable=True, default='default_image.jpg')
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_card.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('my_movies', lazy=True))
    movie = db.relationship('MovieCard', backref=db.backref('added_by_users', lazy=True))

class UserRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_card.id'), nullable=False)
    comment = db.Column(db.Text, nullable=True)

    movie = db.relationship('MovieCard', backref='recommendations')
