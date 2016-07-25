# tests for Vendr
# The lastest and greatest in database testing/searches

# oneUser = User.query.filter_by(id=userid).first()
# allUsers = User.query.all()

from app import db, User, Item, Match, Message, Tag

def printTestOptions():
	print "TEST OPTIONS:"
	print "  0: Print test options"
	print "  1: Print user info from nickname"
	print "  2: Print all"
	print "  3: Print tag users & items"
	print " 99: END TESTS"
	return False

def printUserByNickname():
	oneUser = None
	while (oneUser == None):
		nickname = raw_input("Enter user nickname: ")
		oneUser = User.query.filter_by(nickname=nickname).first()
		if (oneUser == None):
			print "User not found."
		else:
			print "\nUSER INFO DUMP: "
			print oneUser

			print "\n- FRIENDS: "
			for friend in oneUser.friends:
				print friend

			print "\n- MATCHES: "
			for match in oneUser.matches:
				print match

			print "\n- ITEMS: "
			for item in oneUser.items:
				print item

			print "\n- TAGS: "
			for tag in oneUser.tags:
				print tag
	return False

def printAll():
	users = User.query.all()
	items = Item.query.all()
	tags = Tag.query.all()

	print "USERS: "
	for user in users:
		print user
	print "ITEMS: "
	for item in items:
		print item
	print "TAGS: "
	for tag in tags:
		print tag
	return False

def printTag():
	tag = None
	while (tag == None):
		tagName = raw_input("Enter tag name: ")
		tag = Tag.query.filter_by(name=tagName).first()
		if (tag == None):
			option = raw_input("Tag doesn't exist yet. Create tag? (Y/N)")
			if opton == "Y":
				newTag = Tag(tagName)
				db.session.add(newTag)
				db.session.commit()
				print "Tag created: "
				print newTag
			else:
				return False
		else:
			print "\TAG INFO DUMP: "
			print tag

			print "\n- USERS (" + str(len(tag.users)) + "):"
			for user in tag.users:
				print user

			print "\n- ITEMS (" + str(len(tag.items)) + "):"
			for item in tag.items:
				print item
	return False

def end():
	print "BYE BYE!"
	return True


result = printTestOptions()
while (result != True):
	testNum = int(raw_input("Test choice: "))
	print ""
	if testNum == 0:
		result = printTestOptions()
	elif testNum == 1:
		result = printUserByNickname()
	elif testNum == 2:
		result = printAll()
	elif testNum == 3:
		result = printTag()
	elif testNum == 99:
		result = end()
	else:
		print "Command not recognized. Enter 0 for options"


