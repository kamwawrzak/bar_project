from app import db
from app.interactors.comment_interactors import CommentInteractors
from app.interactors.drink_interactors import DrinkInteractors
from app.interactors.img_interactors import ImgInteractors
from app.interactors.web_interactors import WebInteractors
from app.models import Drink


from flask import (Blueprint, flash, redirect, render_template,
                   request, url_for)

from flask_login import current_user, login_required


CATEGORIES = ['whisky/bourbon', 'vodka', 'rum', 'gin', 'tequila/mezcal',
              'other']
TECHNIQUES = ['stir', 'shake', 'stir/shake', 'build', 'other']

drink_bp = Blueprint('drink_bp', __name__)


@login_required
@drink_bp.route('/v1/add_drink', methods=['GET', 'POST'])
def add_drink():
    img_name = 'default.jpg'
    if request.method == 'GET':
        return render_template('add_drink.html', title='Add Drink',
                               categories=CATEGORIES, techniques=TECHNIQUES)
    else:
        d = WebInteractors().get_drink_data()
        img = request.files['file']
        new_drink = Drink(name=d['name'],
                          category=d['category'],
                          technique=d['technique'],
                          author=d['author'],
                          description=d['description'],
                          preparation=d['preparation'],
                          ingredients=d['ingredients'],
                          add_date=d['add_date'])
        db.session.add(new_drink)
        current_user.drinks_number += 1

        if img:
            img_name = ImgInteractors().upload_img(img, new_drink.drink_id,
                                                   'drink')
        new_drink.image = img_name
        db.session.commit()
        flash('Drink added successfully.')
        return redirect(url_for('home_bp.index'))


@drink_bp.route('/v1/drink/<drink_id>', methods=['GET'])
def display_drink(drink_id):
    drink = DrinkInteractors().get_drink(drink_id)
    ingredients = DrinkInteractors().get_shorter_ingredients(drink)
    comments = CommentInteractors().get_drink_comments(drink_id)
    img = ImgInteractors().get_img_path(drink, 'drink')
    return render_template('drink_page.html', title=drink.name, drink=drink,
                           ingredients=ingredients, comments=comments, img=img)


@drink_bp.route('/v1/drinks/<category>', methods=['GET', 'POST'])
def display_category(category):
    if category == 'all':
        drinks = DrinkInteractors().get_drinks()
    else:
        drinks = DrinkInteractors().search_by_category(category)
    return render_template('search_results.html', title=category.upper(),
                           drinks=drinks)


@login_required
@drink_bp.route('/v1/drink/delete/<drink_id>', methods=['GET', 'POST'])
def delete_drink(drink_id):
    DrinkInteractors().delete_drink(drink_id)
    return redirect('/v1/profile/{}'.format(current_user.user_id))


@login_required
@drink_bp.route('/v1/drink/update/<drink_id>', methods=['GET', 'POST'])
def update_drink(drink_id):
    drink = DrinkInteractors().get_drink(drink_id)
    ingredients = DrinkInteractors().get_ingredients(drink)
    ingr_number = len(ingredients)
    current_image = ImgInteractors().get_img_path(drink, 'drink')
    if request.method == 'POST':
        d = WebInteractors().get_drink_data()
        img = request.files['file']
        if img:
            if drink.image != 'default.jpg':
                ImgInteractors().delete_img(drink, 'drink')
            img_name = ImgInteractors().upload_img(img, drink.drink_id,
                                                   'drink')
            drink.image = img_name
        drink.name = d['name']
        drink.category = d['category']
        drink.technique = d['technique']
        drink.description = d['description']
        drink.preparation = d['preparation']
        drink.ingredients = d['ingredients']
        db.session.commit()
        return redirect('/v1/drink/{}'.format(drink_id))

    else:
        return render_template('update_drink.html', title='Update drink',
                               drink=drink, techniques=TECHNIQUES,
                               categories=CATEGORIES, ingredients=ingredients,
                               ingr_number=ingr_number, img=current_image)


@login_required
@drink_bp.route('/v1/drink/<drink_id>/delete_image')
def delete_drink_pic(drink_id):
    drink = DrinkInteractors().get_drink(drink_id)
    ImgInteractors().delete_img(drink, 'drink')
    return redirect('/v1/drink/update/{}'.format(drink_id))
