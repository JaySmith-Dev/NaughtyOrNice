from datetime import datetime

# from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

# Simple model joining a children table to their wishlist.
class Children(db.Model):
    __tablename__ = 'children'
    child_id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String)
    age = db.mapped_column(db.Integer)
    gender = db.mapped_column(db.String)
    address = db.mapped_column(db.String)
    list_status = db.mapped_column(db.String(7))


class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    wish_id = db.mapped_column(db.Integer, primary_key=True)
    item = db.mapped_column(db.String)

    child_id = db.mapped_column(db.Integer, db.ForeignKey('children.child_id'), nullable=False)
    child = db.relationship('Children', backref=db.backref('wishlist', lazy=True, cascade='all, delete-orphan'))
