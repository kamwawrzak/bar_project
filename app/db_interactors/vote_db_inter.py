from app import db
from app.interactors.vote_inter import VoteInter
from app.models import Vote


class VoteDbInter:

    def get_drink_votes(self, drink_id):
        """Drink votes getter.

        Function returns list of Vote objects assigned to specific Drink.

        Parameters
        ----------
        drink_id: int

        Returns
        -------
        []
            List of Vote objects.
        """
        return Vote.query.filter_by(drink=drink_id).all()

    def get_user_votes(self, user_id):
        """Drink votes getter.

        Function returns list of Vote objects assigned to specific User.

        Parameters
        ----------
        user_id: int

        Returns
        -------
        []
            List of Vote objects.
        """
        return Vote.query.filter_by(user=user_id).all()

    def delete_drink_votes(self, drink_id):
        """Delete votes assigned to drink.

        Function gets Vote objects assigned to Drink and delete them from
        database.

        Parameters
        ----------
        drink_id: int
        """
        votes = VoteDbInter().get_drink_votes(drink_id)
        for v in votes:
            db.session.delete(v)
            db.session.commit()

    def delete_user_votes(self, user_id):
        """Delete votes assigned to user.

        Function gets Vote objects assigned to User and delete them from
        database.

        Parameters
        ----------
        user_id: int
        """
        votes = VoteDbInter().get_user_votes(user_id)
        for v in votes:
            db.session.delete(v)
            db.session.commit()

    def check_new_vote(self, drink_id, user_id):
        """Check new vote.

        Function checks if specific User already added Vote for specific Drink.

        Parameters
        ----------
        drink_id: int
        user_id: int

        Returns
        -------
        boolean
            If returns False it means that Vote exists in database and it value
            must be overwritten.
            If returns True it means that Vote doesn't exist and it new vote
            can be added.
        """
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
        """Add new Vote.

        Function checks if the same Vote as v exists in database. If it exists
        it overwrites its value. Otherwise it adds new Vote object do database.

        Parameters
        ----------
        drink: Drink
            drink_id property of Drink object
        v: Vote
        """
        if VoteDbInter().check_new_vote(v.drink, v.user):
            db.session.add(v)
        else:
            current_vote = Vote.query.filter_by(drink=v.drink,
                                                user=v.user).first()
            current_vote.value = v.value
        VoteDbInter().assign_rate(drink)
        db.session.commit()

    def assign_rate(self, drink):
        """Assign average Drink rate.

        Function gets all Votes of specific Drink object and calculates its
        average rate. Next it assign this value to Drink's avg_property.

        Parameters
        ----------
        drink: Drink
        """
        votes = VoteDbInter().get_drink_votes(drink.drink_id)
        rate = VoteInter().calc_avg_rate(votes)
        drink.avg_rate = rate
        db.session.commit()
