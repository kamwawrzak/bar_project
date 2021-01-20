from app import db
from app.interactors.vote_inter import VoteInter
from app.models import Vote


class VoteDbInter:

    def get_drink_votes(self, drink_id):
        return Vote.query.filter_by(drink=drink_id).all()

    def get_user_votes(self, user_id):
        return Vote.query.filter_by(user=user_id).all()

    def delete_drink_votes(self, drink_id):
        votes = VoteDbInter().get_drink_votes(drink_id)
        for v in votes:
            db.session.delete(v)
            db.session.commit()

    def delete_user_votes(self, user_id):
        votes = VoteDbInter().get_user_votes(user_id)
        for v in votes:
            db.session.delete(v)
            db.session.commit()

    def check_new_vote(self, drink_id, user_id):
        votes = VoteDbInter().get_drink_votes(drink_id)
        if len(votes) > 0:
            for v in votes:
                if user_id == v.user:
                    return False
                else:
                    return True
        else:
            return True

    def add_vote(self, drink, v):
        if VoteDbInter().check_new_vote(v.drink, v.user):
            db.session.add(v)
        else:
            current_vote = Vote.query.filter_by(drink=v.drink,
                                                user=v.user).one()
            db.session.delete(current_vote)
            db.session.add(v)
        VoteDbInter().assign_rate(drink)
        db.session.commit()

    def assign_rate(self, drink):
        votes = VoteDbInter().get_drink_votes(drink.drink_id)
        rate = VoteInter().calc_avg_rate(votes)
        drink.avg_rate = rate
