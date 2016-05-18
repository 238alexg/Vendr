from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime
import uuid
from app import db

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Unicode, unique=True, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    nickname = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    interests = db.Column(db.String(120))
    dateCreated = db.Column(db.DateTime)
    # friends = db.relationship('User', backref='User', lazy='dynamic')

    def __init__(self, email, nickname, password, interests):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.interests = interests
        self.dateCreated = datetime.utcnow()
        self.id = uuid.uuid1()

    def __repr__(self):
        return "<User(name='%s', email='%s', password='%s')>" % (
            self.nickname, self.email, self.password)

    def is_authenticated():
    	return True

   	def is_active():
   		return False

   	def is_anonymous():
   		return False

   	def get_id():
   		return self.id


# class Item(db.Model):
#     __tablename__ = 'Item'
#     name = db.Column(db.String(80), primary_key = True)
#     owner = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
#     price = db.Column(db.Float)
#     comments = db.Column(db.String(120))

#     def __init__(self, name, owner, price, comments):
#         self.owner = owner
#         self.name = name
#         self.price = price
#         self.comments = comments

#     def __repr__(self):
#         return '<Owner %r, item: %r, >' % (self.owner.nickname, self.name)