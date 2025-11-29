from flask import render_template, redirect, request, url_for, flash, abort
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired
from flask_mongo_user import app, db, mail, bcrypt, um
from flask_mongo_user.users import users
from flask_mongo_user.users.forms import SignUpForm, LoginForm, EditProfileForm, EmailForm, ResetPasswordForm
from datetime import datetime
from random import randint

code = randint(1000, 9999)

def get_token(email, expires=300):
    s = Serializer(app.config['SECRET_KEY'], expires)
    global code
    return s.dumps({'email': email, 'code': code}).decode('utf-8')

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        global code
        if s.loads(token)['code'] == code:
            return s.loads(token)['email']
        else:
            raise SignatureExpired('Signature has expired.')
    except SignatureExpired:
        abort(404)

@users.route('/')
@um.access_required
def account():
    return render_template(
        'account.html',
        title='Account',
        um=um
    )

@users.route('/sign_up', methods=['GET', 'POST'])
@um.access_restricted
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.users.insert_one({
            'email': form.email.data,
            'password': hashed,
            'datetime': datetime.utcnow(),
            'verified': False
        })
        verify(form.email.data)
        return redirect(url_for('users.login'))
    return render_template(
        'sign_up.html',
        title='Sign Up',
        um=um,
        form=form
    )

@users.route('/login', methods=['GET', 'POST'])
@um.access_restricted
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        um.set_user(db.users.find_one({'email': form.email.data}))
        return redirect(url_for('users.account'))
    return render_template(
        'login.html',
        title='Login',
        um=um,
        form=form
    )

def verify(email):
    token = get_token(email)
    msg = Message(
        'Verify your account',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f'''
To verify your account, click on the following link:

{url_for('users.verify2', token=token, _external=True)}'''
    mail.send(msg)
    flash('An email has been sent with a link to verify your account.')

@users.route('/verify')
@um.access_required
def verify1():
    verify(um.get_user('email'))
    return redirect(url_for('users.account'))

@users.route('/verify/<token>')
def verify2(token):
    email = verify_token(token)
    if not db.users.find_one({'email': email}):
        abort(404)
    db.users.update_one({'email': email}, {
        '$set': {'verified': True}
    })
    global code
    code = randint(1000, 9999)
    if um.status():
        um.reset_user()
        um.set_user(db.users.find_one({'email': email}))
    flash('Your account has been verified.')
    return redirect(url_for('gen.home'))

@users.route('/edit', methods=['GET', 'POST'])
@um.access_required
def edit_account():
    form = EditProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.email.data != um.get_user('email'):
            db.users.update_one({'email': um.get_user('email')}, {
                '$set': {
                    'email': form.email.data,
                    'verified': False
                }
            })
            verify(form.email.data)
            um.reset_user()
            um.set_user(db.users.find_one({'email': form.email.data}))
        return redirect(url_for('users.account'))
    return render_template(
        'edit_account.html',
        title='Edit Account',
        um=um,
        form=form
    )

def reset_password(email):
    token = get_token(email)
    msg = Message(
        'Reset your password',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f'''
To reset your password, click on the following link:

{url_for('users.reset_password2', token=token, _external=True)}'''
    mail.send(msg)
    flash('An email has been sent with a link to reset your password.')

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password1():
    if um.status():
        reset_password(um.get_user('email'))
        return redirect(url_for('users.logout'))
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        reset_password(form.email.data)
        return redirect(url_for('users.login'))
    return render_template(
        'email.html',
        title='Reset password',
        um=um,
        form=form
    )

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
@um.access_restricted
def reset_password2(token):
    email = verify_token(token)
    if not db.users.find_one({'email': email}):
        abort(404)
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.users.update_one({'email': email}, {
            '$set': {'password': hashed}
        })
        global code
        code = randint(1000, 9999)
        flash('Password has been reset.')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_password.html',
        title='Reset password',
        um=um,
        form=form,
        token=token
    )

@users.route('/logout')
@um.access_required
def logout():
    um.reset_user()
    return redirect(url_for('users.login'))

@users.route('/delete')
@um.access_required
def delete1():
    token = get_token(um.get_user('email'))
    msg = Message(
        'Delete your account',
        sender=app.config['MAIL_USERNAME'],
        recipients=[um.get_user('email')]
    )
    msg.body = f'''
To delete your account, click on the following link:

{url_for('users.delete2', token=token, _external=True)}'''
    mail.send(msg)
    flash('An email has been sent with a link to delete your account.')
    return redirect(url_for('users.logout'))

@users.route('/delete/<token>')
def delete2(token):
    email = verify_token(token)
    db.users.delete_one({'email': email})
    global code
    code = randint(1000, 9999)
    flash('Your account has been deleted.')
    return redirect(url_for('gen.home'))
