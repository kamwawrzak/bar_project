from app.db_interactors.comment_db_inter import CommentDbInter
from app.interactors.web_inter import WebInter

from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_required

comment_bp = Blueprint('comment_bp', __name__)


@comment_bp.route('/v1/drink/<drink_id>/comment', methods=['POST'])
@login_required
def add_comment(drink_id):
    """Add new comment.

    POST: Get comment data and add new Comment object to database.
          Flash confirmation and redirect to drink page. Only logged in users
          can use this route.

    Parameters
    ----------
    drink_id: int
    """
    if request.method == 'POST':
        d = WebInter().get_comment_data(drink_id)
        CommentDbInter().add_comment(author=d['author'],
                                     author_nick=d['author_nick'],
                                     drink=d['drink'],
                                     content=d['content'],
                                     date=d['date'])
        flash('Your comment has been added', category='success')
        return redirect(url_for('drink_bp.display_drink', drink_id=drink_id))


@comment_bp.route('/v1/drink/<drink_id>/comment/delete/<comment_id>',
                  methods=['GET'])
@login_required
def delete_comment(comment_id, drink_id):
    """Delete comment.

    GET: Route accepts comment_id as argument and deletes the Comment from
         database. Next it flash confirmation and redirect to drink page.
         Only logged in users can use this route.

    Parameters
    ----------
    comment_id: int
    drink_id: int
    """
    CommentDbInter().delete_comment(comment_id)
    flash('Comment has been deleted.', category='success')
    return redirect(url_for('drink_bp.display_drink', drink_id=drink_id))


@comment_bp.route('/v1/drink/<drink_id>/comment/edit/<comment_id>',
                  methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id, drink_id):
    """Update comment.

        GET: Render template 'update_comment.html' allowing to edit comment
             body.
        POST: Update comment body and flash confirmation. Next redirects to
              drink page.
        Only logged in users can use this route.

        Parameters
        ----------
        comment_id: int
        drink_id: int
        """
    comment = CommentDbInter().get_comment(comment_id)
    if request.method == 'POST':
        CommentDbInter().update_comment(comment)
        flash('Your comment is updated.', category='success')
        return redirect(url_for('drink_bp.display_drink', drink_id=drink_id))
    else:
        return render_template('update_comment.html', title='Update comment',
                               comment=comment)
