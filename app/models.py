from app import db, bcrypt
from flask_login import UserMixin
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user = db.relationship('User', backref='carts')
    dog = db.relationship('Dog', backref='carts')



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user = db.relationship('User', backref='orders')
