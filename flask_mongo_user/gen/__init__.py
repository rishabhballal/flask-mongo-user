from flask import Blueprint

gen = Blueprint(
    'gen',
    __name__,
    static_folder='static',
    static_url_path='/gen/static'
)

from flask_mongo_user.gen import views
