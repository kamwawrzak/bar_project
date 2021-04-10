from app.db_interactors.drink_db_inter import DrinkDbInter
from app.db_interactors.vote_db_inter import VoteDbInter
from app.interactors.vote_inter import VoteInter
from app.models import Vote

from flask import Blueprint, jsonify, make_response, request

from flask_login import login_required


vote_bp = Blueprint('vote_bp', __name__)


@vote_bp.route('/v1/add_vote', methods=['POST'])
@login_required
def add_vote():
    """Add new vote.

        POST: Get new vote properties from JSON object and creates new Vote
              object. Next add it to database and returns response to the
              client that it has been added correctly. If there is some error
              it returns response informing that it has not been added.
    """
    data = request.json
    if len(data['user_id']) == 0:
        return make_response({'success': False, 'err': 'Unauthorized user.'}, 401)
    else:
        drink = DrinkDbInter().get_drink(data['drink_id'])
        new_vote = Vote(drink=int(data['drink_id']),
                        user=int(data['user_id']),
                        value=int(data['value']))
        VoteDbInter().add_vote(drink, new_vote)
        return make_response({'success': True, 'msg': 'Vote added successfully.'}, 200)


@vote_bp.route('/v1/display_rate/<drink_id>', methods=['GET'])
def display_drink_rate(drink_id):
    """Display drink rate.

    GET: Gets all Votes assigned to the Drink from database. Next calculate
         number of the Votes and Drink average rate. Return this information to
         the client in JSON object.
    Parameters
    ----------
    drink_id: int
    """
    votes = VoteDbInter().get_drink_votes(drink_id)
    amount = len(votes)
    avg_rate = VoteInter().calc_avg_rate(votes)
    return make_response({'success': True, 'rate': avg_rate, 'amount': amount}, 200)
