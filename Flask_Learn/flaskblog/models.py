from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))


class Accounts(UserMixin, db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)
    username = db.Column(db.String(20), nullable=False)

    favorites_list = db.relationship('Favorites', backref='user')

    def __repr__(self):
        return f"Accounts('{self.email}', '{self.username}')"

class SportsFacilities(db.Model):
    __tablename__ = 'sportsfacilities'
    gid = db.Column(db.Integer, primary_key=True)
    X = db.Column(db.Float)
    Y = db.Column(db.Float)
    Name = db.Column(db.Text)
    description = db.Column(db.Text)
    FACILITIES = db.Column(db.Text)
    ROAD_NAME = db.Column(db.Text)
    CONTACT_NO = db.Column(db.Text)
    GYM = db.Column(db.Text)
    INC_CRC = db.Column(db.Text)
    FMEL_UPD_D = db.Column(db.Float)
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('sportsfacilities.gid'), primary_key=True)

    # add a relationship to the Accounts model
    account = db.relationship('Accounts', backref=db.backref('favorites', lazy='dynamic'))

    def __init__(self, account_id, facility_id):
        self.account_id = account_id
        self.facility_id = facility_id


class RecentSearches(db.Model):
    __tablename__ = 'recentsearches'
    raccount_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), primary_key=True)
    rfacility_id = db.Column(db.Integer, db.ForeignKey('sportsfacilities.gid'), primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"RecentSearches('{self.raccount_id}', '{self.rfacility_id}', '{self.timestamp}')"