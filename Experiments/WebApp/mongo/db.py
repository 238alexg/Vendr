from mongoengine import connect
from .models import RideRequest
from datetime import datetime
import operator, re
connect('saferide')


r = RideRequest(name="Rider", uoid=951000000, pickup_time=datetime.now(),
                    pickup_addr="Some place",
                    dropoff_addr="Other place", group_size=3)

phone_re = re.compile("\d{10}")

def validate(ride):
    errors = {}
    if type(ride) == dict:
        uoid = ride.get("uoid")
        if not uoid:
              errors['uoid'] = "UOID is required."
	elif uoid < 950000000 or uoid > 959999999:
              errors['uoid'] = "Invalid UOID."

        phone = ride.get("phone")
        if not phone:
              errors['phone'] = "Phone is required."
        elif not phone_re.match(phone):
              errors['phone'] = "Invalid phone number."
        
        if not ride.get("name") or ride.get("name") == "":
              errors['name'] = "Name is required."
  
        if not ride.get("pickup_addr"):
              errors['pickup_addr'] = "Pickup location is required."
        
        if not ride.get("dropoff_addr"):
              errors['dropoff_addr'] = "Dropoff location is required."

	if not ride.get("group_size"):
              errors['group_size'] = "Group size is required."

              
    return errors

def save_ride(ride):
    if type(ride) == RideRequest:
        print("saving the ride object")
        ride.save()
        return ride
    elif type(ride) == dict:
        print("saving the ride dict", ride)
        try:
            r = RideRequest(**ride)
            r.save()
	except BaseException as e:
            print(e)
        print("save successful")
        return r
    else:
        print("Error saving ride", type(ride))
        return None

def delete_ride(ride_id):
    ride = RideRequest.objects(id=ride_id)
    if ride:
        ride.delete()
        return True
    else:
        return False

def delete_all():
    for r in RideRequest.objects:
        r.delete()
    print("PASS")

def list_rides():
    for r in RideRequest.objects:
        print(r)

def get_ride_list(sort=None):
    return sorted(RideRequest.objects, key=operator.itemgetter(sort if sort else "pickup_time"))

# save_ride(r)
# list_rides()
