from my_app import app, bcrypt, db, cache
from flask import jsonify, request, make_response, render_template
from ..models.user import User
import uuid


@app.route('/user', methods=['GET'])
def get_user():
    return make_response(jsonify('Hola'), 200)

@app.route('/user/create', methods=['POST'])
def create_user():
    id = uuid.uuid4()
    hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
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
    return make_response(jsonify(user), 201)

@app.route('/user/auth', methods=['POST'])
def submit_auth():
    status = 200
    try:
        data = User.load_user_by_email(request.json['email'])
        """
        TODO: Tira invalid salt todo el rato
        """
        check_password = bcrypt.check_password_hash(data.password, request.json["password"])
        data = data.serialize()
        if not check_password:
            raise Exception("Password is incorrect")
    except Exception as error:
        status = 400
        data = error.__repr__()
    return make_response(jsonify(data), status)
