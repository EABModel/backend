from my_app.models import shop
from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.product import Product
import uuid


@app.route('/catalogue/add-single-product', methods=['POST'])
@cache.cached(timeout=50)
def create_product():
    id = uuid.uuid4()
    product = Product(
        id=id,
        shopId=request.json['shopId'],
        name=request.json['name'],
        brand=request.json['brand'],
        os=request.json['os'],
        color=request.json['color'],
        inches=request.json['inches'],
        price=request.json['price']
    )
    db.session.add(product)
    db.session.commit()
    product = Product.load_product(str(id))
    return make_response(jsonify(product), 201)


@app.route('/catalogue', methods=['GET'])
@cache.cached(timeout=50)
def get_catalogue():
    unserialized_products = Product.query.all()
    serialized_products = [product.serialize()
                           for product in unserialized_products]
    return make_response(jsonify(serialized_products))


@app.route('/catalogue/product', methods=['GET'])
def get_product():
    product = Product.query.get(str(request.args.get('productId')))
    if product:
        return make_response(jsonify(product.serialize()))
    return {}


@app.route('/catalogue/shop', methods=['GET'])
def get_shop_catalogue():
    products = Product.load_shops_products(request.args.get('shopId'))
    return make_response(jsonify(products))
