from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.shop import Shop
from ..models.company import Company
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
    shop = Shop.load_shop(id)
    return make_response(jsonify(shop), 201)

@app.route('/shop/login', methods=['POST'])
@cache.cached(timeout=50)
def login_shop():
    status = 200
    data = []
    try:
        company = Company.load_company_by_name(request.json['name'])
        """
        TODO: Tira invalid salt todo el rato
        """
        check_password = True
        # check_password = bcrypt.check_password_hash(data["password"], request.json["password"].encode('utf-8'))
        # if not check_password:
        #     status = 403
        #     raise Exception("Password is incorrect")
        if check_password:
            data = Shop.load_shops(company.id)
    except Exception as error:
        status = 403 if status == 403 else 400
        data = error.__repr__()
    return make_response(jsonify(data), status)