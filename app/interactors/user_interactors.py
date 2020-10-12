from app.models import RegularUser


class UserInteractors:

    def get_user(self, user_id):
        user = RegularUser.query.filter_by(user_id=user_id).first()
        return user
