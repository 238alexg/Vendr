#app.py

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, login_required
from datetime import datetime
import uuid

app = Flask(__name__)

app.secret_key = "secrets secrets are no fun"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.setup_app(app)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    print("You were logged out")
    return redirect('/login')

@app.route("/", methods=['GET','POST'])
def login():
    error = [] #render_template with param error = error in future
    if (request.method == 'POST'):
        print("BUTTON PRESSED")

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
                print("REMEMBER LOG IN")
                login_user(user, remember = True)
            else:
                print("NO REMEMBER LOG IN")
                login_user(user)
                # next = flask.request.args.get('next')
            return render_template('index.html', nickname=user.nickname, interests=user.interests)

    return render_template('login.html', error = error)

@app.route("/createAccount", methods=['POST'])
def createProfile():
    
    error = []

    # Get all signup form fields
    if (request.method == 'POST'):
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

        # If any errors thrown, render login with errors
        if error != []:
            return render_template('login.html', error = error)
        # Else add user to database
        else:
            newUser = User(email, nickname, password, interests)
            db.session.add(newUser)
            db.session.commit()
            return render_template('createAccount.html', nickname=nickname, interests=interests)


@app.route("/profile", methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')

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
    # friends = db.relationship('User', secondary=friendship, 
    #                             primaryjoin=id==friendship.c.friend_a_id,
    #                             secondaryjoin=id==friendship.c.friend_b_id)

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


if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0")




