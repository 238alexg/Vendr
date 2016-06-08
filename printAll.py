#test python code

from app import db, User, Item

users = User.query.all()
items = Item.query.all()

print "USERS: "
for user in users:
	print user

print "ITEMS: "
for item in items:
	print item