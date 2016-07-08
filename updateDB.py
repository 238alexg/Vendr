# update DB

from app import db, User, Item, Match, Message

db.drop_all()
db.create_all()

# test cases
me = User("me@email.com","Alex","testtest","Me, myself and I")
test1 = User("student@u.edu","Timmy Tester","testtest","books")
test2 = User("rando@bmail.com","Tina Test","testtest","burgers")
test3 = User("noob@lolz.com","Ima Noob","testtest","being noobish")
test4 = User("nerd@u.edu","Nerd Bird","testtest","glasses")
test5 = User("cook@cook.cook","Chef Meats","testtest","Ham")

item1 = Item("Books","Learning, fun times", "$45.00")
item2 = Item("Ham","Food, pig", "$12.00")
item3 = Item("Football","Sports, fun times", "$23.00")

db.session.add(test1)
db.session.add(test2)
db.session.add(test3)
db.session.add(test4)
db.session.add(test5)
db.session.add(item1)
db.session.add(item2)
db.session.add(item3)

db.session.commit()


me.befriend(test1)
me.befriend(test2)
me.befriend(test3)
me.befriend(test4)
me.befriend(test5)

me.appendItem(item1)
me.appendItem(item2)
me.appendItem(item3)

me.match(test1, item1)
me.match(test2, item2)
me.match(test3, item3)

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


