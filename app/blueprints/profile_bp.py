from app.db_interactors.img_db_inter import ImgDbInter
from app.db_interactors.user_db_inter import UserDbInter
from app.interactors.img_inter import ImgInter
from app.interactors.validators import Validators
from app.interactors.web_inter import WebInter


from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import current_user, login_required, logout_user

from werkzeug.security import check_password_hash

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/v1/profile/<user_id>', methods=['GET'])
def display_profile(user_id):
    user = UserDbInter().get_user(user_id)
    img = ImgInter().get_img_path(user)
    return render_template('profile.html', title=user.nick, user=user, img=img)


@login_required
@profile_bp.route('/v1/profile/manage/<user_id>')
def manage_profile(user_id):
    user = UserDbInter().get_user(user_id)
    return render_template('manage_profile.html', title=user.nick)


@login_required
@profile_bp.route('/v1/profile/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html', title='Change password')
    else:
        d = WebInter().get_form_data('oldpass', 'newpass', 'confirmnew')
        e = Validators().validate_pass(d['newpass'], d['confirmnew'])
        if check_password_hash(current_user.password_hash, d['oldpass']):
            if e:
                flash(e)
            else:
                UserDbInter().update_password(d['newpass'])
                flash('Password has been changed successfully.')
            return redirect(url_for('profile_bp.display_profile'))
        else:
            flash('Incorrect current password.')
            return redirect(url_for('profile_bp.change_password'))


@login_required
@profile_bp.route('/v1/profile/<user_id>/update_img', methods=['GET', 'POST'])
def update_profile_pic(user_id):
    user = UserDbInter().get_user(user_id)
    current_img = ImgInter().get_img_path(user)
    if request.method == 'POST':
        img = request.files['file']
        if img:
            if user.image != 'default.jpg':
                ImgInter().delete_img(user)
            img_name = ImgInter().upload_img(img, user)
            ImgDbInter().update_db_image(user, img_name)
        return redirect('/v1/profile/{}'.format(user_id))
    else:
        return render_template('profile_img.html', title=user.nick,
                               img=current_img)


@login_required
@profile_bp.route('/v1/profile/<user_id>/delete_pic')
def delete_profile_pic(user_id):
    user = UserDbInter().get_user(user_id)
    ImgInter().delete_img(user)
    return redirect('/v1/profile/{}'.format(user_id))


@login_required
@profile_bp.route('/v1/profile/delete/<user_id>')
def delete_account(user_id):
    UserDbInter().delete_user(user_id)
    logout_user()
    flash('Account deleted successfully')
    return redirect(url_for('home_bp.index'))


@login_required
@profile_bp.route('/v1/profile/delete/confirm', methods=['GET'])
def confirm_delete():
    return render_template('delete_account.html', title='Delete account')
