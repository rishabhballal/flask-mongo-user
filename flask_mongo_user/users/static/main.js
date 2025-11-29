const getUser = () =>
  fetch('/account/users/static/user.json', {cache: 'no-cache'})
    .then(response => response.json());

var email = {
  'name': 'email',
  'length': [4, 254],
  'regex': /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$/,
  'required': true,
  'default': null
}

var password = {
  'name': 'password',
  'length': [8, 20],
  'regex': /^[a-zA-Z0-9_]+$/,
  'required': true,
  'default': null
}

var confirm_password = {
  'name': 'confirm_password',
  'length': [8, 20],
  'regex': /^[a-zA-Z0-9_]+$/,
  'required': true,
  'default': null
};

const route = window.location.pathname.split('/');
switch (route[2]) {
  case 'sign_up':
    new Form('sign-up-form').validate([email, password, confirm_password]);
    break;

  case 'login':
    new Form('login-form').required(['email', 'password']);
    break;

  case 'edit':
    getUser().then(user => {
      email.default = user.email;
      new Form('edit-account-form').validate([email]);
    });
    break;

  case 'reset_password':
    if (route[3]) {
      new Form('reset-password-form').validate([password, confirm_password]);
      break;
    } else {
      new Form('email-form').required(['email']);
      break;
    }
}
