from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.shop import Shop
import uuid


@app.route('/shop/create', methods=['POST'])
def create_shop():
    id = uuid.uuid4()
    shop = Shop(
        id=id,
        companyId=request.json['companyId'],
        name=request.json['name'],
        location=request.json['location'],
    )
    db.session.add(shop)
    db.session.commit()
    shop = Shop.load_shop(id)
    return make_response(jsonify(shop), 201)
