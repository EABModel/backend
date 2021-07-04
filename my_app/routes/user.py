from my_app import app, bcrypt, db, cache
from flask import jsonify, request, make_response, render_template
from ..models.user import User
from ..utils.auth import generate_tokens
import uuid


@app.route('/user', methods=['GET'])
def get_user():
    return make_response(jsonify('Hola'), 200)


@app.route('/user/create', methods=['POST'])
def create_user():
    try:
        id = uuid.uuid4()
        hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        user = User(
            id=id,
            username=request.json['username'],
            email=request.json['email'],
            companyId=request.json['companyId'],
            shopId=request.json['shopId'],
            password=hashed_password,
            sessionType='EMPLOYEE'
        )
        db.session.add(user)
        db.session.commit()
        user = User.load_user(str(id))
        return make_response(jsonify({}), 201)
        # return make_response(jsonify(user), 201)
    except Exception as err:
        app.logger.info('Err', err)
        raise err

@app.route('/user/set_shop', methods=['PATCH'])
def set_shop_id():
    try:
        user = User.query.filter_by(id=request.json['userId']).first()
        user.shopId = request.json['shopId']
        db.session.commit()
        return make_response(jsonify(user.serialize()), 202)
    except Exception as err:
        app.logger.info('Err', err)
        raise err

@app.route('/user/<userId>', methods=['DELETE'])
def delete_user(userId):
    user = User.query.filter_by(id=userId).first()
    db.session.delete(user)
    db.session.commit()
    return make_response('User has been deleted', 202)
