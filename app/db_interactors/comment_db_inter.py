from app import db
from app.interactors.web_inter import WebInter
from app.models import Comment


class CommentDbInter:

    def get_drink_comments(self, drink_id):
        """Drink comments getter.

        Function returns list of comments assigned to drink.

        Parameters
        ----------
        drink_id: int

        Returns
        -------
        []
            List of Comment objects assigned to the Drink.
        """
        return Comment.query.filter_by(
            drink=drink_id).order_by(Comment.date).all()

    def get_user_comments(self, user_id):
        """User comments getter.

        Function returns list of comments assigned to user.

        Parameters
        ----------
        user_id: int

        Returns
        -------
        []
            List of Comment objects assigned to the User.
        """
        return Comment.query.filter_by(author=user_id).all()

    def get_comment(self, comment_id):
        """Comment getter.

        Function returns single Comment object.

        Parameters
        ----------
        comment_id: int

        Returns
        -------
        Comment
            Single Comment object.
        """
        return Comment.query.filter_by(comment_id=comment_id).first()

    def add_comment(self, author, author_nick, drink, content, date):
        """Add comment to database.

        Function creates new Comment object and add it to database.

        Parameters
        ----------
        author: int
            Author equals user_id parameter of User model.
        author_nick: string
            Author_nick equals nick parameter of User model.
        drink: int
            Drink equals drink_id paramter of Drink model.
        content: string
            Body of comment added by user.
        date: datetime
            Current date and time.
        """
        new_comment = Comment(author=author,
                              author_nick=author_nick,
                              drink=drink,
                              content=content,
                              date=date)
        db.session.add(new_comment)
        db.session.commit()

    def update_comment(self, comment):
        """Update comment body.

        Function assign new comment body passed by HTML form to content
        parameter of current Comment object.

        Parameters
        ----------
        comment: Comment
        """
        comment.content = WebInter().get_form_data('content')
        db.session.commit()

    def delete_comment(self, comment_id):
        """Delete comment.

        Function deletes single Comment object from database.

        Parameters
        ----------
        comment_id: int
        """
        comment = CommentDbInter().get_comment(comment_id)
        db.session.delete(comment)
        db.session.commit()

    def delete_many_comments(self, drink_id=None, user_id=None):
        """Delete many Comment objects.

        Function deletes all drink assigned to specific Drink or User object.

        Parameters
        ----------
        drink_id: int
            If this argument is passed the function will delete all comments
            of this Drink.
        user_id: int
            If this argument is passed the function will delete all comments
            of this User.
        """
        if drink_id is not None:
            comments = CommentDbInter().get_drink_comments(drink_id)
        elif user_id is not None:
            comments = CommentDbInter().get_user_comments(user_id)
        else:
            pass
        if len(comments) > 0:
            for c in comments:
                db.session.delete(c)
            db.session.commit()
