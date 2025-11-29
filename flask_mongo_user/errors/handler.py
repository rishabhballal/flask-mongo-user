from flask import render_template
from werkzeug.exceptions import HTTPException
from flask_mongo_user import um
from flask_mongo_user.errors import errors

@errors.app_errorhandler(HTTPException)
def error_handler(error):
    return render_template(
        'error.html',
        title=error.name,
        error=error,
        um=um
    ), error.code
