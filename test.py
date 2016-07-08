#test python code

# oneUser = User.query.filter_by(id=userid).first()
# allUsers = User.query.all()


from app import db, User, Item, Match, Message

users = User.query.all()

for match in Match.query.all():
	print (match)

oneUser = User.query.filter_by(id=6).first()

oneUserMatch = oneUser.matches[0]

oneUser.unmatch(oneUserMatch)

for match in Match.query.all():
	print (match)