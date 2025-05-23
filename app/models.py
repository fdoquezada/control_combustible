from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    fuel_records = db.relationship('FuelRecord', backref='driver', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FuelRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    guide_number = db.Column(db.String(64))
    license_plate = db.Column(db.String(20))
    service_station = db.Column(db.String(100))
    supply = db.Column(db.String(50))
    kilometers = db.Column(db.Integer)
    consumption = db.Column(db.Float)
    image_filename = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def monthly_summary(self):
        return {
            'month': self.date.strftime('%Y-%m'),
            'total_consumption': sum(record.consumption for record in FuelRecord.query.filter(
                db.extract('year', FuelRecord.date) == self.date.year,
                db.extract('month', FuelRecord.date) == self.date.month,
                FuelRecord.user_id == self.user_id
            ).all()),
            'average_consumption': db.session.query(db.func.avg(FuelRecord.consumption)).filter(
                db.extract('year', FuelRecord.date) == self.date.year,
                db.extract('month', FuelRecord.date) == self.date.month,
                FuelRecord.user_id == self.user_id
            ).scalar()
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))