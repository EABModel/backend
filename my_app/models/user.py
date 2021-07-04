from my_app import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.String(150), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    sessionType = db.Column(db.String(20), nullable=False)
    companyId = db.Column(db.String(150), db.ForeignKey('company.id'), nullable=False)
    shopId = db.Column(db.String(150), db.ForeignKey('shop.id'))

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "sessionType": self.sessionType,
            "companyId": self.companyId,
            "shopId": self.shopId,
        }

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(str(user_id)).serialize()

    @staticmethod
    @login_manager.user_loader
    def load_user_by_email(email):
        return User.query.filter_by(email=str(email)).first()

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', {self.companyId}, {self.shopId})"
