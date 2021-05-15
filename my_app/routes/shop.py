from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.shop import Shop
import uuid


@app.route('/shop/create', methods=['POST'])
@cache.cached(timeout=50)
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
    # Returns an empty object to avoid changing shop state in frontend state
    return make_response(jsonify({}), 201)
