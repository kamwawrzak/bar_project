from app.db_interactors import DbInteractors
from app.web_interactors import WebInteractors

from flask import Blueprint, render_template

search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/v1/search', methods=['GET', 'POST'])
def search_drink():
    search_word = WebInteractors().get_form_data('search')
    drinks = DbInteractors().drinks_by_name(search_word)
    return render_template('search_results.html', title='Search results',
                           drinks=drinks)
