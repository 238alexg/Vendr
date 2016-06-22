# update DB

from app import db, User, Item, Conversation, Message

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

test2.appendItem(item1)

me.befriend(test1)
me.befriend(test2)
me.befriend(test3)
me.befriend(test4)
me.befriend(test5)

me.match(test1)
me.match(test2)
me.match(test3)

db.session.add(test1)
db.session.add(test2)
db.session.add(test3)
db.session.add(test4)
db.session.add(test5)
db.session.add(item1)
db.session.add(item2)
db.session.add(item3)

me.appendItem(item1)
me.appendItem(item3)

db.session.commit()

conv1 = me.conversations[0]

conv1.newMessage(Message("Hey what's up?",me))
conv1.newMessage(Message("Not much, what about you?",test1))
conv1.newMessage(Message("Just interested in that basketball you're selling",me))
conv1.newMessage(Message("Oh sorry already sold it",test1))
conv1.newMessage(Message("Jerk.",me))

db.session.commit()

print("UPDATE SUCCESSFUL")