from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime
import uuid
from app import Base

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, unique=True, primary_key=True)
    email = Column(String(80), unique=True)
    nickname = Column(String(80), unique=True)
    password = Column(String(80))
    interests = Column(String(120))
    dateCreated = Column(DateTime)
    active = Column(Boolean)
    admin = Column(Boolean)
    friendCount = Column(Integer)
    matchCount = Column(Integer)
    itemCount = Column(Integer)
    items = relationship('Item', backref='User', lazy='dynamic')
    friends = relationship('User',
                           secondary=friendship,
                           primaryjoin=id==friendship.c.user_id,
                           secondaryjoin=id==friendship.c.friend_id)
    matches = relationship('User',
                           secondary=match,
                           primaryjoin=id==match.c.user_id,
                           secondaryjoin=id==match.c.match_id)

    def __init__(self, email, nickname, password, interests):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.interests = interests
        self.dateCreated = datetime.utcnow()
        self.active = True

    def __repr__(self):
        return "<User(name='%s', email='%s', password='%s')>" % (
            self.nickname, self.email, self.password)

    def is_authenticated(self):
        return self.admin

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def befriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            friend.friends.append(self)
            self.updateFriendCount()
            friend.updateFriendCount()
            session.commit()

    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)
            self.updateFriendCount()
            friend.updateFriendCount()
            session.commit()

    def match(self, match):
        if match not in self.matches:
            self.matches.append(match)
            match.matches.append(self)
            self.updateMatchCount()
            match.updateMatchCount()
            session.commit()

    def unmatch(self, match):
        if match in self.matches:
            self.matches.remove(match)
            match.matches.remove(self)
            self.updateMatchCount()
            match.updateMatchCount()
            session.commit()

    def appendItem(self, item):
        self.items.append(item)
        self.updateItemCount()
        session.commit()

    def updateFriendCount(self):
        self.friendCount = len(self.friends)

    def updateMatchCount(self):
        self.matchCount = len(self.matches)

    def updateItemCount(self):
        self.itemCount = len(self.items.all())

# Items are things Users are selling to other Users
class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(80), unique=True)
    tags = Column(String(80), unique=True)
    price = Column(String(80))
    dateCreated = Column(DateTime)
    owner = Column(Integer, ForeignKey('User.id'))

    def __init__(self, name, tags, price):
        self.name = name
        self.tags = tags
        self.price = price
        self.dateCreated = datetime.utcnow()

    def __repr__(self):
        return "<Item(name='%s', tags='%s', price='%s', owner='%d')>" % (
            self.name, self.tags, self.price, self.owner)

# Tags are relationships for item tags and user interests
class Tag(Base):
    __tablename__ = 'Tag'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(80), unique=True)

# Match conversation, which has:
# Match Comments as one-to-many relationship