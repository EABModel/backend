from my_app import app, db, cache, bcrypt
from flask import jsonify, request, make_response, Response
from ..models.shop import Shop
from ..models.company import Company
from .user import build_user
from ..utils.errors import ClientError, error_handling
from ..utils.validation import validate_request
import uuid


create_company_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "name": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "name", "password"]
}


@app.route('/company/create', methods=['POST'])
@error_handling('create company')
def create_company():
    validate_request(request.json, create_company_schema)
    # Create Company
    company_id = uuid.uuid4()
    hashed_password = bcrypt.generate_password_hash(
        request.json['password']).decode('utf-8')
    company = Company(
        id=company_id,
        name=request.json['name'],
        email=request.json['email'],
        password=hashed_password,
    )
    # Create Company Admin
    user = build_user(
        username=f"Admin {request.json['name']}",
        email=request.json['email'],
        password=hashed_password,
        sessionType='ADMINISTRATOR',
        companyId=company_id,
    )
    db.session.add(company)
    db.session.commit()
    company = Company.load_company(company_id)
    return make_response(jsonify(company), 201)


company_login_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["name", "password"]
}


@app.route('/company/login', methods=['POST'])
@error_handling('login company')
def login_company():
    validate_request(request.json, company_login_schema)
    company = Company.load_company_by_name(request.json['name'])
    if not company:
        raise ClientError("Company does not exist", status_code=404)

    check_password = bcrypt.check_password_hash(
        company.password, request.json["password"])
    if not check_password:
        raise ClientError('Password is incorrect', status_code=403)

    data = {
        "id": company.id,
        "name": company.name,
        "email": company.email,
        "shops": Shop.load_shops(company.id)
    }
    return make_response(jsonify(data), 200)


@app.route('/company/<companyId>/shops', methods=['GET'])
@error_handling('get company shops')
def get_company(companyId):
    company = Company.query.filter_by(id=companyId).first()
    if not company:
        raise ClientError("Company does not exist", status_code=404)
    shops = company.shops
    return make_response(jsonify({'shops': [i.serialize() for i in shops]}))


@app.route('/company/<companyId>/users', methods=['GET'])
@error_handling('get company users')
def get_users(companyId):
    company = Company.query.filter_by(id=companyId).first()
    if not company:
        raise ClientError("Company does not exist", status_code=404)
    users = company.users
    return make_response(jsonify({'users': [i.serialize() for i in users]}))
