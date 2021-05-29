from my_app import app, bcrypt, db, cache
from flask import jsonify, request, make_response, render_template
from ..models.user import User
from ..utils.auth import generate_tokens
import uuid


@app.route('/user', methods=['GET'])
@cache.cached(timeout=50)
def get_user():
    return make_response(jsonify('Hola'), 200)


@app.route('/user/create', methods=['POST'])
@cache.cached(timeout=50)
def create_user():
    try:
        id = uuid.uuid4()
        hashed_password = bcrypt.generate_password_hash(
            request.json['password'].encode('utf-8'))
        user = User(
            id=id,
            username=request.json['username'],
            email=request.json['email'],
            password=hashed_password,
            sessionType='EMPLOYEE'
        )
        db.session.add(user)
        db.session.commit()
        user = User.load_user(str(id))
        refresh_token, token = generate_tokens(user["id"])
        return make_response(jsonify({'user': user, 'refresh_token': refresh_token, 'token': token}), 201)
        # return make_response(jsonify(user), 201)
    except Exception as err:
        app.logger.info('Err', err)
        raise err
