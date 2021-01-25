from app.db_interactors.img_db_inter import ImgDbInter
from app.db_interactors.search_db_inter import SearchDbInter
from app.db_interactors.user_db_inter import UserDbInter
from app.interactors.img_inter import ImgInter
from app.interactors.validators import Validators
from app.interactors.web_inter import WebInter


from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import current_user, login_required, logout_user

import werkzeug
from werkzeug.security import check_password_hash

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/v1/profile/<user_id>/<page>', methods=['GET'])
def display_profile(user_id, page):
    """Display user profile

    GET: Render template 'profile.html' including user data and drinks added by
         the user.

    Parameters
    ----------
    user_id: int
    page: int
    """
    msg = None
    user = UserDbInter().get_user(user_id)
    drinks = SearchDbInter().search_by_user(user_id, int(page))
    if not drinks:
        msg = 'This user did not add any drinks yet.'
    return render_template('profile.html', title=user.nick, user=user,
                           drinks=drinks, msg=msg, user_id=user_id)


@profile_bp.route('/v1/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password.

    GET: Render template 'change_password.html' allowing to introduce new
         password.
    POST: Gets and validate password data introduced by user. If it's correct
          assign the hashed new password to currently logged in user password
          property. Next redirects to user profile page. If there is any issue
          flash the error and redirects to change password page.
    Only logged in users can use this route.
    """
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


@profile_bp.route('/v1/profile/<user_id>/update_img', methods=['GET', 'POST'])
@login_required
def update_profile_pic(user_id):
    """Update user image.

    GET: Renders template 'profile_img.html' allowing to upload new image.
    POST: Get currently logged in User object and image file passed by user.
          Delete current user's image and upload the new one to S3 bucket.
          Update User image property with the new image path. Next redirects to
          User profile page. If there is some issue flash error and redirects
          to update profile img page.
    Only logged in users can use this route.

    Parameters
    ---------
    user_id: int
    """
    user = UserDbInter().get_user(user_id)
    if request.method == 'POST':
        img = request.files['file']
        if img:
            try:
                img_link = ImgInter().upload_img(img, user)
                if user.image != ImgInter().get_default_img('user'):
                    ImgInter().delete_img(user)
                ImgDbInter().update_db_image(user, img_link)
                return redirect(url_for('profile_bp.display_profile',
                                        user_id=user_id, page=1))
            except werkzeug.exceptions.BadRequest:
                flash('Incorrect file format. Please use .jpg .jpeg or .png',
                      category='error')
                return redirect(request.referrer)
            except werkzeug.exceptions.RequestEntityTooLarge:
                flash('The added file is too large. It should be < 1MB.',
                      category='error')
                return redirect(request.referrer)
        else:
            flash('No image has been chosen.', category='error')
            return redirect(request.referrer)
    else:
        return render_template('profile_img.html', title=user.nick,
                               user=current_user)


@profile_bp.route('/v1/profile/<user_id>/delete_pic', methods=['GET'])
@login_required
def delete_profile_pic(user_id):
    """Delete user image.

    GET: Get currently logged in user and delete his current image from S3
         bucket. Next update User image property with default image path.
         In the end redirects to user profile.
    Only logged in users can use this route.

    Parameters
    ----------
    user_id: int
    """
    user = UserDbInter().get_user(user_id)
    ImgInter().delete_img(user)
    return redirect(url_for('profile_bp.display_profile', user_id=user_id,
                            page=1))


@profile_bp.route('/v1/profile/delete/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_account(user_id):
    """Delete user image.

    GET: Renders template 'delete_account.html' allowing to confirm if user
         wants to delete his account. For regular User account it requires
         typing password and in oauth User type it requires to choose correct
         button.
    POST: Validate if user confirm that he wants to delete account. Next
          account is deleted and user is logged out. It redirects to home page.

    Parameters
    ----------
    user_id: int
    """
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
