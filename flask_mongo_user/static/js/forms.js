class Form {
  constructor(form_id) {
    this.form = document.getElementById(form_id);
    this.green = '#00ab66';
    this.red = '#d11a2a';
  }

  _length(field, min, max) {
    if (field.value.trim().length < min || field.value.length > max) {
      return false;
    } else {
      return true;
    }
  }

  _pass(field) {
    field.style.padding = '9px 19px';
    field.style.border = `${this.green} solid 2px`;
    document.getElementById(`${field.name}-error`).innerText = '';
    return true;
  }

  _fail(field) {
    field.style.padding = '9px 19px';
    field.style.border = `${this.red} solid 2px`;
    return false;
  }

  required(fields) {
    this.form.addEventListener('submit', () => {
      fields.forEach(field => {
        if (!this.form.elements[field].value.length) {
          var u = this._fail(this.form.elements[field]);
          event.preventDefault();
        }
      });
    });
  }

  validate(validators) {
    var flags = [];
    for (var i=0; i < validators.length; i++) {
      flags[i] = !validators[i]['required'];
    }

    validators.forEach((val, i) => {
      var field = this.form.elements[val['name']];
      if (val['default']) {
        field.value = val['default'];
        flags[i] = this._pass(field);
      }
      field.addEventListener('change', () => {
        var subflag1 = this._length(field, val['length'][0], val['length'][1]);
        var subflag2 = val['regex'].test(field.value);
        if (subflag1 && subflag2) {
          flags[i] = this._pass(field);
        } else if (field.value.trim().length) {
          flags[i] = this._fail(field);
          switch (field.name) {
            case 'email':
              document.getElementById('email-error').innerText = 'Invalid email address.';
              break;
            case 'password':
              document.getElementById('password-error').innerText = 'Allowed characters: a-z, A-Z, 0-9, and _.';
              break;
            default:
              document.getElementById(`${field.name}-error`).innerText = `Invalid characters in ${field.name}.`;
          }
          if (!subflag1) {
            document.getElementById(`${field.name}-error`).innerText = `Has to be between ${val['length'][0]} and ${val['length'][1]} characters.`;
          }
        } else {
          if (val['required']) {
            flags[i] = this._fail(field);
          } else {
            flags[i] = this._pass(field);
          }
        }
        var confirm = field.name.split('_');
        if (confirm[0] == 'confirm') {
          if (field.value == this.form.elements[confirm[1]].value) {
            flags[i] = this._pass(field);
          } else {
            flags[i] = this._fail(field);
            document.getElementById(`${field.name}-error`).innerText = `Does not match ${confirm[1]}.`;
          }
        }
        confirm = this.form.elements[`confirm_${field.name}`];
        if (confirm && confirm.value) {
          if (field.value == confirm.value) {
            flags[i+1] = this._pass(confirm);
          } else {
            flags[i+1] = this._fail(confirm);
            document.getElementById(`confirm_${field.name}-error`).innerText = `Does not match ${field.name}.`;
          }
        }
      });
    });

    this.form.addEventListener('submit', event => {
      validators.forEach((val, i) => {
        var field = this.form.elements[val['name']];
        if (flags[i]) {
          flags[i] = this._pass(field);
        } else {
          flags[i] = this._fail(field);
        }
      });
      if (flags.includes(false)) {
        event.preventDefault();
      }
    });
  }
}
