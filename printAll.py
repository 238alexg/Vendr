#test python code

from app import db, User, Item, Tag

users = User.query.all()
items = Item.query.all()
tags = Tag.query.all()

# print "USERS: "
# for user in users:
# 	print user
# print "ITEMS: "
# for item in items:
# 	print item
# print "TAGS: "
# for tag in tags:
# 	print tag

print "User tags: "
for user in users:
	print (user.nickname, len(user.tags))
	for tag in user.tags:
		print tag

for tag in tags:
	print (tag.name, len(tag.users), len(tag.items))
	for user in tag.users:
		print user