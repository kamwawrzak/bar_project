from app.models import Comment


class CommentInteractors:

    def get_drink_comments(self, drink_id):
        comments = Comment.query.filter_by(drink=drink_id).all()
        return comments

    def get_comment(self, comment_id):
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        return comment
