from my_app.models import shop
from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.product import Product
from ..utils.errors import ClientError
import uuid


@app.route('/catalogue/add-single-product', methods=['POST'])
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

@app.route('/catalogue/add-many-products', methods=['POST'])
def create_products():
    products = []
    for row in request.json:
        id = uuid.uuid4()
        product = Product(
            id=id,
            shopId=row['shopId'],
            name=row['name'],
            brand=row['brand'],
            os=row['os'],
            color=row['color'],
            inches=row['inches'],
            price=row['price']
        )
        products.append(product)
        db.session.add_all(products)
        db.session.commit()
    return make_response(jsonify({}), 201)

@app.route('/catalogue', methods=['GET'])
@cache.cached(timeout=50)
def get_catalogue():
    unserialized_products = Product.query.all()
    serialized_products = [product.serialize()
                           for product in unserialized_products]
    return make_response(jsonify(serialized_products))


@app.route('/catalogue/<productId>', methods=['GET', 'PUT'])
@cache.cached(timeout=50)
def get_product(productId):
    if request.method == 'GET':
        product = Product.load_product(productId)
        return make_response(jsonify(product), 200)

    if request.method == 'PUT':
        product = Product.query.get(productId)

        if request.json['name']:   product.name =  request.json['name']
        if request.json['brand']:  product.brand = request.json['brand']
        if request.json['os']:     product.os = request.json['os']
        if request.json['color']:  product.color = request.json['color']
        if request.json['inches']: product.inches = request.json['inches']
        if request.json['price']:  product.price = request.json['price']
        
        db.session.commit()
    
        return make_response(jsonify(product.serialize()), 200)


@app.route('/catalogue/shop/<shopId>', methods=['GET'])
def get_catalog(shopId):
    products = Product.load_shops_products(shopId)
    return make_response(jsonify(products), 200)
