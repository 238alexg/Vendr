# update DB

################################################
#
# NOW JUST FOR RESETTING THE ENTIRE DB
#
# WHICH YOU SHOULD NEVER DO UNLESS
#
# THE WORLD IS ENDING AND YOU WANT A THRILL
#
################################################

from app import db, User, Item, Match, Message, Tag

users = User.query.all()
items = Item.query.all()
matches = Match.query.all()
messages = Message.query.all()
tags = Tag.query.all()

# db.drop_all()
# db.create_all()

# test cases
me = User("me@email.com","Alex","testtest")
test1 = User("student@u.edu","Timmy Tester","testtest")
test2 = User("rando@bmail.com","Tina Test","testtest")
test3 = User("noob@lolz.com","Ima Noob","testtest")
test4 = User("nerd@u.edu","Nerd Bird","testtest")
test5 = User("cook@cook.cook","Chef Meats","testtest")

item1 = Item("Books", "$45.00", test1)
item2 = Item("Ham", "$12.00", test2)
item3 = Item("Football", "$23.00", test3)
item4 = Item("Rubbish", "$1.00", test4)
item5 = Item("Rubbish1", "$1.00", me)
item6 = Item("Rubbish2", "$1.00", me)

tag1 = Tag("Learning")
tag2 = Tag("Sports")
tag3 = Tag("Cooking")

me.befriend(test1)
me.befriend(test2)
me.befriend(test3)
me.befriend(test4)
me.befriend(test5)

me.match(item1)
me.match(item2)
me.match(item3)

test1.match(item5)

me.tags.append(tag1)
me.tags.append(tag2)
me.tags.append(tag3)

# db.session.commit()

conv1 = me.matches[0]

conv1.addItem(item2)

conv1.newMessage(Message("Hey what's up?",me))
conv1.newMessage(Message("Not much, what about you?",test1))
conv1.newMessage(Message("Just interested in that basketball you're selling",me))
conv1.newMessage(Message("Oh sorry already sold it",test1))
conv1.newMessage(Message("Jerk.",me))

conv2 = me.matches[1]

conv2.newMessage(Message("Hey! Saw that listing for a flower pot. I've never had one before, how much?",me))
conv2.newMessage(Message("$50 or no dice",test2))
conv2.newMessage(Message("I've got a satchel full of paperclips",me))
conv2.newMessage(Message("Meet me at 13th and Olive at 8 and we've got a deal",test2))
conv2.newMessage(Message(":)",me))
conv2.newMessage(Message("Hey this is a really long message why don't you see if it will extend past where it is due? Time to repeat! Hey this is a really long message why don't you see if it will extend past where it is due? Time to repeat!",test2))
conv2.newMessage(Message("Hey this is a really long message why don't you see if it will extend past where it is due? Time to repeat! Hey this is a really long message why don't you see if it will extend past where it is due? Time to repeat!",me))

db.session.commit()

print("UPDATE SUCCESSFUL")


