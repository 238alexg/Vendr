#test python code

from app import db, User

users = User.query.all()

print(users)