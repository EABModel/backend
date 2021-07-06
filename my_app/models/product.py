from my_app import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String(150), primary_key=True)
    shopId = db.Column(db.String(150), db.ForeignKey(
        'shop.id'), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    os = db.Column(db.String(300), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    inches = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "shopId": self.shopId,
            "name": self.name,
            "brand": self.brand,
            "os": self.os,
            "color": self.color,
            "inches": self.inches,
            "price": self.price,
            "image": self.image
        }

    @staticmethod
    def load_product(product_id):
        return Product.query.get(str(product_id)).serialize()

    @staticmethod
    def load_shops_products(shopId):
        unserialized_products = Product.query.filter_by(
            shopId=str(shopId)).all()
        return [product.serialize() for product in unserialized_products]

    def __repr__(self):
        return f"Product('{self.id}', '{self.name}', '{self.brand}')"
