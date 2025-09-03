from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    watchlist_items = db.relationship("WatchlistItem", backref="user", lazy=True)
    watched_items = db.relationship("WatchedItem", backref="user", lazy=True)


class WatchlistItem(db.Model):
    __tablename__ = "watchlist_item"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100))
    rating = db.Column(db.String(50))
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class WatchedItem(db.Model):
    __tablename__ = "watched_item"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100))
    rating = db.Column(db.String(50))
    comment = db.Column(db.Text)
    my_rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)