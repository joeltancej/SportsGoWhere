import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import Accounts
from flask_mysqldb import MySQL, MySQLdb
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import mysql.connector
from NearestFinder.nearestCarparks import *

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
    password="Wushurocks1!",
    database="sportsgowhere"
)



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
        return render_template('home.html', sports = SPORTS, locations = LOCATIONS)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/search", methods = ['POST', 'GET'])
def search():
    activity = request.args.get("activities")
    location = request.args.get("location")
    activity = SPORTS[activity]
    locationLat = LOCATIONS[location][0]
    locationLong = LOCATIONS[location][1]

    mycursor = mydb.cursor()
    sql = """select Y, X, Name, FACILITIES, ROAD_NAME, CONTACT_NO, ROUND(SQRT(
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


    return render_template('search.html', title='Search results', activity=activity, location = location, locationLat=locationLat, locationLong=locationLong, result=result, resCount=resCount)


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
    selected_facility_list = selected_facility[1:-1].split(", ")

    lat = selected_facility_list[0]
    long = selected_facility_list[1]

    return render_template('facility_info.html', selected_facility=selected_facility, selected_facility_list=selected_facility_list, lat=lat, long=long)


@app.route("/parking")
def parking():

    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))

    result = nearestCP(lat, long)

    return render_template('parking.html', lat=lat, long=long, result=result)

@app.route("/directions")
def directions():

    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    # name = float(request.args.get('name'))

    return render_template('directions.html', lat=lat, long=long)

@app.route("/search_results")
def search_results():
    return render_template('search_results.html')
