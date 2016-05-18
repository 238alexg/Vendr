from mongoengine import *

class RideRequest(Document):
    userID = ObjectId()
    lastLoc = "Google It"
    nickname = StringField(max_length=100,required=True)
    comment = StringField(max_length="200")

    def __repr__(self):
        pickup_time_str = self.pickup_time.strftime("%I:%M").lstrip("0")
        return "ID: %s, nickname: %s, comment: %s" % (ObjectId().str, self.nickname, self.comment)
    def __str__(self):
        return self.__repr__()