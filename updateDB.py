# update DB

from app import db, User

db.drop_all()
db.create_all()

# test cases
test1 = User("student@u.edu","Timmy Tester","test","books")
test2 = User("rando@bmail.com","Tina Test","test","kinky shit")

db.session.add(test1)
db.session.add(test2)
db.session.commit()

users = User.query.all()

print(test1)
print(test2)
print(users)