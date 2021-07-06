from my_app.models import shop
from my_app import app, db, cache
from flask import jsonify, request, make_response, session, g
from ..models.product import Product
from ..utils.auth import login_required
from ..utils.errors import ClientError, error_handling
from ..utils.validation import validate_request
import uuid


create_product_schema = {
    "type": "object",
    "properties": {
        "brand": {"type": "string"},
        "color": {"type": "string"},
        "image": {"type": "string"},
        "inches": {"type": "integer"},
        "name": {"type": "string"},
        "os": {"type": "string"},
        "price": {"type": "integer"},
        "shopId": {"type": "string"},
    },
    "required": ["brand", "color", "image", "inches", "name", "os", "price", "shopId"]
}


@app.route('/catalogue/add-single-product', methods=['POST'])
@login_required
@error_handling('create product')
def create_product():
    validate_request(request.json, create_product_schema)
    id = uuid.uuid4()
    product = Product(
        id=id,
        shopId=request.json['shopId'],
        name=request.json['name'],
        brand=request.json['brand'],
        os=request.json['os'],
        color=request.json['color'],
        inches=request.json['inches'],
        price=request.json['price'],
        image=request.json['image']
    )
    db.session.add(product)
    db.session.commit()
    product = Product.load_product(str(id))
    return make_response(jsonify(product), 201)


create_products_schema = {
    "type": "array",
    "items": create_product_schema
}


@app.route('/catalogue/add-many-products', methods=['POST'])
@login_required
@error_handling('create products')
def create_products():
    validate_request(request.json, create_products_schema)
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
            price=row['price'],
            image=row['image']
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


@app.route('/catalogue/<productId>', methods=['GET'])
@error_handling('get product')
def get_product(productId):
    product = Product.load_product(productId)
    if not product:
        raise ClientError("Product does not exist", status_code=404)
    return make_response(jsonify(product), 200)


@app.route('/catalogue/shop/', methods=['GET'])
@error_handling('get empty catalogue')
def get_empty_catalog():
    raise ClientError("You are not in a shop", status_code=404)


@app.route('/catalogue/shop/<shopId>', methods=['GET'])
@error_handling('get catalogue')
def get_catalog(shopId):
    products = Product.load_shops_products(shopId)
    if products:
        return make_response(jsonify(products), 200)
    raise ClientError("You haven't created products", status_code=404)


@app.route('/catalogue/delete-product/<productId>', methods=['DELETE'])
@error_handling('delete product')
def delete_product(productId):
    product = Product.query.get(productId)
    if not product:
        raise ClientError("Product does not exist", status_code=404)
    db.session.delete(product)
    db.session.commit()
    return make_response(jsonify(product.serialize()), 200)


edit_product_schema = {
    "type": "object",
    "properties": {
        "brand": {"type": "string"},
        "color": {"type": "string"},
        "image": {"type": "string"},
        "inches": {"type": "integer"},
        "name": {"type": "string"},
        "os": {"type": "string"},
        "price": {"type": "integer"},
    },
}


@app.route('/catalogue/edit-product/<productId>', methods=['PUT'])
@error_handling('edit product')
def edit_product(productId):
    validate_request(request.json, edit_product_schema)
    product = Product.query.get(productId)

    if request.json['brand']:  product.brand = request.json['brand']
    if request.json['color']:  product.color = request.json['color']
    if request.json['image']:  product.image = request.json['image']
    if request.json['inches']: product.inches = request.json['inches']
    if request.json['name']:   product.name =  request.json['name']
    if request.json['os']:     product.os = request.json['os']
    if request.json['price']:  product.price = request.json['price']
    
    db.session.commit()

    return make_response(jsonify(product.serialize()), 200)
