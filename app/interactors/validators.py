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
                e1 = 'This account has been created via Facebook.'
                e2 = 'Please try to login via Facebook.'
                error = e1 + e2
        else:
            error = None
        return error

    def validate_nick(self, nick):
        if not nick:
            error = 'Nickname is required.'
        elif 12 > len(nick) < 3:
            error = 'Nickname must contain between 4 and 12 characters.'
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
        elif 7 < len(password) > 16:
            error = 'Password must contain between 8 and 15 characters.'
        elif not any(char.isdigit() for char in password):
            error = 'Password must contain at least one digit.'
        elif not any(char.isupper() for char in password):
            error = 'Password must contain at least one capital letter.'
        elif not any(char.islower() for char in password):
            error = 'Password must contain at least one lower letter.'
        elif not any(char in specials for char in password):
            s1 = 'Password must contain at least one special sign:'
            s2 = ' !@#$%^&*()'
            error = s1 + s2
        elif any(char == ' ' for char in password):
            error = 'Password cannot contain spaces.'
        else:
            error = None
        return error

    def validate_login_data(self, email, password):
        user = UserDbInter().user_by_email(email)
        if not user:
            return "This account doesn't exist"
        elif user.oauth_user is True:
            return 'This account requires login via Facebook.'
        elif not check_password_hash(user.password_hash, password):
            return 'Incorrect password.'
        else:
            return user
