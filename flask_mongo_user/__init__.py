from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_mongo_user.config import Config
from flask_mongo_user.manager import UserManager

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGODB_URI'])
db = client.flask_mongo_user
bcrypt = Bcrypt(app)
mail = Mail(app)
um = UserManager(app)

from flask_mongo_user.gen import gen
from flask_mongo_user.users import users
from flask_mongo_user.errors import errors
app.register_blueprint(gen)
app.register_blueprint(users)
app.register_blueprint(errors)
