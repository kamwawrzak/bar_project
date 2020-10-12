from app import db
from app.interactors.drink_interactors import DrinkInteractors
from app.interactors.img_interactors import ImgInteractors
from app.interactors.user_interactors import UserInteractors
from app.interactors.validators import Validators
from app.interactors.web_interactors import WebInteractors


from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import current_user, login_required, logout_user

from werkzeug.security import check_password_hash, generate_password_hash


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/v1/profile/<user_id>', methods=['GET'])
def display_profile(user_id):
    user = UserInteractors().get_user(user_id)
    img = ImgInteractors().get_img_path(user, 'user')
    return render_template('profile.html', title=user.nick, user=user, img=img)


@login_required
@profile_bp.route('/v1/profile/manage/<user_id>')
def manage_profile(user_id):
    user = UserInteractors().get_user(user_id)
    return render_template('manage_profile.html', title=user.nick)


@profile_bp.route('/v1/user_drinks/<user_id>')
def user_drinks(user_id):
    drinks = DrinkInteractors().search_by_user(user_id)
    return render_template('search_results.html', title='Your Drinks',
                           drinks=drinks)


@login_required
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


@login_required
@profile_bp.route('/v1/profile/<user_id>/update_img', methods=['GET', 'POST'])
def update_profile_pic(user_id):
    user = UserInteractors().get_user(user_id)
    current_img = ImgInteractors().get_img_path(user, 'user')
    if request.method == 'POST':
        img = request.files['file']
        if img:
            if user.image != 'default.jpg':
                ImgInteractors().delete_img(user, 'user')
            img_name = ImgInteractors().upload_img(img, user_id, 'user')
            user.image = img_name
            db.session.commit()
        return redirect('/v1/profile/{}'.format(user_id))
    else:
        return render_template('profile_img.html', title=user.nick,
                               img=current_img)


@login_required
@profile_bp.route('/v1/profile/<user_id>/delete_pic')
def delete_profile_pic(user_id):
    user = UserInteractors().get_user(user_id)
    ImgInteractors().delete_img(user, 'user')
    return redirect('/v1/profile/{}'.format(user_id))


@login_required
@profile_bp.route('/v1/profile/delete/confirm', methods=['GET'])
def confirm_delete():
    return render_template('delete_account.html', title='Delete account')


@login_required
@profile_bp.route('/v1/profile/delete/<user_id>')
def delete_account(user_id):
    user = UserInteractors().get_user(user_id)
    drinks = DrinkInteractors().search_by_user(user.user_id)
    if user.image != 'default.jpg':
        ImgInteractors().delete_img(user, 'user')
    for d in drinks:
        if d.image != 'default.jpg':
            ImgInteractors().delete_img(d, 'drink')
        db.session.delete(d)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Account deleted successfully')
    return redirect(url_for('home_bp.index'))
