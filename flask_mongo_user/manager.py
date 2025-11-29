from flask import redirect, url_for
import json

class UserManager:
    def __init__(self, app):
        self._path = app.root_path + app.config['PATH_TO_USER_JSON']
        self.reset_user()

    def reset_user(self):
        self._user = {}
        with open(self._path, 'w') as file:
            file.write('{}')

    def set_user(self, user):
        if not self.status():
            user.pop('_id', None)
            user.pop('password', None)
            self._user = user
            with open(self._path, 'w') as file:
                file.write(json.dumps(user, indent=4, default=str))

    def get_user(self, attr=None):
        if attr:
            return self._user[attr]
        return self._user

    def status(self):
        return bool(self._user)

    def access_required(self, func):
        def wrapper(*args, **kwargs):
            if not self.status():
                return redirect(url_for('users.login'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def access_restricted(self, func):
        def wrapper(*args, **kwargs):
            if self.status():
                return redirect(url_for('gen.home'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
