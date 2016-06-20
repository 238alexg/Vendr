#test python code

from app import db, User, Item

users = User.query.all()

for user in users:
	print (user.nickname, user.friendCount, user.matchCount, user.itemCount)