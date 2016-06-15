#app.py

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
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

@app.route("/logout")
@login_required
def logout():
    print(current_user.nickname + " being logged out")
    logout_user()
    print("Successfully logged out")
    return redirect('/')

@app.route("/", methods=['GET','POST'])
def login():
    
    print(current_user)

    if (current_user.is_anonymous == False):
        return redirect("/profile")
    else:
        error = [] #render_template with param error = error in future

        if (request.method == 'POST'):
            # Handle sign in
            if(request.form.get('loginButton')):
                logEmail = request.form['logEmail']
                logPass = request.form['logPass']

                user = User.query.filter_by(email=logEmail).first()
                
                if (user == None):
                    error.append(3)
                    print("Email not found")
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
                    # next = flask.request.args.get('next') ??
                    return redirect('/profile')
            # Handle sign up
            elif (request.form.get('completeSignUp')):
                email = request.form['email']
                password = request.form['password']
                confirmPass = request.form['confirmPass']
                nickname = request.form['nickname']
                interests = request.form['interest']
                # If password length is < 7, error
                if (len(password) < 7):
                    error.append(5)
                # If password fields don't match, error
                elif (password != confirmPass):
                    error.append(1)
                # If email not in correct format, error
                if ('@' not in email) | ('.' not in email):
                    error.append(2)
                # If email already in use
                if (User.query.filter_by(email=email).first() != None):
                    error.append(6)
                # If any errors thrown, render login with errors
                if error != []:
                    return render_template('login.html', error = error)
                # Else add user to database
                else:
                    try:
                        newUser = User(email, nickname, password, interests)
                        db.session.add(newUser)
                        db.session.commit()
                        login_user(newUser)
                        return redirect('/profile')
                    except BaseException as e:
                        print (e)
        return render_template('login.html', error = error)

@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    if (request.method == 'POST'):
        # Handle change profile info
        print(request.form.get('loginButton'))
        print("EDIT PROFILE RECIEVED")
    return render_template('profile.html')

friendship = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), index=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('User.id')),
    db.UniqueConstraint('user_id', 'friend_id', name='unique_friendships')
)
match = db.Table('matches',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), index=True),
    db.Column('match_id', db.Integer, db.ForeignKey('User.id')),
    db.UniqueConstraint('user_id', 'match_id', name='unique_matches')
)

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    nickname = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    interests = db.Column(db.String(120))
    dateCreated = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    items = db.relationship('Item', backref='User', lazy='dynamic')
    friends = db.relationship('User',
                           secondary=friendship,
                           primaryjoin=id==friendship.c.user_id,
                           secondaryjoin=id==friendship.c.friend_id)
    matches = db.relationship('User',
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

    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)

    def match(self, match):
        if match not in self.matches:
            self.matches.append(match)
            match.matches.append(self)

    def unmatch(self, match):
        if match in self.matches:
            self.matches.remove(match)
            match.matches.remove(self)

class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    tags = db.Column(db.String(80), unique=True)
    price = db.Column(db.String(80))
    dateCreated = db.Column(db.DateTime)
    owner = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __init__(self, name, tags, price):
        self.name = name
        self.tags = tags
        self.price = price
        self.dateCreated = datetime.utcnow()

    def __repr__(self):
        return "<Item(name='%s', tags='%s', price='%s', owner='%d')>" % (
            self.name, self.tags, self.price, self.owner)

if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0")




