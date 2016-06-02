#test python code

from app import db, User

users = User.query.all()

for user in users:
	print user