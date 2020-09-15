from app import db
from app.interactors.drink_interactors import DrinkInteractors
from app.interactors.web_interactors import WebInteractors
from app.models import Drink

from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_required

CATEGORIES = ['whisky/bourbon', 'vodka', 'rum', 'gin', 'tequila/mezcal',
              'other']
TECHNIQUES = ['stir', 'shake', 'stir/shake', 'build', 'other']

drink_bp = Blueprint('drink_bp', __name__)


@login_required
@drink_bp.route('/v1/add_drink', methods=['GET', 'POST'])
def add_drink():
    if request.method == 'GET':
        return render_template('add_drink.html', title='Add Drink',
                               categories=CATEGORIES, techniques=TECHNIQUES)
    else:
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
    drink = DrinkInteractors().get_drink(drink_id=drink_id)
    ingredients = DrinkInteractors().get_ingredients(drink)
    return render_template('drink_page.html', title=drink.name, drink=drink,
                           ingredients=ingredients)


@drink_bp.route('/v1/drinks/<category>', methods=['GET', 'POST'])
def display_category(category):
    print(category)
    if category == 'all':
        drinks = DrinkInteractors().get_drinks()
    else:
        drinks = DrinkInteractors().search_by_category(category)
    return render_template('search_results.html', title=category.upper(),
                           drinks=drinks)


@login_required
@drink_bp.route('/v1/drink/delete/<drink_id>')
def delete_drink(drink_id):
    drink = DrinkInteractors().get_drink(drink_id)
    db.session.delete(drink)
    db.session.commit()
    return redirect(url_for('profile_bp.profile'))
