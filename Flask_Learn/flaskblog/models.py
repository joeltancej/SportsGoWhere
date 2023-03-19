from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))


class Accounts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)
    username = db.Column(db.String(20), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Accounts.query.get(user_id)

    def __repr__(self):
        return f"Accounts('{self.email}', '{self.username}')"
