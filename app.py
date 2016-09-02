#app.py

import re
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_join
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
import uuid

app = Flask(__name__)

app.secret_key = "secrets secrets are no fun"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
db.init_app(app)

Base = declarative_base()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#####################################################
##################  APP ROUTES  #####################
#####################################################

# Logout with redirect to login
@app.route("/logout")
@login_required
def logout():
    print(current_user.nickname + " being logged out")
    current_user.active = False
    db.session.commit()
    logout_user()
    print("Successfully logged out")
    return redirect('/')

# Page error handlers
@app.errorhandler(401)
def unauthorized_error(e):
    return render_template('401.html'), 401
@app.errorhandler(500)
def unauthorized_error(e):
    return render_template('500.html'), 500

# Home page redirections
@app.route("/", methods=['GET','POST'])
def login():
    if (current_user.is_anonymous == True):
        if (request.method == 'POST'):
            # Handle log in
            if(request.form.get('logEmail')):
                logEmail = request.form['logEmail']
                logPass = request.form['logPass']
                user = User.query.filter_by(email=logEmail).first()
                if (request.form.get('remember')):
                    login_user(user, remember=True)
                else:
                    login_user(user)
                return redirect('/profile/' + str(current_user.id))
            # Handle sign up
            elif (request.form.get('completeSignUp')):
                email = request.form['email']
                password = request.form['password']
                nickname = request.form['nickname']
                tagStrings = request.form['tags']
                newUser = User(email, nickname, password)
                # Find existing tags/create new tags
                tagToks = re.split('\W+', tagStrings)
                for tag in tagToks:
                    existingTag = Tag.query.filter_by(name=tag).first()
                    if (existingTag != None):
                        newUser.tags.append(existingTag)
                    else:
                        newTag = Tag(tag)
                        newUser.tags.append(newTag)
                db.session.commit()
                login_user(newUser)
                return redirect('/profile/' + str(newUser.id))
        return render_template('login.html')
    else:
        return redirect('/profile/' + str(current_user.id))

# Validate user email availibility on sign up
@app.route("/emailValidate", methods=['GET','POST'])
def emailValidate():
    email = request.args.get('email', "NoEmail", type=str)
    if (User.query.filter_by(email=email).first() != None):
        return jsonify(valid=2)
    elif (email == "NoEmail"):
        return jsonify(valid=1)
    else:
        return jsonify(valid=0)

# Validate user nickname availibility on sign up
@app.route("/nicknameValidate", methods=['GET','POST'])
def nicknameValidate():
    nickname = request.args.get('nickname', "NoName", type=str)
    if (User.query.filter_by(nickname=nickname).first() != None):
        return jsonify(valid=False)
    else:
        return jsonify(valid=True)

# Validate user login credentials on sign up
@app.route("/loginValidate", methods=['GET','POST'])
def loginValidate():
    email = request.json['email']
    password = request.json["password"]
    logUser = User.query.filter_by(email=email).first()

    print email
    print password
    print logUser

    if (logUser == None):
        print "User not found"
        return jsonify(valid=0)
    elif (logUser.password != password):
        print "Passwords don't match"
        return jsonify(valid=1)
    else:
        print "Start of user log in"
        return jsonify(valid=2)

# Page for user info display
@app.route("/profile/<int:userid>/", methods=['GET','POST'])
@login_required
def profile(userid):
    try:
        if (current_user.id == userid):
            if (request.method == 'POST'):
                # Handle change profile info
                print(request.form.get('loginButton'))
                print("EDIT PROFILE RECIEVED")
            return render_template('profile.html')
        else:
            print "GOT HERE BRUH!"
            user = User.query.filter_by(id=userid).first()
            return render_template('otherProfile.html', user=user)
    except BaseException as e:
        print e

# Page for match chats
@app.route("/matches", methods=['GET','POST'])
@app.route("/matches/<string:category>", methods=['GET','POST'])
@app.route("/matches/<int:displayConvo>", methods=['GET','POST'])
@app.route("/matches/<string:category>/<int:displayConvo>", methods=['GET','POST'])
@login_required
def matches(category="all", displayConvo=0):
    try:
        hasBuyMatches = False
        hasSellMatches = False
        index = 0
        if (current_user.matchCount != None):
            if category == "buying":
                for match in current_user.matches:
                    if current_user == match.buyer:
                        displayConvo = index
                        hasBuyMatches = True
                        break
                    index += 1
            elif category == "selling":
                for match in current_user.matches:
                    if current_user == match.seller:
                        displayConvo = index
                        hasSellMatches = True
                        break
                    index += 1
            if (request.method == 'POST'):
                # To change current chat window to another match
                if (request.form.get('index')):
                    displayConvo = int(request.form['index'])
            if (category == "buying") & (hasBuyMatches == False):
                return render_template('noMatches.html')
            elif (category == "selling") & (hasSellMatches == False):
                return render_template('noMatches.html')

            return render_template('matches.html', displayConvo=displayConvo, category=category)
        else:
            return render_template('noMatches.html')
    except BaseException as e:
        print e

# AJAX for new chat messages
@app.route('/newMessage', methods=['GET','POST'])
@login_required
def newMessage():
    message = request.json['message']
    displayConvo = int(request.json['displayConvo'])
    currMatch = current_user.matches[displayConvo]
    currMatch.newMessage(Message(message,current_user))
    newMsg = currMatch.messages[-1]
    date = str(newMsg.dateCreated.strftime('%b %d, %Y')) + " at " + str(newMsg.dateCreated.strftime('%-I:%M %p'))

    return jsonify(result=[date,message])

# Page to display items
@app.route("/items", methods=['GET','POST'])
@app.route("/items/<int:itemNum>", methods=['GET','POST'])
@login_required
def items(itemNum = 0):
    if (current_user.itemCount != None):
        if (request.method == 'POST'):
            # To change current chat window to another match
            if (request.form.get('index')):
                itemNum = int(request.form['index'])
        return render_template('items.html', itemNum=itemNum)
    else:
        # !!!        ~~~~  CHANGE REQUIRED  ~~~~~        !!!
        # CHANGE THIS TO NOITEMS.HTML
        return render_template('noMatches.html')

# Page for creating an item for current user
@app.route("/createItem", methods=['GET','POST'])
@login_required
def createItem():
    if (request.method == 'POST'):
        itemName = request.form['itemName']
        itemPrice = request.form['itemPrice']
        itemTags = request.form['itemTags']
        newItem = Item(itemName, itemPrice)
        # Add tags to item
        tagToks = re.split('\W+', itemTags)
        for tag in tagToks:
            existingTag = Tag.query.filter_by(name=tag).first()
            if (existingTag != None):
                newItem.tags.append(existingTag)
            else:
                newTag = Tag(tag)
                newItem.tags.append(newTag)
        db.session.commit()
        current_user.appendItem(newItem)
        return redirect('/items/' + str(current_user.itemCount-1))
    else:
        return render_template('createItem.html')

# Search page
@app.route("/search", methods=['GET','POST'])
@app.route("/search/<string:searchText>", methods=['GET','POST'])
@login_required
def search(searchText=None):
    if (request.method == 'POST'):
        if (request.form.get('searchText')):
            searchText = request.form['searchText']
            return redirect('/search/' + searchText)
        elif (request.form.get('add')):
            addNum = request.form['add']
            friend = User.query.filter_by(id=addNum).first()
            current_user.befriend(friend)
            return redirect('/search/' + searchText)
        elif (request.form.get('remove')):
            removeNum = request.form['remove']
            friend = User.query.filter_by(id=removeNum).first()
            current_user.unfriend(friend)
            print ("Success removed " + friend.nickname)
            return redirect('/search/' + searchText)
    else:
        if (searchText != None):
            searchResults = []
            searchPriority = []
            searchLower = []
            # Included within name match
            for user in User.query.all():
                # Exact match = highest priority
                if searchText == user.nickname:
                    searchResults.append(user)
                # Case sensitive = higher priority
                elif searchText in user.nickname:
                    searchPriority.append(user)
                # Search is in name at all = lower priority
                elif searchText.lower() in user.nickname.lower():
                    searchLower.append(user)
            # append priority search results first
            searchResults.extend(searchPriority)
            searchResults.extend(searchLower)
            return render_template('search.html', searchResults=searchResults, lastSearch=searchText, searched=True)
        return render_template('search.html', searchResults=[], searched=False)

# test page for AJAX
@app.route("/matcher", methods=['GET','POST'])
@login_required
def matcher():
    try:
        items = current_user.items
        return render_template('matcher.html', items=items)
    except BaseException as e:
        print e

# AJAX for new matches
@app.route('/newMatch', methods=['GET','POST'])
@login_required
def newMatch():
    print "NEW Match!"

    print current_user.matchCount
    item_id = request.json['item_id']
    item = Item.query.filter_by(id=item_id).first()
    current_user.match(item)
    print current_user.matchCount

    return jsonify(items=current_user.items)      

# AJAX for test page
@app.route("/noMatch", methods=['GET','POST'])
@login_required
def noMatch():
    print "NO Match!"
    return jsonify(items=current_user.items)


#####################################################
###############  DATABASE COLUMNS  ##################
#####################################################

friendship = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), index=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('User.id')),
    db.UniqueConstraint('user_id', 'friend_id', name='unique_friendships')
)
matchTable = db.Table('matches',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('match_id', db.Integer, db.ForeignKey('Match.id'))
)
matchItems = db.Table('items',
    db.Column('match_id', db.Integer, db.ForeignKey('Match.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('Item.id'))
)
userTagTable = db.Table('userTags',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'))
)
itemTagTable = db.Table('itemTags',
    db.Column('item_id', db.Integer, db.ForeignKey('Item.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'))
)

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    nickname = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    bio = db.Column(db.String(120))
    dateCreated = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    friendCount = db.Column(db.Integer)
    matchCount = db.Column(db.Integer)
    itemCount = db.Column(db.Integer)

    tags = db.relationship("Tag", secondary=userTagTable, back_populates='users')
    items = db.relationship('Item', backref='User', lazy='dynamic')
    matches = db.relationship("Match", secondary=matchTable)
    friends = db.relationship('User',
                           secondary=friendship,
                           primaryjoin=id==friendship.c.user_id,
                           secondaryjoin=id==friendship.c.friend_id)

    def __init__(self, email, nickname, password):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.dateCreated = datetime.utcnow()
        self.active = True
        db.session.add(self)
        db.session.commit()

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
            db.session.commit()

    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)
            self.updateFriendCount()
            friend.updateFriendCount()
            db.session.commit()

    def match(self, item):
        seller = item.owner
        for match in self.matches:
            if (seller == match.seller):
                if (item not in match.items):
                    match.addItem(item)
                else:
                    print "MATCH ITEM EXISTS"
                return False
        newMatch = Match(item)
        newMatch.seller = seller
        newMatch.buyer = self
        self.matches.append(newMatch)
        seller.matches.append(newMatch)
        self.updateMatchCount()
        seller.updateMatchCount()
        db.session.commit()

    def unmatch(self, match):
        if match in self.matches:
            if self == match.buyer:
                otherUser = match.seller
            else:
                otherUser = match.buyer
            otherUser.matches.remove(match)
            self.matches.remove(match)
        else:
            return False
        otherUser.updateMatchCount()
        self.updateMatchCount()
        db.session.delete(match)
        db.session.commit()

    def appendItem(self, item):
        self.items.append(item)
        self.updateItemCount()
        db.session.commit()

    def updateFriendCount(self):
        self.friendCount = len(self.friends)
        db.session.commit()

    def updateMatchCount(self):
        self.matchCount = len(self.matches)
        db.session.commit()

    def updateItemCount(self):
        self.itemCount = len(self.items.all())
        db.session.commit()

# Items are things Users are selling to other Users
class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(160), unique=True)
    price = db.Column(db.String(80))
    dateCreated = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    owner = db.relationship('User',back_populates='items', foreign_keys="Item.owner_id")
    matches = db.relationship('Match', secondary=matchItems, back_populates='items')
    tags = db.relationship('Tag', secondary=itemTagTable, back_populates='items')

    def __init__(self, name, price, owner):
        self.name = name
        self.price = price
        self.dateCreated = datetime.utcnow()
        self.owner_id = owner.id
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Item(name='%s', tags='%s', price='%s', owner='%s')>" % (
            self.name, self.tags, self.price, self.owner)

# Tags are relationships for item tags and user interests
class Tag(db.Model):
    __tablename__ = 'Tag'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    users = db.relationship('User', secondary=userTagTable, back_populates='tags')
    items = db.relationship("Item", secondary=itemTagTable, back_populates='tags')
    name = db.Column(db.String(80), unique=True)
    dateCreated = db.Column(db.DateTime)

    def __init__(self, name):
        self.name = name.lower()
        self.dateCreated = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Tag(id='%d', name='%s')>" % (self.id, self.name)

# Match conversation
class Match(db.Model):
    __tablename__ = 'Match'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    items = db.relationship("Item", secondary=matchItems, back_populates='matches')
    messages = db.relationship('Message', backref='Match', lazy='dynamic')
    lastMessage = db.Column(db.String(160))
    dateCreated = db.Column(db.DateTime)

    seller_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    seller = db.relationship("User", foreign_keys="Match.seller_id")
    buyer = db.relationship("User", foreign_keys="Match.buyer_id")

    def __init__(self, item):
        self.dateCreated = datetime.utcnow()
        self.lastMessage = "Send a message!"
        self.items.append(item)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        itemNames = []
        for item in self.items:
            itemNames.append(item.name)
        return "<Match(\n       id='%d'\n       buyer='%s'\n       seller='%s'\n       items='%s'\n       numMessages='%d')>\n" % (
            self.id, self.buyer.nickname, self.seller.nickname, itemNames, len(self.messages.all()))

    def newMessage(self, message):
        self.messages.append(message)
        self.lastMessage = message.text
        db.session.commit()

    def deleteMessage(self, message):
        self.messages.remove(message)
        db.session.delete(message)
        db.session.commit()

    def addItem(self, item):
        self.items.append(item)
        db.session.commit()

    def removeItem(self,item):
        self.items.remove(item)
        db.session.commit()

class Message(db.Model):
    __tablename__ = 'Message'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    conversation = db.Column(db.Integer, db.ForeignKey('Match.id'))
    text = db.Column(db.String(160))
    sender = db.Column(db.Integer)
    dateCreated = db.Column(db.DateTime)

    def __init__(self, text, sender):
        self.text = text
        self.sender = sender.id
        self.dateCreated = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0")




