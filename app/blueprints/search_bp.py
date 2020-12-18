from app.db_interactors.drink_db_inter import DrinkDbInter
from app.db_interactors.search_db_inter import SearchDbInter
from app.interactors.web_inter import WebInter
from app.models import Drink

from flask import Blueprint, render_template, request


search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/v1/search', methods=['GET', 'POST'])
def search_drinks():
    if request.method == 'GET':
        return render_template('search.html', title='Search',
                               search_criteria=Drink.SEARCH_CRITERIA)
    else:
        criteria = WebInter().get_form_data('criteria')['criteria']
        search_string = WebInter().get_form_data('search')['search']
        if criteria == 'drink name':
            drinks = SearchDbInter().get_drinks_by_name(search_string)
        else:
            drinks = SearchDbInter().get_drinks_by_ingredient(search_string)
        msg = 'Search results for: "{}"'.format(search_string)
        if len(drinks) == 0:
            msg = 'There are no search results for: "{}"'.format(search_string)
        return render_template('search_results.html', title='Search results',
                               drinks=drinks, msg=msg)


@search_bp.route('/v1/drinks/<category>', methods=['GET', 'POST'])
def display_category(category):
    category = category.replace('_', '/')
    if category == 'all':
        drinks = DrinkDbInter().get_all_drinks()
    else:
        drinks = SearchDbInter().search_by_category(category)
    msg = '{} Drinks:'.format(category.capitalize())
    return render_template('search_results.html', title=category.capitalize() +
                           ' Drinks', drinks=drinks, msg=msg)
