from my_app import app, db, cache
from flask import jsonify, request, make_response, Response
from ..models.shop import Shop
from ..models.company import Company
import uuid


@app.route('/company/create', methods=['POST'])
@cache.cached(timeout=50)
def create_company():
    id = uuid.uuid4()
    company = Company(
        id=id,
        name=request.json['name'],
        password=request.json['password'],
    )
    db.session.add(company)
    db.session.commit()
    company = Company.load_company(id)
    return make_response(jsonify(company), 201)

@app.route('/company/login', methods=['POST'])
@cache.cached(timeout=50)
def login_company():
    status = 200
    data = []
    try:
        company = Company.load_company_by_name(request.json['name'])
        """TODO: Tira invalid salt todo el rato"""
        check_password = True
        # check_password = bcrypt.check_password_hash(data["password"], request.json["password"].encode('utf-8'))
        if not check_password:
            return Response('Password is incorrect', status=403)
        if not company:
            return Response('Company not found', status=404)
        if check_password:
            data = {
                "id": company.id,
                "name": company.name,
                "shops": Shop.load_shops(company.id)
            }
            return make_response(jsonify(data), status)
    except Exception as error:
        status = 400
        return Response(error.__repr__(), status=status)
