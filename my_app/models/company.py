from my_app import db


class Company(db.Model):
    id = db.Column(db.String(150), primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def load_company(company_id):
        return Company.query.get(str(company_id)).serialize()

    @staticmethod
    def load_company_by_name(name):
        return Company.query.filter_by(name=str(name)).first()

    def __repr__(self):
        return f"Company('{self.id}', '{self.name}')"


db.create_all()
