from my_app import db


class Shop(db.Model):
    id = db.Column(db.String(150), primary_key=True)
    companyId = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "companyId": self.companyId,
            "name": self.name,
            "location": self.location
        }

    @staticmethod
    def load_shop(shop_id):
        return Shop.query.get(str(shop_id)).serialize()

    @staticmethod
    def load_shops(company_id):
        unserialized_shops = Shop.query.filter_by(companyId=str(company_id)).all()
        return [shop.serialize() for shop in unserialized_shops]

    def __repr__(self):
        return f"Shop('{self.id}', '{self.name}', '{self.location}')"


db.create_all()
