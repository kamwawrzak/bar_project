from app.db_interactors.user_db_inter import UserDbInter

from werkzeug.security import check_password_hash


class Validators:

    def validate_register_data(self, email, nick, password, confirm_pass):
        error = None
        check_email = Validators().validate_email(email)
        check_nick = Validators().validate_nick(nick)
        check_pass = Validators().validate_pass(password, confirm_pass)
        if check_email is not None:
            error = check_email
        elif check_nick:
            error = check_nick
        elif check_pass:
            error = check_pass
        return error

    def validate_email(self, email):
        if not email:
            error = 'Email is required.'
        elif UserDbInter().user_by_email(email):
            if UserDbInter().user_by_email(email) is False:
                error = 'This email address is already registered.'
            else:
                e1 = 'This email address is taken. '
                e2 = 'Please try to login via Facebook.'
                error = e1 + e2
        else:
            error = None
        return error

    def validate_nick(self, nick):
        if not nick:
            error = 'Nickname is required.'
        elif len(nick) < 5:
            error = 'Nickname must me longer then 5 characters'
        elif len(nick) > 12:
            error = "Nickname must be shorter then 10 characters"
        elif UserDbInter().user_by_nick(nick):
            error = 'This nickname already exists'
        else:
            error = None
        return error

    def validate_pass(self, password, confirm_pass):
        specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        if not password:
            error = 'Password is required.'
        elif password != confirm_pass:
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
        user = UserDbInter().user_by_email(email)
        if not user:
            return 'This email is not registered'
        elif not check_password_hash(user.password_hash, password):
            return 'Incorrect password'
        else:
            return user
