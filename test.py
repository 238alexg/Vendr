#test python code

from app import db, User, Item, Conversation, Message

users = User.query.all()

for user in users:
	print (user.nickname)
	for convo in user.conversations:
		print (convo)