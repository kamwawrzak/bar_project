from app import db
from app.db_interactors.ingredient_db_inter import IngredientDbInter
from app.db_interactors.vote_db_inter import VoteDbInter
from app.interactors.img_inter import ImgInter
from app.interactors.web_inter import WebInter
from app.models import Drink

from config import Config

from flask_login import current_user

from sqlalchemy import func


class DrinkDbInter:

    """Method accepts integer drink_id as argument and returns single drink
    object from database."""
    def get_drink(self, drink_id):
        return Drink.query.filter_by(drink_id=drink_id).first()

    """Method accepts integer page argument and returns some drinks objects
    assigned to that page determined by PER_PAGE value. The drinks are sorted
    alphabetically from A to Z."""
    def get_all_drinks(self, page):
        return Drink.query.order_by(Drink.name).paginate(
                                            page=int(page),
                                            per_page=Config().PER_PAGE)

    """Method accepts integer user_id as argument and returns all Drink
    assigned to that user objects."""
    def user_all_drinks(self, user_id):
        return Drink.query.filter_by(author=user_id).all()

    def add_drink(self, drink, img=None):
        db.session.add(drink)
        current_user.drinks_number += 1
        db.session.commit()
        IngredientDbInter().add_ingredients(WebInter().get_ingredients(),
                                            drink)
        if img:
            img_name = ImgInter().upload_img(img, drink)
            drink.image = img_name
            db.session.commit()

    def update_drink(self, drink, name, category, technique, description,
                     preparation, img):
        drink.name = name
        drink.category = category
        drink.technique = technique
        drink.description = description
        drink.preparation = preparation
        if img:
            img_name = ImgInter().upload_img(img, drink)
            if drink.image != ImgInter().get_default_img('drink'):
                ImgInter().delete_img(drink)
            drink.image = img_name
        db.session.commit()

    def delete_drink(self, drink_id):
        drink = DrinkDbInter().get_drink(drink_id)
        if drink.image != ImgInter().get_default_img('drink'):
            ImgInter().delete_img(drink)
        current_user.drinks_number -= 1
        IngredientDbInter().delete_ingredients(drink_id)
        VoteDbInter().delete_drink_votes(drink_id)
        db.session.delete(drink)
        db.session.commit()

# Recommended drinks functions

    def views_counter(self, drink):
        drink.views += 1
        db.session.commit()

    def get_most_viewed(self):
        max_views = db.session.query(func.max(Drink.views))
        drinks = Drink.query.filter_by(views=max_views).all()
        drinks.sort(key=lambda x: x.avg_rate, reverse=True)
        d = {'id': drinks[0].drink_id,
             'image': drinks[0].image,
             'name': drinks[0].name}
        return d

    def get_top_rated(self):
        max_rate = db.session.query(func.max(Drink.avg_rate))
        drinks = Drink.query.filter_by(avg_rate=max_rate).all()
        drinks.sort(key=lambda x: x.views, reverse=True)
        d = {'id': drinks[0].drink_id,
             'image': drinks[0].image,
             'name': drinks[0].name}
        return d
