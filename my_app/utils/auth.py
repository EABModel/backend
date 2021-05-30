import jwt
import datetime
from .errors import ClientError
from flask import jsonify, make_response, request, session, g
from functools import wraps
from my_app import app, fernet
from ..models.user import User
import uuid


def generate_jwt(user_id):
    return jwt.encode({
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, app.config['SECRET_KEY'], algorithm="HS256")


def generate_refresh_jwt(user_id):
    return jwt.encode({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=11)
    }, app.config['SECRET_KEY'], algorithm="HS256")


def generate_tokens(user_id):
    return [
        generate_refresh_jwt(user_id),
        generate_jwt(user_id)
    ]


def refresh_new_token(encoded_refresh_token):
    try:
        refresh_token = jwt.decode(
            encoded_refresh_token,
            app.config['SECRET_KEY'],
            algorithms="HS256"
        )
        """
        TODO: revisar que el refresh token no este en una base de datos con tokens invalidados (log out)
        """
        return generate_jwt(refresh_token["user_id"])
    except:
        return make_response(jsonify({'message': 'Refresh-Token is invalid'}), 401)


def current_user(user):
    if 'current_user' not in g:
        g.user = {}
    g.user['user'] = user


def login_required(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        token = request.headers.get('Token')
        if not token:
            return make_response(jsonify({'message': 'Token is missing'}), 401)
        try:
            decoded_token = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms="HS256")
            user = User.load_user(decoded_token["user_id"])
            if user:
                app.logger.info("if user")
                current_user(user)
                return func(*args, **kwargs)
            raise ClientError("Problems in authentication")
        except ClientError as error:
            return make_response(jsonify({'message': error.message}), 401)
        except Exception as error:
            app.logger.info('login_required error', error)
            return make_response(jsonify({'message': 'Token is invalid'}), 401)
    return check_token


def admin_required(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        token = request.headers.get('Token')
        if not token:
            return make_response(jsonify({'message': 'Token is missing'}), 401)
        try:
            decoded_token = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms="HS256")
            user = User.load_user(decoded_token["user_id"])
            if user and user.sessionType == 'ADMINISTRATOR':
                app.logger.info("if user")
                current_user(user)
                return func(*args, **kwargs)
            raise ClientError("Problems in authentication")
        except ClientError as error:
            return make_response(jsonify({'message': error.message}), 401)
        except Exception as error:
            app.logger.info('login_required error', error)
            return make_response(jsonify({'message': 'Token is invalid'}), 401)
    return check_token
