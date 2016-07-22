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

@app.route("/logout")
@login_required
def logout():
    print(current_user.nickname + " being logged out")
    current_user.active = False
    db.session.commit()
    logout_user()
    print("Successfully logged out")
    return redirect('/')

@app.errorhandler(401)
def unauthorized_error(e):
    return render_template('401.html'), 401

@app.errorhandler(500)
def unauthorized_error(e):
    return render_template('500.html'), 500
    
@app.route("/", methods=['GET','POST'])
def login():
    if (current_user.is_anonymous == True):
        error = [] #render_template with param error = error in future

        if (request.method == 'POST'):
            # Handle sign in
            if(request.form.get('loginButton')):
                logEmail = request.form['logEmail']
                logPass = request.form['logPass']

                user = User.query.filter_by(email=logEmail).first()
                
                #check for username match AND email for log in
                if (user == None):
                    user = User.query.filter_by(nickname=logEmail).first()
                if (user == None):
                    error.append(3)
                    print("Account not found")
                elif (logPass != user.password):
                    error.append(4)
                    print("Incorrect password")
                # User logs in with correct credentials
                else:
                    # Remember user if remember is checked
                    if (request.form.get('remember')):
                        login_user(user, remember = True)
                    else:
                        login_user(user)
                        user.active = True
                        db.session.commit()
                    # next = flask.request.args.get('next') ??
                    return redirect('/profile/' + str(current_user.id))
            # Handle sign up
            elif (request.form.get('completeSignUp')):
                try:
                    email = request.form['email']
                    password = request.form['password']
                    confirmPass = request.form['confirmPass']
                    nickname = request.form['nickname']
                    tagStrings = request.form['tags']
                    # Errors for: password length is < 7, password fields don't match
                    #             email not in correct format, email already in use
                    if (len(password) < 7):
                        error.append(5)
                    elif (password != confirmPass):
                        error.append(1)
                    if ('@' not in email) | ('.' not in email):
                        error.append(2)
                    if (User.query.filter_by(email=email).first() != None):
                        error.append(6)
                    # If any errors thrown, render login with errors
                    if error != []:
                        return render_template('login.html', error = error)
                    # Else add user to database
                    else:
                        tagToks = re.split('\W+', tagStrings)
                        print tagToks
                        newUser = User(email, nickname, password, "This is my bio")
                        db.session.add(newUser)
                        db.session.commit()

                        for tag in tagToks:
                            existingTag = Tag.query.filter_by(name=tag).first()
                            if (existingTag != None):
                                print "EXISTING TAG: " + existingTag.name
                                newUser.tags.append(existingTag)
                            else:
                                print "NEW TAG: " + tag
                                newTag = Tag(tag)
                                db.session.add(newTag)
                                db.session.commit()
                                newUser.tags.append(newTag)
                        db.session.commit()

                        login_user(newUser)
                        return redirect('/profile/' + str(newUser.id))
                except BaseException as e:
                    print e
        return render_template('login.html', error = error)
    else:
        return redirect('/profile/' + str(current_user.id))

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

@app.route("/matches", methods=['GET','POST'])
@app.route("/matches/<int:displayConvo>/", methods=['GET','POST'])
@login_required
def matches(displayConvo = 0):
    if (current_user.matchCount != None):
        if (request.method == 'POST'):
            # To change current chat window to another match
            if (request.form.get('index')):
                displayConvo = int(request.form['index'])
            # To send a message to the current match
            elif (request.form.get('messageSend')):
                displayConvo = int(request.form['indexSend'])
                messageText = request.form['messageSend']
                currMatch = current_user.matches[displayConvo]
                currMatch.newMessage(Message(messageText,current_user))
                return redirect('matches/' + str(displayConvo))
        return render_template('matches.html', displayConvo=displayConvo)
    else:
        return render_template('noMatches.html')

# @app.route('/newMessage', methods=['GET','POST'])
# @login_required
# def newMessage(itemNum = 0):
#     print "SEND MESSAGE"
#     # To change current chat window to another match
#     # if (request.form.get('index')):
#     # displayConvo = int(request.form['index'])
#     displayConvo = request.args.get('indexSend', 0, type=int)
#     print displayConvo
#     messageText = request.args.get('messageSend', "", type=str)
#     print messageText
#     currMatch = current_user.matches[displayConvo]
#     currMatch.newMessage(Message(messageText,current_user))

#     newMsg = currMatch.messages[-1]
#     date = str(message.dateCreated.strftime('%b %d, %Y')) + "at" + str(message.dateCreated.strftime('%-I:%M %p'))
    
#     print newMsg
#     print date

#     return jsonify(date=date, message=messageText)

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

@app.route("/createItem", methods=['GET','POST'])
@login_required
def createItem():
    if (request.method == 'POST'):
        itemName = request.form['itemName']
        itemPrice = request.form['itemPrice']
        itemTags = request.form['itemTags']
        newItem = Item(itemName, itemTags, itemPrice)
        current_user.appendItem(newItem)
        return redirect('/items/' + str(current_user.itemCount-1))
    else:
        return render_template('createItem.html')

@app.route("/search/", methods=['GET','POST'])
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


@app.route("/matcher/", methods=['GET','POST'])
@login_required
def matcher():
    words = ["This","that","the other thing"]
    return render_template("matcher.html", words=words)

@app.route("/loadMatches/", methods=['GET','POST'])
@login_required
def loadMatches():
    print "GOT HERE 2"
    newWord = request.args.get('newWord', "TEST", type=str)
    print newWord
    newArray = [newWord, "Billy", "Sandra"]
    return jsonify(result=newArray)


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
    matches = db.relationship("Match", secondary=matchTable, back_populates='party')
    friends = db.relationship('User',
                           secondary=friendship,
                           primaryjoin=id==friendship.c.user_id,
                           secondaryjoin=id==friendship.c.friend_id)

    def __init__(self, email, nickname, password, bio):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.bio = bio
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
            db.session.commit()

    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)
            self.updateFriendCount()
            friend.updateFriendCount()
            db.session.commit()

    def match(self, user, item):
        for match in self.matches:
            if user in match.party:
                return False
        matchConvo = Match(item)
        matchConvo.party = [self, user]
        self.updateMatchCount()
        user.updateMatchCount()
        db.session.commit()

    def unmatch(self, match):
        if match in self.matches:
            for user in match.party:
                user.matches.remove(match)
                user.updateMatchCount()
        db.session.delete(match)
        db.session.commit()

    def appendItem(self, item):
        self.items.append(item)
        self.updateItemCount()
        db.session.commit()

    def updateFriendCount(self):
        self.friendCount = len(self.friends)

    def updateMatchCount(self):
        self.matchCount = len(self.matches)

    def updateItemCount(self):
        self.itemCount = len(self.items.all())

# Items are things Users are selling to other Users
class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.String(80))
    dateCreated = db.Column(db.DateTime)
    owner = db.Column(db.Integer, db.ForeignKey('User.id'))
    matches = db.relationship('Match', secondary=matchItems, back_populates='items')
    tags = db.relationship('Tag', secondary=itemTagTable, back_populates='items')

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.dateCreated = datetime.utcnow()

    def __repr__(self):
        return "<Item(name='%s', tags='%s', price='%s', owner='%d')>" % (
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

    def __repr__(self):
        return "<Tag(id='%d', name='%s')>" % (self.id, self.name)

# Match conversation
class Match(db.Model):
    __tablename__ = 'Match'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    party = db.relationship('User', secondary=matchTable, back_populates='matches')
    items = db.relationship("Item", secondary=matchItems, back_populates='matches')
    messages = db.relationship('Message', backref='Match', lazy='dynamic')
    lastMessage = db.Column(db.String(160))
    dateCreated = db.Column(db.DateTime)

    def __init__(self, item):
        self.dateCreated = datetime.utcnow()
        self.lastMessage = "Send a message!"
        self.items.append(item)
        db.session.commit()

    def __repr__(self):
        userNames = []
        itemNames = []
        for user in self.party:
            userNames.append(user.nickname)
        for item in self.items:
            itemNames.append(item.name)
        return "<Match(\n       id='%d'\n       party='%s'\n       items='%s'\n       numMessages='%d')>" % (
            self.id, userNames, itemNames, len(self.messages.all()))

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

if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0")




