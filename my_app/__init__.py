from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_caching import Cache
from flask_cors import CORS
from flask_uuid import FlaskUUID
import os

# Load environmet variables
load_dotenv('./env')

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
FlaskUUID(app)


# _______________________________________________________________________________
# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

# _______________________________________________________________________________
# Cache config
cache = Cache(app, config={'CACHE_TYPE': 'redis',
                           'CACHE_REDIS_URL': 'redis://redis:6379/0'})
if db and cache:
    print('Conection to database and cache established successfully...')

# _______________________________________________________________________________
# Mail config

# app.config['MAIL_SERVER']= os.getenv("MAIL_SERVER")
# app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
# app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
# app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
# app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
# app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL")
mail = Mail(app)

# _______________________________________________________________________________
# Others
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}},)

from .routes import *  # nopep8
