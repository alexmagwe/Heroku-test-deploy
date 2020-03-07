from datetime import datetime
from iot import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(users_id):
    return Users.query.get(int(users_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(200), unique = True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Users('{self.username}','{self.email}')"


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    IoT_name= db.Column(db.String(120), unique=True ,nullable=False)
    high = db.Column(db.Integer, nullable=False)
    off_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    low = db.Column(db.Integer, nullable=False)
    on_time= db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"Devices('{self.IoT_name}','{self.high}','{self.off_time}','{self.low}','{self.on_time}')"