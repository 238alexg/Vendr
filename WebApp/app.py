#app.py

from flask import Flask, render_template, request as req, url_for
from flask.ext.mongoengine import MongoEngine
from werkzeug.contrib.fixers import ProxyFix
from datetime import datetime
from auth import requires_auth

from mongo.db import save_ride, get_ride_list, delete_ride, delete_all, validate


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.config["MONGODB_SETTINGS"] = {'DB': "saferide"}
app.config["SECRET_KEY"] = "thisisasecret"

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
	return render_template('index.html')

@app.route("/admin", methods=['GET', 'POST'])
@requires_auth
def admin():
    if req.form:
        #Need to delete ride
        ride_id = req.form.get("id")
        print("Deleting ride with id:", ride_id)
        if ride_id:
            delete_ride(ride_id)

        delAll = req.form.get("delBut")
        print("Deleting all rides")
        if delAll:
            try:
                delete_all()
            except BaseException as e:
                print (e)
    rides = get_ride_list()
    return render_template('admin.html', rides=rides)

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/request")
def ask():
    try:
        return render_template('request.html',ride={}, errors={})
    except BaseException as e:
        print(e)
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/suc")
def suc():
    return render_template('success.html')

@app.route('/buttonPress', methods=['POST'])
def buttonPress():
    print("BUTTON HAS BEEN PRESSED")
    name = req.form.get('usr').encode('utf-8')
    print(name, type(name))

    uoid = req.form.get('id')
    if uoid:
        uoid = uoid.encode('utf-8')
        uoid = int(uoid)
    print(uoid, type(uoid))

    phone = req.form.get('phone').encode('utf-8')
    print(phone, type(phone))

    pickup = req.form.get('pick_up').encode('utf-8')
    print(pickup, type(pickup))

    dropoff = req.form.get('drop_off').encode('utf-8')
    print(dropoff, type(dropoff))
    
    new_hour = int(req.form.get('hours').encode('utf-8'))
    print(new_hour, type(new_hour))

    new_minute = int(req.form.get('minute').encode('utf-8'))
    print(new_minute, type(new_minute))

    numRiders = int(req.form.get('riders').encode('utf-8'))
    print(numRiders, type(numRiders))

    specRequests = req.form.get('spec').encode('utf-8')
    print(specRequests, type(specRequests))
	# print("unexpected indent")

    # Set the pickup time to the one on the form
    pick_time = datetime.now()
    #print(pick_time)
    updated_time = pick_time.replace(hour=new_hour, minute=new_minute, second=0, microsecond=0)
    #print(updated_time)
    ride = {"name":name,"phone":phone,"uoid":uoid,"pickup_addr":pickup,"pickup_time":updated_time,"dropoff_addr":dropoff,"group_size":numRiders,"special":specRequests}    
    print("Gonna validate")
    errors = validate(ride)
    if not errors:
        print("success, saving ride")
        save_ride(ride)
        return render_template('success.html') 
    else:
        print("uh oh, errors")
        print(errors)
        return render_template("request.html",ride=ride, errors=errors)
    

if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0")
