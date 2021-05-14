from my_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id)).serialize()

@login_manager.user_loader
def load_user_by_email(email):
    return User.query.filter_by(email=str(email)).first().serialize()

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    sessionType = db.Column(db.String(20), nullable=False)
    authToken = db.Column(db.String(300), nullable=True)
    refreshToken = db.Column(db.String(300), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "sessionType": self.sessionType,
            "authToken": self.authToken,
            "refreshToken": self.refreshToken
        }

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"

class Shop(db.Model):
    id = db.Column(db.String(150), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
        }

    def __repr__(self):
        return f"Shop('{self.id}', '{self.name}', '{self.location}')"

class Product(db.Model):
    id = db.Column(db.String(150), primary_key=True)
    shopId = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    os = db.Column(db.String(300), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    inches = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "shopId": self.shopId,
            "name": self.name,
            "brand": self.brand,
            "os": self.os,
            "color": self.color,
            "inches": self.inches,
            "price": self.price
        }

    def __repr__(self):
        return f"Product('{self.id}', '{self.name}', '{self.brand}')"


# Run migrations
db.create_all()
