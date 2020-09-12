from app import db
from app.models import Drink
from app.web_interactors import WebInteractors

from flask import Blueprint, flash, redirect, url_for


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
