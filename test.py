#test python code

from app import db, User, Item

users = User.query.all()

for user in users:
	print user.id
	for item in user.items:
		print ("USER: ",user," has ITEM: ",item)
