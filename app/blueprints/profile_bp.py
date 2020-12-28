from app.db_interactors.img_db_inter import ImgDbInter
from app.db_interactors.search_db_inter import SearchDbInter
from app.db_interactors.user_db_inter import UserDbInter
from app.interactors.img_inter import ImgInter
from app.interactors.validators import Validators
from app.interactors.web_inter import WebInter


from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import current_user, login_required, logout_user

from werkzeug.security import check_password_hash

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/v1/profile/<user_id>/<page>', methods=['GET'])
def display_profile(user_id, page):
    msg = None
    user = UserDbInter().get_user(user_id)
    drinks = SearchDbInter().search_by_user(user_id, int(page))
    if not drinks:
        msg = 'This user did not add any drinks yet.'
    return render_template('profile.html', title=user.nick, user=user,
                           drinks=drinks, msg=msg, user_id=user_id)


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
                flash(e, category='error')
            else:
                UserDbInter().update_password(d['newpass'])
                flash('Password has been changed successfully.',
                      category='success')
            return redirect(url_for('profile_bp.display_profile',
                                    user_id=current_user.user_id,
                                    page=1))
        else:
            flash('Incorrect current password.', category='error')
            return redirect(url_for('profile_bp.change_password'))


@login_required
@profile_bp.route('/v1/profile/<user_id>/update_img', methods=['GET', 'POST'])
def update_profile_pic(user_id):
    user = UserDbInter().get_user(user_id)
    if request.method == 'POST':
        img = request.files['file']
        if img:
            if user.image != ImgInter().get_default_img('user'):
                ImgInter().delete_img(user)
            img_link = ImgInter().upload_img(img, user)
            ImgDbInter().update_db_image(user, img_link)
        return redirect(url_for('profile_bp.display_profile',
                                user_id=user_id,
                                page=1))
    else:
        return render_template('profile_img.html', title=user.nick,
                               user=current_user)


@login_required
@profile_bp.route('/v1/profile/<user_id>/delete_pic')
def delete_profile_pic(user_id):
    user = UserDbInter().get_user(user_id)
    ImgInter().delete_img(user)
    return redirect(url_for('profile_bp.display_profile', user_id=user_id,
                            page=1))


@login_required
@profile_bp.route('/v1/profile/delete/<user_id>', methods=['GET', 'POST'])
def delete_account(user_id):
    if request.method == 'POST':
        if current_user.oauth_user is False:
            d = WebInter().get_form_data('password')
            if not check_password_hash(current_user.password_hash,
                                       d['password']):
                flash('Incorrect password.', category='error')
                return redirect(url_for('profile_bp.delete_account',
                                        user_id=user_id))
            UserDbInter().delete_user(user_id)
            logout_user()
            flash('Account deleted successfully.', category='success')
            return redirect(url_for('home_bp.index'))
        else:
            if request.form.get('option') == 'True':
                UserDbInter().delete_user(user_id)
                logout_user()
                flash('Account deleted successfully.', category='success')
                return redirect(url_for('home_bp.index'))
            else:
                return redirect(url_for('profile_bp.display_profile',
                                        user_id=user_id, page=1))
    else:
        return render_template('delete_account.html', title='Delete account')
