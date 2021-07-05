from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.shop import Shop
from ..utils.errors import error_handling
from ..utils.validation import validate_request
import uuid


create_shop_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "name": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["location", "name", "password"]
}


@app.route('/shop/create', methods=['POST'])
@error_handling('create shop')
def create_shop():
    validate_request(request.json, create_shop_schema)
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
