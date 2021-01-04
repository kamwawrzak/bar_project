from app.db_interactors.user_db_inter import UserDbInter
from app.interactors.validators import Validators
from app.interactors.web_inter import WebInter

from flask import Blueprint, flash, redirect, render_template, request, url_for

import werkzeug
from werkzeug.security import generate_password_hash


register_bp = Blueprint('register_bp', __name__)


@register_bp.route('/v1/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html', title='Registration')
    else:
        d = WebInter().get_user_data()
        error = Validators().validate_register_data(d['email'],
                                                    d['nick'],
                                                    d['password'],
                                                    d['confirm_pass'])
        img = request.files['file']
        if error is None:
            pass_hash = generate_password_hash(d['password'], method='SHA256')
            try:
                UserDbInter().add_user(email=d['email'],
                                       nick=d['nick'],
                                       password=pass_hash,
                                       img=img,
                                       user_type='regular')
                flash('Your account has been created.', category='success')
                return redirect(url_for('login_bp.login'))
            except werkzeug.exceptions.BadRequest:
                flash('Incorrect file format. Please use .jpg .jpeg or .png',
                      category='error')
                return redirect(request.referrer)
            except werkzeug.exceptions.RequestEntityTooLarge:
                flash('The added file is too large. It should be < 1MB.',
                      category='error')
                return redirect(request.referrer)
        else:
            flash(error, category='error')
            return redirect(url_for('register_bp.register_user'))
