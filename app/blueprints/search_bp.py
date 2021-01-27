from app.db_interactors.drink_db_inter import DrinkDbInter
from app.db_interactors.search_db_inter import SearchDbInter
from app.interactors.web_inter import WebInter
from app.models import Drink

from flask import Blueprint, redirect, render_template, request, url_for

search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/v1/search', methods=['GET', 'POST'])
def search_drinks():
    """Search drinks.

    GET: Renders template 'search.html' allowing to type searching text.
    POST: Get search criteria and search text and pass it to display results
          routes.
    """
    if request.method == 'GET':
        return render_template('search.html', title='Search',
                               search_criteria=Drink.SEARCH_CRITERIA)
    else:
        search = WebInter().get_form_data('search')['search']
        criteria = WebInter().get_form_data('criteria')['criteria']
        return redirect(url_for('search_bp.display_results', search=search,
                                criteria=criteria, page=1))


@search_bp.route('/v1/results/<criteria>/<search>/<int:page>', methods=['GET'])
def display_results(search, criteria, page):
    """Display search results.

    GET: Renders 'search_results.html' template displaying drinks meeting
         search criteria.

    Parameters
    ----------
    search: String
        Search text introduced by user
    criteria: String
        Search criteria chosen by user - it can be 'drink_name' or 'ingredient'
    page: int
    """
    if criteria == 'drink_name':
        drinks = SearchDbInter().get_drinks_by_name(search, int(page))
    else:
        drinks = SearchDbInter().get_drinks_by_ingredient(search, int(page))
    msg = 'Search results for: "{}"'.format(search)
    if len(drinks.items) == 0:
        msg = 'There are no search results for: "{}"'.format(search)
    return render_template('search_results.html', title='Search results',
                           drinks=drinks, msg=msg, search=search,
                           criteria=criteria)


@search_bp.route('/v1/drinks/<category>/<int:page>', methods=['GET'])
def display_category(category, page):
    """Display category

    GET: Renders 'category.html' template displaying drinks in passed category.

    Parameters
    ----------
    category: String
        Name of category. It can takes values: all or any value in CATEGORY
        list in Drink model.
    page: int
    """
    category = category.replace('_', '/')
    if category == 'all':
        drinks = DrinkDbInter().get_all_drinks(page)
    else:
        drinks = SearchDbInter().search_by_category(category, page)
    msg = '{} Drinks:'.format(category.capitalize())
    title = category.capitalize() + ' Drinks'
    if len(drinks.items) == 0:
        msg = 'There are no drinks in {} category.'.format(category)
    return render_template('category.html', title=title, drinks=drinks,
                           msg=msg, category=category)
