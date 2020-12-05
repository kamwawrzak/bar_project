from app.db_interactors.vote_db_inter import VoteDbInter
from app.interactors.vote_inter import VoteInter
from app.models import Vote

from flask import Blueprint, jsonify, make_response, request

from flask_login import login_required


vote_bp = Blueprint('vote_bp', __name__)


@login_required
@vote_bp.route('/v1/add_vote', methods=['POST'])
def add_vote():
    vote_data = request.json['drink_id']
    vote_data1 = request.json['user_id']
    vote_data2 = request.json['value']
    new_vote = Vote(drink=int(vote_data[0]),
                    user=int(vote_data1[0]),
                    value=int(vote_data2[0]))
    VoteDbInter().add_vote(new_vote)
    return make_response(jsonify({'msg': 'Vote added'}), 200)


@vote_bp.route('/v1/display_rate/<drink_id>', methods=['GET'])
def display_drink_rate(drink_id):
    votes = VoteDbInter().get_drink_votes(drink_id)
    amount = len(votes)
    avg_rate = VoteInter().calc_avg_rate(votes)
    return make_response(jsonify({'rate': avg_rate, 'amount': amount}), 200)