# flask + mongo db user portal

initialise config.py within the flask_mongo_user subdirectory:
```
# /flask_mongo_user/config.py
class Config:
  SECRET_KEY = <secret_key>
  FLASK_APP = 'wsgi.py'
  STATIC_FOLDER = 'static'
  TEMPLATES_FOLDER = 'templates'
  MONGODB_SETTINGS = {
    'db': <db_name>,
    'host': <mongo_uri>,
  }
```
