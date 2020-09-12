from app import db
from app.models import RegularUser
from app.web_interactors import WebInteractors

from flask import Blueprint, flash, redirect, url_for

from werkzeug.security import generate_password_hash


register_bp = Blueprint('register_bp', __name__)


@register_bp.route('/v1/register', methods=['GET', 'POST'])
def register_post():
    d = WebInteractors().get_form_data('email', 'nick',
                                       'password', 'confirm_pass')
    error = check_data(d['email'], d['nick'], d['password'], d['confirm_pass'])
    if error is None:
        pass_hash = generate_password_hash(d['password'], method='SHA256')
        new_user = RegularUser(email=d['email'], nick=d['nick'],
                               password_hash=pass_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('You have been registered successfully')
        return redirect(url_for('index'))
    else:
        flash(error)
        return redirect(url_for('registration'))


def check_data(email, nick, password, confirm_pass):
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
    elif password != confirm_pass:
        error = "Password and Confirm Password don't match."
    elif validate_password(password) is not None:
        error = validate_password(password)
    else:
        error = None
    return error


def validate_password(password):
    specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    if len(password) > 15:
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
