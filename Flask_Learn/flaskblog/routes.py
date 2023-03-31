import os
import secrets
from PIL import Image
import json
from flask import render_template, url_for, flash, redirect, session, request
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import Accounts, Favorites, SportsFacilities, RecentSearches
from flask_mysqldb import MySQL, MySQLdb
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import mysql.connector
from NearestFinder.nearestCarparks import *
from NearestFinder.nearestEateries import *
from NearestFinder.geoloc import *
from datetime import timedelta
from flaskblog.apimanagers import *
from pytz import timezone
from sqlalchemy.exc import IntegrityError
import datetime
import ast

tz = timezone('Asia/Singapore')  # set the timezone to Singapore time

SPORTS = {
    'Badminton': 'Sports Hall',
    'Basketball': 'Sports Hall',
    'Football': 'Stadium',
    'Futsal': 'Futsal',
    'Gym': 'Gym',
    'Hockey': 'Hockey',
    'Netball': 'Sports Hall', 
    'Running': 'Stadium',
    'Squash': 'Squash',
    'Swimming': 'Swimming', 
    'Tennis': 'Tennis Centre', 
}

LOCATIONS = {
    'ANG MO KIO': [1.3690491614585905, 103.84617662205791],
    'BEDOK': [1.323753876830021, 103.92747988227394],
    'BISHAN': [1.3527095239371663, 103.83487455556293],
    'BUKIT BATOK': [1.3589929677978048, 103.76468959616123],
    'BUKIT MERAH': [1.2819985061957189, 103.82404636322299],
    'BUKIT PANJANG': [1.3774071542249358, 103.77262807405172],
    'BUKIT TIMAH': [1.3296203145827528, 103.8014919349198],
    'CENTRAL AREA': [1.3556114305355844, 103.8685252584247],
    'CHOA CHU KANG': [1.383595915929974, 103.74736775188698],
    'CLEMENTI': [1.3163527247327258, 103.76361384574014],
    'GEYLANG': [1.3198669883135887, 103.89096164542512],
    'HOUGANG': [1.3616095354801252, 103.88564750275046],
    'JURONG EAST': [1.3331177503052059, 103.74224177362655],
    'JURONG WEST': [1.3404037339836228, 103.70762392935701],
    'KALLANG/WHAMPOA': [1.3100572199069005, 103.86537010275725],
    'MARINE PARADE': [1.3021725626741638, 103.89667221080559],
    'PASIR RIS': [1.3722133204648286, 103.94715237268906],
    'PUNGGOL': [1.3985842176940457, 103.90686891552899],
    'QUEENSTOWN': [1.2950155130052179, 103.78726592256501],
    'SEMBAWANG': [1.4496527897849414, 103.81835058481245],
    'SENGKANG': [1.387524817888245, 103.89016697111667],
    'SERANGOON': [1.3500985388379187, 103.87131077596565],
    'TAMPINES': [1.354082646900409, 103.94388853511829],
    'TOA PAYOH': [1.3345022819925925, 103.85611284427664], 
    'WOODLANDS': [1.4379172007989964, 103.78951816040572],
    'YISHUN': [1.4307833017382476, 103.83613078444286],
    'NORTH': [1.4303502008219373, 103.79983165130324],
    'SOUTH': [1.2992761595279543, 103.82034860814527],
    'EAST': [1.3521733297485963, 103.93717682823622], 
    'WEST': [1.351326983979124, 103.71833556089194]
}

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="sportsgowhere"
)

# secret key
app.secret_key = "sportsgowhere"
# session lifetime
app.permanent_session_lifetime = timedelta(minutes = 10)

SEARCH = {}

ACTIVITY = ""
LOCATION = ""
LOCATION_LAT = ""
LOCATION_LONG = ""

@app.route("/")
@app.route("/home", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        ACTIVITY = request.args.get("activities")
        LOCATION = request.args.get("location")
        return redirect(url_for('search', sports = SPORTS, locations = LOCATIONS))
    else: 
        session["loc"] = "region"
        return render_template('home.html', sports = SPORTS, locations = LOCATIONS)
    
@app.route("/currentloc", methods = ['POST', 'GET'])
def currentloc():
    if request.method == 'POST':
        ACTIVITY = request.args.get("activities")
        LOCATION = request.args.get("location")
        return redirect(url_for('search', sports = SPORTS, locations = LOCATIONS))
    else: 
        session["loc"] = "user"
        lat, long = getgeoloc()
        session["lat"] = lat
        session["long"] = long
        return render_template('currentloc.html', sports = SPORTS, locations = LOCATIONS, lat=lat, long=long)
    
@app.route("/secondloc")
def secondloc():
    firstlocation = request.args.get("location")
    sport = request.args.get("activities")

    return render_template('secondloc.html', sport=sport, firstlocation=firstlocation, locations=LOCATIONS)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/search2loc", methods=['POST', 'GET'])
def search2loc():
    activity = request.args.get("activities")
    activity = SPORTS[activity]
    firstlocation = request.args.get("firstlocation")
    secondlocation = request.args.get("secondlocation")
    if session["loc"] == "region":
        locationLat1 = LOCATIONS[firstlocation][0]
        locationLong1 = LOCATIONS[firstlocation][1]
    else:
        locationLat1 = session["lat"]
        locationLong1 = session["long"]
    locationLat2 = LOCATIONS[secondlocation][0]
    locationLong2 = LOCATIONS[secondlocation][1]
    locationLat, locationLong = float((locationLat1+locationLat2)/2), float((locationLong1+locationLong2)/2)
    mycursor = mydb.cursor()
    sql = """select Y, X, gid, Name, FACILITIES, ROAD_NAME, CONTACT_NO, ROUND(SQRT(
	POW(69.1 * (Y - %s), 2) +
    POW(69.1 * (%s - X) * COS(Y / 57.3), 2)) * 1.60934, 2) as distance
    from sportsfacilities
    where FACILITIES like "%""" + activity +"""%"
    order by distance
    limit 20;"""
    
    value = (locationLat, locationLong)
    mycursor.execute(sql, value)
    result = mycursor.fetchall()

    resCount = 0
    for i in result:
        resCount += 1


    return render_template('search.html', title='Search results', activity=activity, locationLat=locationLat, locationLong=locationLong, result=result, resCount=resCount)

@app.route("/search", methods = ['POST', 'GET'])
def search():
    activity = request.args.get("activities")
    activity = SPORTS[activity]
    if session["loc"] == "region":
        location = request.args.get("location")
        locationLat = LOCATIONS[location][0]
        locationLong = LOCATIONS[location][1]
    else:
        locationLat = session["lat"]
        locationLong = session["long"]

    mycursor = mydb.cursor()
    sql = """select Y, X, gid, Name, FACILITIES, ROAD_NAME, CONTACT_NO, ROUND(SQRT(
	POW(69.1 * (Y - %s), 2) +
    POW(69.1 * (%s - X) * COS(Y / 57.3), 2)) * 1.60934, 2) as distance
    from sportsfacilities
    where FACILITIES like "%""" + activity +"""%"
    order by distance
    limit 20;"""
    
    value = (locationLat, locationLong)
    mycursor.execute(sql, value)
    result = mycursor.fetchall()

    resCount = 0
    for i in result:
        resCount += 1


    return render_template('search.html', title='Search results', activity=activity, locationLat=locationLat, locationLong=locationLong, result=result, resCount=resCount)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Accounts(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Accounts.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Accounts.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/facility_info", methods=['GET', 'POST'])
def facility_info():
    selected_facility = request.args.get('type')
    source = request.args.get('source')  # retrieve the source parameter
    if source == 'favorites' or source == 'recentsearches':
        # Convert the selected_facility to int
        selected_facility_str = str(selected_facility)
        facility_gid = selected_facility_str.split()[1][:-1]
        # Convert gid string to integer
        facility_gid = int(facility_gid.strip('<>SportsFacilities '))

        # Query SportsFacilities table to get matching facility
        facility = SportsFacilities.query.filter_by(gid=facility_gid).first()

        # Convert facility attributes to a list
        selected_facility_list = [facility.X, facility.Y, facility.gid, '"' + facility.Name + '"', facility.description, facility.FACILITIES, facility.ROAD_NAME, '"' + facility.CONTACT_NO + '"', facility.GYM, facility.INC_CRC, facility.FMEL_UPD_D]
    elif source == 'save_favorite':
        selected_facility_list = request.args.get('selected_facility_list').split('|')
        
    else:
        selected_facility_list = selected_facility[1:-1].split(", ")

    lat = selected_facility_list[0]
    long = selected_facility_list[1]
    gid = selected_facility_list[2]

    timestamp = datetime.datetime.now(tz=tz)  # create a datetime object with the specified timezone
    if current_user.is_authenticated:
        user_id = current_user.id
        # Insert new record into recentsearches, or update timestamp if a record with the same primary key exists
        try:
            recent_search = RecentSearches(raccount_id=user_id, rfacility_id=gid, timestamp=timestamp)
            db.session.add(recent_search)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            existing_search = RecentSearches.query.filter_by(raccount_id=user_id, rfacility_id=gid).first()
            existing_search.timestamp = timestamp
            db.session.commit()
        # Check number of recent searches for the user
        num_recent_searches = RecentSearches.query.filter_by(raccount_id=user_id).count()

        # If the number of recent searches exceeds 5, delete the excess records
        if num_recent_searches > 5:
            excess_searches = RecentSearches.query.filter_by(raccount_id=user_id).order_by(RecentSearches.timestamp.asc()).limit(num_recent_searches - 4).all()
            for search in excess_searches:
                db.session.delete(search)
            db.session.commit()

    session['lat'] = lat
    session['long'] = long
    session['selected_facility_list'] = selected_facility_list
    airquality, airdescriptor, airadvisory, psiarea= getpsi(selected_facility_list[0], selected_facility_list[1])

    region, forecast = getcurweather(selected_facility_list[0], selected_facility_list[1])

    return render_template('facility_info.html', selected_facility=selected_facility, selected_facility_list=selected_facility_list, 
                           lat=lat, long=long, airquality=airquality, airdescriptor=airdescriptor, airadvisory=airadvisory, 
                           psiarea=psiarea, forecast=forecast, region=region)


@app.route("/parking", methods=['GET', 'POST'])
def parking():

    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))

    result = nearestCP(lat, long)

    return render_template('parking.html', lat=lat, long=long, result=result)

@app.route("/eateries", methods=['GET', 'POST'])
def eateries():

    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))

    result = nearestHE(lat, long)


    return render_template('eateries.html', lat=lat, long=long, result=result)

@app.route("/eaterymap", methods=['GET', 'POST'])
def eaterymap():
    name = request.args.get('name')
    street = request.args.get('st')

    return render_template('eaterymap.html', name=name, street=street)

@app.route("/directions")
def directions():

    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    clat, clong = getgeoloc()
    # name = float(request.args.get('name'))

    return render_template('directions.html', lat=lat, long=long, clat=clat, clong=clong)

@app.route("/parking_info", methods=['GET', 'POST'])
def parking_info():

    res = request.args.get('type')
    resdic = ast.literal_eval(res)
    name = resdic['address']
    name = (name.split('/'))[0]
    cpno = resdic['cpno']
    availability = getcarparkinfo(cpno)

    return render_template('parking_info.html', res=res, name=name, availability=availability, cpno=cpno)

@app.route("/search_results")
def search_results():
    return render_template('search_results.html')


@app.route('/save_favorite', methods=['POST'])
@login_required
def save_favorite():
    facility_gid = request.form['selected_facility_list_gid']
    is_favorite = request.form.get('is_favorite', False)
    account_id = current_user.id

    # Get the facility ID from the SportsFacilities table using the facility_gid
    facility = SportsFacilities.query.filter_by(gid=facility_gid).first()
    if facility is None:
        flash('Facility not found.', 'danger')
        return redirect(url_for('home'))
    
    facility_id = facility.gid

    # Check if the record already exists in the favorites table
    existing_favorite = Favorites.query.filter_by(account_id=account_id, facility_id=facility_id).first()
    
    if is_favorite:
        if not existing_favorite:
            # Insert a new record if it doesn't exist
            favorite = Favorites(account_id=account_id, facility_id=facility_id)
            db.session.add(favorite)
            db.session.commit()
            flash('The facility has been added to your favorites!', 'success')
        else:
            flash('The facility is already in your favorites!', 'danger')
    else:
        if existing_favorite:
            # Delete the existing record if it exists
            db.session.delete(existing_favorite)
            db.session.commit()
            flash('The facility has been removed from your favorites.', 'success')
        else:
            flash('The facility is not in your favorites!', 'danger')

    lat = session.get('lat')
    long = session.get('long')
    selected_facility_list = session.get('selected_facility_list')
    selected_facility_list = [str(elem) for elem in selected_facility_list]
    return redirect(url_for('facility_info', selected_facility_list='|'.join(selected_facility_list), source='save_favorite'))


@app.route('/favorites')
@login_required
def favorites():
    user_id = current_user.id
    favorites = Favorites.query.filter_by(account_id=user_id).all()

    facilities = []
    for favorite in favorites:
        facility = SportsFacilities.query.filter_by(gid=favorite.facility_id).first()
        if facility:
            facilities.append(facility)

    return render_template('favorites.html', title='Favorites', facilities=facilities, source='favorites')


@app.route('/recentsearches')
@login_required
def recentsearches():
    user_id = current_user.id
    recentsearches = RecentSearches.query.filter_by(raccount_id=user_id).all()

    facilities = []
    for recentsearch in recentsearches:
        facility = SportsFacilities.query.filter_by(gid=recentsearch.rfacility_id).first()
        if facility:
            facilities.append(facility)

    return render_template('recentsearches.html', title='Recent Searches', facilities=facilities, source='recentsearches')

@app.route('/weather_24h')
def weather_24h():
    weather = get24hweather()
    return render_template('weather_24h.html', weather=weather)

@app.route('/weather_4day')
def weather_4day():
    weather, dates, temp = get4dayweather()
    return render_template('weather_4day.html', weather=weather, dates=dates, temp=temp)

@app.route('/psi')
def psi():
    regions, readings = getfullpsi()
    return render_template('psi.html', regions=regions, readings=readings)