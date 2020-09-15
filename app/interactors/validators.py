from app.models import RegularUser

from werkzeug.security import check_password_hash


class Validators:

    def validate_register_data(self, email, nick, password, confirm_pass):
        if not email:
            error = 'Email is required.'
        elif not nick:
            error = 'Nickname is required.'
        elif len(nick) < 5:
            error = 'Nickname must me longer then 5 characters'
        elif len(nick) > 10:
            error = "Nickname must be shorter then 10 characters"
        elif not password:
            error = 'Password is required.'
        elif RegularUser.query.filter_by(email=email).first():
            error = 'This email address is already registered.'
        elif RegularUser.query.filter_by(nick=nick).first():
            error = 'This nickname already exists'
        elif Validators().validate_pass(password, confirm_pass) is not None:
            error = Validators().validate_pass(password, confirm_pass)
        else:
            error = None
        return error

    def validate_pass(self, password, confirm_pass):
        specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        if password != confirm_pass:
            error = "Password and Confirm Password don't match."
        elif len(password) > 15:
            error = 'Password must be shorter then 15 characters'
        elif len(password) < 8:
            error = 'Password must be longer then 8 characters'
        elif not any(char.isdigit() for char in password):
            error = 'Password must contain at least one digit'
        elif not any(char.isupper() for char in password):
            error = 'Password must contain at least one capital letter'
        elif not any(char.islower() for char in password):
            error = 'Password must contain at least one lower letter'
        elif not any(char in specials for char in password):
            error = 'Password must contain at least of symbols: !@#$%^&*()'
        elif any(char == ' ' for char in password):
            error = 'Password cannot include spaces'
        else:
            error = None
        return error

    def validate_login_data(self, email, password):
        user = RegularUser.query.filter_by(email=email).first()
        if not user:
            return 'This email is not registered'
        elif not check_password_hash(user.password_hash, password):
            return 'Incorrect password'
        else:
            return user
