from flask import Blueprint

users = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/users/static',
    url_prefix='/account'
)

from flask_mongo_user.users import views
