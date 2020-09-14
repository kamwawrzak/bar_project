from app import db
from app.db_interactors import DbInteractors
from app.models import Drink
from app.web_interactors import WebInteractors

from flask import Blueprint, flash, redirect, render_template,  url_for

from flask_login import login_required
CATEGORIES = ['whisky/bourbon', 'vodka', 'rum', 'gin', 'tequila/mezcal',
              'other']
TECHNIQUES = ['stir', 'shake', 'stir/shake', 'build', 'other']

drink_bp = Blueprint('drink_bp', __name__)


@login_required
@drink_bp.route('/v1/add_drink')
def add_drink():
    return render_template('add_drink.html', title='Add Drink',
                           categories=CATEGORIES, techniques=TECHNIQUES)


@drink_bp.route('/add_drink', methods=['POST'])
def add_drink_post():
    d = WebInteractors().get_drink_data()
    new_drink = Drink(name=d['name'],
                      category=d['category'],
                      technique=d['technique'],
                      author=d['author'],
                      description=d['description'],
                      preparation=d['preparation'],
                      ingredients=d['ingredients'])
    db.session.add(new_drink)
    db.session.commit()
    flash('Drink added successfully.')
    return redirect(url_for('home_bp.index'))


@drink_bp.route('/v1/drink/<drink_id>', methods=['GET'])
def display_drink(drink_id):
    drink = DbInteractors().get_drink(drink_id=drink_id)
    ingredients = DbInteractors().get_ingredients(drink)
    return render_template('drink_page.html', title=drink.name, drink=drink,
                           ingredients=ingredients)


@drink_bp.route('/v1/drinks/all', methods=['GET'])
def display_drinks():
    drinks = DbInteractors().get_drinks()
    return render_template('search_results.html', title='Drinks',
                           drinks=drinks)


@drink_bp.route('/v1/drinks/whisky/bourbon', methods=['GET'])
def whisky_drinks():
    drinks = DbInteractors().search_by_category('whisky/bourbon')
    return render_template('search_results.html', title='category'.upper(),
                           drinks=drinks)


@drink_bp.route('/v1/drinks/rum', methods=['GET'])
def rum_drinks():
    drinks = DbInteractors().search_by_category('rum')
    return render_template('search_results.html', title='category'.upper(),
                           drinks=drinks)


@drink_bp.route('/v1/drinks/gin', methods=['GET'])
def gin_drinks():
    drinks = DbInteractors().search_by_category('gin')
    return render_template('search_results.html', title='category'.upper(),
                           drinks=drinks)


@drink_bp.route('/v1/drinks/tequila/mezcal', methods=['GET'])
def tequila_drinks():
    drinks = DbInteractors().search_by_category('tequila/mezcal')
    return render_template('search_results.html', title='category'.upper(),
                           drinks=drinks)


@drink_bp.route('/v1/drinks/vodka', methods=['GET'])
def vodka_drinks():
    drinks = DbInteractors().search_by_category('vodka')
    return render_template('search_results.html', title='category'.upper(),
                           drinks=drinks)


@drink_bp.route('/v1/drinks/other', methods=['GET'])
def other_drinks():
    drinks = DbInteractors().search_by_category('other')
    return render_template('search_results.html', title='category'.upper(),
                           drinks=drinks)
