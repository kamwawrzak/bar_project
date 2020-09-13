from app import db
from app.db_interactors import DbInteractors
from app.models import Drink
from app.web_interactors import WebInteractors

from flask import Blueprint, flash, redirect, render_template,  url_for


drink_bp = Blueprint('drink_bp', __name__)


@drink_bp.route('/add_drink', methods=['POST'])
def add_drink_post():
    d = WebInteractors().get_drink_data()
    new_drink = Drink(name=d['name'],
                      technique=d['technique'],
                      author=d['author'],
                      description=d['description'],
                      preparation=d['preparation'],
                      ingredients=d['ingredients'])
    db.session.add(new_drink)
    db.session.commit()
    flash('Drink added successfully.')
    return redirect(url_for('index'))


@drink_bp.route('/v1/drink/<drink_id>', methods=['GET'])
def display_drink(drink_id):
    drink = DbInteractors().get_drink(drink_id=drink_id)
    ingredients = DbInteractors().get_ingredients(drink)
    return render_template('drink_page.html', title=drink.name, drink=drink,
                           ingredients=ingredients)


@drink_bp.route('/v1/drinks', methods=['GET'])
def display_drinks():
    drinks = DbInteractors().get_drinks_from_db()
    print(drinks)
    return render_template('drink.html', drinks=drinks)
