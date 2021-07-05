from my_app import app, bcrypt, db, cache
from flask import jsonify, request, make_response, render_template
from ..models.user import User
from ..utils.auth import generate_tokens
from ..utils.errors import ClientError, error_handling
from ..utils.validation import validate_request
import uuid


def build_user(email='', username='', password='', companyId='', shopId=None, sessionType='EMPLOYEE'):
    id = uuid.uuid4()
    user = User(
        id=id,
        username=username,
        email=email,
        companyId=companyId,
        shopId=shopId,
        password=password,
        sessionType=sessionType
    )
    db.session.add(user)
    return user


@app.route('/user', methods=['GET'])
def get_user():
    return make_response(jsonify('Hola'), 200)


create_user_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"},
        "companyId": {"type": "string"},
        "shopId": {"type": "string"},
    },
    "required": ["email", "username", "password", "companyId", "shopId"]
}


@app.route('/user/create', methods=['POST'])
@error_handling('create user')
def create_user():
    validate_request(request.json, create_user_schema)
    hashed_password = bcrypt.generate_password_hash(
        request.json['password']).decode('utf-8')
    user = build_user(
        username=request.json['username'],
        email=request.json['email'],
        companyId=request.json['companyId'],
        shopId=request.json['shopId'],
        password=hashed_password,
        sessionType='EMPLOYEE'
    )
    db.session.commit()

    return make_response(jsonify({}), 201)


set_shop_id_schema = {
    "type": "object",
    "properties": {
        "userId": {"type": "string"},
        "shopId": {"type": "string"},
    },
    "required": ["userId", "shopId"]
}


@app.route('/user/set_shop', methods=['PATCH'])
@error_handling('set shop id to user')
def set_shop_id():
    validate_request(request.json, set_shop_id_schema)
    user = User.query.filter_by(id=request.json['userId']).first()
    if not user:
        raise ClientError(f"user does not exist", status_code=404)
    user.shopId = request.json['shopId']
    db.session.commit()
    return make_response(jsonify(user.serialize()), 202)


@app.route('/user/<userId>', methods=['DELETE'])
@error_handling('delete user')
def delete_user(userId):
    user = User.query.filter_by(id=userId).first()
    if not user:
        raise ClientError(f"user does not exist", status_code=404)
    db.session.delete(user)
    db.session.commit()
    return make_response('User has been deleted', 202)
