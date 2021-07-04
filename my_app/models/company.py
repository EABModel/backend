from my_app import db


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.String(150), primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    shops = db.relationship('Shop', backref='company', lazy=True)
    users = db.relationship('User', backref='company', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def load_company(company_id):
        return Company.query.get(str(company_id)).serialize()

    @staticmethod
    def load_company_by_name(name):
        return Company.query.filter_by(name=str(name)).first()

    def __repr__(self):
        return f"Company('{self.id}', '{self.name}')"
