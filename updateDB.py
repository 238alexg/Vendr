# update DB

from app import db, User, Item

db.drop_all()
db.create_all()

# test cases
test1 = User("student@u.edu","Timmy Tester","test","books")
test2 = User("rando@bmail.com","Tina Test","test","kinky shit")
item1 = Item("Books", "Learning, fun times", "$45.00")

db.session.add(test1)
db.session.add(test2)
db.session.add(item1)
db.session.commit()

print("UPDATE SUCCESSFUL")