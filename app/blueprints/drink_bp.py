from app.db_interactors.comment_db_inter import CommentDbInter
from app.db_interactors.drink_db_inter import DrinkDbInter
from app.db_interactors.user_db_inter import UserDbInter
from app.interactors.drink_inter import DrinkInter
from app.interactors.img_inter import ImgInter
from app.interactors.web_inter import WebInter
from app.models import Drink

from config import Config

from flask import (Blueprint, flash, jsonify, make_response, redirect,
                   render_template, request, url_for)

from flask_login import current_user, login_required


drink_bp = Blueprint('drink_bp', __name__)


@login_required
@drink_bp.route('/v1/add_drink', methods=['GET', 'POST'])
def add_drink():
    if request.method == 'GET':
        return render_template('add_drink.html', title='Add Drink',
                               categories=Drink.CATEGORIES,
                               techniques=Drink.TECHNIQUES)
    else:
        d = WebInter().get_drink_data()
        default_link = Config.S3_LOCATION + 'images/drinks/default.jpg'
        img = request.files['file']
        new_drink = Drink(name=d['name'].capitalize(),
                          category=d['category'],
                          technique=d['technique'],
                          author=d['author'],
                          author_nick=d['author_nick'],
                          description=d['description'],
                          preparation=d['preparation'],
                          ingredients=d['ingredients'],
                          add_date=d['add_date'],
                          image=default_link)
        DrinkDbInter().add_drink(new_drink, img)
        flash('Drink added successfully.', category='success')
        return redirect(url_for('home_bp.index'))


@drink_bp.route('/v1/drink/<drink_id>', methods=['GET'])
def display_drink(drink_id):
    drink = DrinkDbInter().get_drink(drink_id)
    ingredients = DrinkInter().get_ingredients(drink)
    comments = CommentDbInter().get_drink_comments(drink_id)
    author = UserDbInter().get_user(drink.author).nick
    DrinkDbInter().views_counter(drink)
    return render_template('drink_page.html', title=drink.name, drink=drink,
                           ingredients=ingredients, comments=comments,
                           author=author)


@drink_bp.route('/v1/most_viewed', methods=['GET'])
def most_viewed():
    d = DrinkDbInter().get_most_viewed()
    return make_response(jsonify(d), 200)


@drink_bp.route('/v1/top_rated', methods=['GET'])
def top_rated():
    d = DrinkDbInter().get_top_rated()
    return make_response(jsonify(d), 200)


@login_required
@drink_bp.route('/v1/user_drinks/<user_id>')
def user_drinks(user_id):
    msg = None
    drinks = DrinkDbInter().search_by_user(user_id)
    if len(drinks) == 0:
        msg = 'There are no drinks.'
    return render_template('user_drinks.html', title='Your Drinks',
                           drinks=drinks, msg=msg)


@login_required
@drink_bp.route('/v1/drink/delete/<drink_id>', methods=['GET', 'POST'])
def delete_drink(drink_id):
    drink = DrinkDbInter().get_drink(drink_id)
    comments = CommentDbInter().get_drink_comments(drink_id)
    for c in comments:
        CommentDbInter().delete_comment(c.comment_id)
    DrinkDbInter().delete_drink(drink_id)
    ImgInter().delete_img(drink)
    return redirect('/v1/user_drinks/{}'.format(current_user.user_id))


@login_required
@drink_bp.route('/v1/drink/update/<drink_id>', methods=['GET', 'POST'])
def update_drink(drink_id):
    drink = DrinkDbInter().get_drink(drink_id)
    ingredients = DrinkInter().get_ingredients(drink)
    ingr_number = len(ingredients)
    if request.method == 'POST':
        d = WebInter().get_drink_data()
        img = request.files['file']
        DrinkDbInter().update_drink(drink=drink,
                                    name=d['name'],
                                    category=d['category'],
                                    technique=d['technique'],
                                    description=d['description'],
                                    preparation=d['preparation'],
                                    ingredients=d['ingredients'],
                                    img=img)
        return redirect('/v1/drink/{}'.format(drink_id))

    else:
        return render_template('update_drink.html', title='Update drink',
                               drink=drink, techniques=Drink.TECHNIQUES,
                               categories=Drink.CATEGORIES,
                               ingredients=ingredients,
                               ingr_number=ingr_number)


@login_required
@drink_bp.route('/v1/drink/<drink_id>/delete_image')
def delete_drink_pic(drink_id):
    drink = DrinkDbInter().get_drink(drink_id)
    ImgInter().delete_img(drink)
    return redirect('/v1/drink/update/{}'.format(drink_id))
