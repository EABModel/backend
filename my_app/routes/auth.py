from my_app import app, bcrypt, db, cache
from flask import jsonify, request, make_response, render_template
from ..models.user import User
from ..utils.auth import generate_tokens, refresh_new_token
from ..utils.errors import ClientError, error_handling
from ..utils.validation import validate_request


user_auth_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"]
}


@app.route('/user/auth', methods=['POST'])
@error_handling('user auth')
def submit_auth():
    validate_request(request.json, user_auth_schema)
    user = User.load_user_by_email(request.json['email'])
    if not user:
        raise ClientError("Email does not exist")
    check_password = bcrypt.check_password_hash(
        user.password, request.json["password"])
    if not check_password:
        raise ClientError("Password is incorrect")

    user = user.serialize()
    refresh_token, token = generate_tokens(user["id"])
    return make_response(jsonify({'user': user, 'refresh_token': refresh_token, 'token': token}), 201)


@app.route('/user/auth', methods=['get'])
def get_new_token():
    refresh_token = request.headers.get('Refresh-Token')
    new_token = refresh_new_token(refresh_token)
    return make_response(jsonify({'token': new_token}), 201)
