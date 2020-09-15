from app import db
from app.interactors.drink_interactors import DrinkInteractors
from app.interactors.validators import Validators
from app.interactors.web_interactors import WebInteractors
from app.models import RegularUser


from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import current_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/v1/profile')
def display_profile():
    return render_template('profile.html', title=current_user.nick)


@profile_bp.route('/v1/user_drinks/<user_id>')
def user_drinks(user_id):
    drinks = DrinkInteractors().search_by_user(user_id)
    return render_template('search_results.html', title='Your Drinks',
                           drinks=drinks)


@profile_bp.route('/v1/profile/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html', title='Change password')
    else:
        d = WebInteractors().get_form_data('oldpass', 'newpass', 'confirmnew')
        e = Validators().validate_pass(d['newpass'], d['confirmnew'])
        if check_password_hash(current_user.password_hash, d['oldpass']):
            if e:
                flash(e)
            else:
                current_user.password_hash = generate_password_hash(
                    d['newpass'], 'SHA256')
                db.session.commit()
                flash('Password has been changed successfully.')
            return redirect(url_for('profile_bp.profile'))
        else:
            flash('Incorrect password.')


@profile_bp.route('/v1/profile/delete/<user_id>', methods=['GET', 'POST'])
def delete_account(user_id):
    if request.method == 'GET':
        return render_template('delete_account.html', title='Delete account')
    else:
        d = WebInteractors().get_form_data('option')
        if d['option'] == 'True':
            user = RegularUser.query.filter_by(user_id=user_id).first()
            drinks = DrinkInteractors().search_by_user(user.user_id)
            for d in drinks:
                db.session.delete(d)
            db.session.delete(user)
            db.session.commit()
            logout_user()
            flash('Account deleted successfully')
            return redirect(url_for('home_bp.index'))
        else:
            return redirect(url_for('profile_bp.profile'))
