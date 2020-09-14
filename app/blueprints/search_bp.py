from app.db_interactors import DbInteractors
from app.web_interactors import WebInteractors

from flask import Blueprint, render_template

search_bp = Blueprint('search_bp', __name__)

CATEGORIES = ['whisky/bourbon', 'vodka', 'rum', 'gin', 'tequila/mezcal',
              'other']
TECHNIQUES = ['stir', 'shake', 'stir/shake', 'build', 'other']
SEARCH_CRITERIA = ['drink name', 'ingredient']


@search_bp.route('/v1/search')
def search_drinks():
    return render_template('search.html', title='Search',
                           categories=CATEGORIES,
                           search_criteria=SEARCH_CRITERIA)


@search_bp.route('/v1/search', methods=['GET', 'POST'])
def search_drink_post():
    search_criteria = WebInteractors().get_form_data('criteria')['criteria']
    search_string = WebInteractors().get_form_data('search')['search']
    if search_criteria == 'drink name':
        drinks = DbInteractors().search_by_name(search_string)
    else:
        drinks = DbInteractors().search_by_ingredient(search_string)
    return render_template('search_results.html', title='Search results',
                           drinks=drinks)
