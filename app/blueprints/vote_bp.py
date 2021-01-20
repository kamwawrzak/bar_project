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
    vote_drink = request.json['drink_id']
    vote_user = request.json['user_id']
    vote_value = request.json['value']
    if len(vote_user) == 0:
        return make_response(jsonify({'msg': 'Vote not added.'}), 401)
    else:
        drink = DrinkDbInter().get_drink(vote_drink)
        new_vote = Vote(drink=int(vote_drink[0]),
                        user=int(vote_user[0]),
                        value=int(vote_value[0]))
        VoteDbInter().add_vote(drink, new_vote)
        return make_response(jsonify({'msg': 'Vote added'}), 200)


@vote_bp.route('/v1/display_rate/<drink_id>', methods=['GET'])
def display_drink_rate(drink_id):
    votes = VoteDbInter().get_drink_votes(drink_id)
    amount = len(votes)
    avg_rate = VoteInter().calc_avg_rate(votes)
    return make_response(jsonify({'rate': avg_rate, 'amount': amount}), 200)
