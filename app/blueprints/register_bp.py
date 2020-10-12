from app import db
from app.interactors.img_interactors import ImgInteractors
from app.interactors.validators import Validators
from app.interactors.web_interactors import WebInteractors
from app.models import RegularUser

from flask import Blueprint, flash, redirect, render_template, request, url_for

from werkzeug.security import generate_password_hash


register_bp = Blueprint('register_bp', __name__)


@register_bp.route('/v1/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html', title='Registration')
    else:
        d = WebInteractors().get_user_data()
        error = Validators().validate_register_data(d['email'],
                                                    d['nick'],
                                                    d['password'],
                                                    d['confirm_pass'])
        img = request.files['file']
        if error is None:
            pass_hash = generate_password_hash(d['password'], method='SHA256')
            new_user = RegularUser(email=d['email'], nick=d['nick'],
                                   password_hash=pass_hash,
                                   register_date=d['register_date'])
            db.session.add(new_user)
            db.session.commit()
            if img:
                img_name = ImgInteractors().upload_img(img, new_user.user_id,
                                                       'user')
                new_user.image = img_name
                db.session.commit()
            flash('You have been registered successfully')
            return redirect(url_for('login.login'))
        else:
            flash(error)
            return redirect(url_for('register_bp.register_user'))
