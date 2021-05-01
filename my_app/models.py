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


# Run migrations
db.create_all()
