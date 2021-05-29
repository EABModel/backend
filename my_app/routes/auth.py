from my_app import app, bcrypt, db, cache
from flask import jsonify, request, make_response, render_template
from ..models.user import User
from ..utils.auth import generate_tokens, refresh_new_token


@app.route('/user/auth', methods=['POST'])
def submit_auth():
    status = 200
    try:
        user = User.load_user_by_email(request.json['email'])
        """
        TODO: Tira invalid salt todo el rato
        """
        # check_password = bcrypt.check_password_hash(data["password"], request.json["password"].encode('utf-8'))
        # if not check_password:
        #     raise Exception("Password is incorrect")
        refresh_token, token = generate_tokens(user["id"])
        return make_response(jsonify({'user': user, 'refresh_token': refresh_token, 'token': token}), 201)
    except Exception as error:
        data = error.__repr__()
        return make_response(jsonify(data), 400)


@app.route('/user/auth', methods=['get'])
def get_new_token():
    refresh_token = request.headers.get('Refresh-Token')
    new_token = refresh_new_token(refresh_token)
    return make_response(jsonify({'token': new_token}), 201)
