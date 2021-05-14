from my_app import app, bcrypt, db, mail, cache
from flask import render_template, jsonify, redirect, url_for, request, make_response
from my_app.models import User, load_user, load_user_by_email, Product, Shop
from my_app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user
from flask_mail import Message
import uuid

@app.route('/', methods=['GET'])
@cache.cached(timeout=50)
def index():
    return render_template('home.html')

@app.route('/user', methods=['GET'])
@cache.cached(timeout=50)
def get_user():
    return 'Hola'

@app.route('/user/create', methods=['POST'])
@cache.cached(timeout=50)
def create_user():
    # form = RegistrationForm() access -> form.password.data
    id = uuid.uuid4()
    hashed_password = bcrypt.generate_password_hash(request.json['password'].encode('utf-8'))
    user = User(
        id=id,
        username=request.json['username'],
        email=request.json['email'],
        password=hashed_password,
        sessionType='EMPLOYEE',
        authToken='',
        refreshToken=''
    )
    db.session.add(user)
    db.session.commit()
    createdUser = load_user(str(id))
    return make_response(jsonify(createdUser), 201)

@app.route('/shop/create', methods=['POST'])
@cache.cached(timeout=50)
def create_shop():
    shop = Shop(
        id=uuid.uuid4(),
        name=request.json['name'],
        location=request.json['location'],
    )
    db.session.add(shop)
    db.session.commit()
    return make_response(jsonify(shop), 201)

@app.route('/user/auth', methods=['POST'])
def submit_auth():
    response = None
    status = 200
    try:
        data = load_user_by_email(request.json['email'])
        """
        To Fix:
        Tira invalid salt todo el rato
        """
        # check_password = bcrypt.check_password_hash(data["password"], request.json["password"].encode('utf-8'))
        # if not check_password:
        #     raise Exception("Password is incorrect")
    except Exception as error:
        status = 400
        data = error.__repr__()
    return make_response(jsonify(data), status)

@app.route('/catalogue/add-single-product', methods=['POST'])
@cache.cached(timeout=50)
def create_product():
    id = uuid.uuid4()
    product = Product(
        id=id,
        shopId=request.json['shopId'],
        name=request.json['name'],
        brand=request.json['brand'],
        os=request.json['os'],
        color=request.json['color'],
        inches=request.json['inches'],
        price=request.json['price']
    )
    db.session.add(product)
    db.session.commit()
    return make_response(jsonify(product), 201)
