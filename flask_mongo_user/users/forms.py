from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, Regexp, EqualTo, ValidationError
from flask_mongo_user import db, um, bcrypt

def required(form, field):
    if len(field.data) == 0:
        raise ValidationError('')

def unique(form, field):
    if db.users.find_one({'email': field.data}):
        if um.status() and field.data == um.get_user('email'):
            pass
        else:
            raise ValidationError('Already exists in our database.')

def registered(form, field):
    if not db.users.find_one({'email': field.data}):
        raise ValidationError('Does not exist in our database.')

def check_password(form, field):
    user = db.users.find_one({'email': form.email.data})
    if user and not bcrypt.check_password_hash(user['password'], form.password.data):
        raise ValidationError('Incorrect password.')

class SignUpForm(Form):
    email = StringField(
        label='Email address',
        validators=[
            required,
            Length(min=4, max=254),
            Regexp(
                '^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$',
                message='Invalid email address.'
            ),
            unique
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            required,
            Length(min=8, max=20),
            Regexp(
                '^[a-zA-Z0-9_]+$',
                message='Invalid password.'
            )
        ]
    )
    confirm_password = PasswordField(
        label='Confirm password',
        validators=[
            EqualTo('password')
        ]
    )

class LoginForm(Form):
    email = StringField(
        label='Email address',
        validators=[
            required,
            Length(min=4, max=254),
            Regexp(
                '^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$',
                message='Invalid email address.'
            ),
            registered
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            required,
            Length(min=8, max=20),
            Regexp(
                '^[a-zA-Z0-9_]+$',
                message='Invalid password.'
            ),
            check_password
        ]
    )

class EditProfileForm(Form):
    email = StringField(
        label='Email address',
        validators=[
            required,
            Length(min=4, max=254),
            Regexp(
                '^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$',
                message='Invalid email address.'
            ),
            unique
        ]
    )

class EmailForm(Form):
    email = StringField(
        label='Email address',
        validators=[
            required,
            Length(min=4, max=254),
            Regexp(
                '^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$',
                message='Invalid email address.'
            ),
            registered
        ]
    )

class ResetPasswordForm(Form):
    password = PasswordField(
        label='Password',
        validators=[
            required,
            Length(min=8, max=20),
            Regexp(
                '^[a-zA-Z0-9_]+$',
                message='Invalid password.'
            )
        ]
    )
    confirm_password = PasswordField(
        label='Confirm password',
        validators=[
            EqualTo('password')
        ]
    )
