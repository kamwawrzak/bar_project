from app import db
from app.models import Comment

from flask import request


class CommentDbInter:

    def get_drink_comments(self, drink_id):
        comments = Comment.query.filter_by(drink=drink_id).all()
        return comments

    def get_comment(self, comment_id):
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        return comment

    def add_comment(self, author, author_nick, drink, content, date):
        new_comment = Comment(author=author,
                              author_nick=author_nick,
                              drink=drink,
                              content=content,
                              date=date)
        db.session.add(new_comment)
        db.session.commit()

    def update_comment(self, comment):
        comment.content = request.form.get('content')
        db.session.commit()

    def delete_comment(self, comment_id):
        comment = CommentDbInter().get_comment(comment_id)
        db.session.delete(comment)
        db.session.commit()
