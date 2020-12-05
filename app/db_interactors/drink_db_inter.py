from app import db
from app.interactors.img_inter import ImgInter
from app.models import Drink

from flask_login import current_user

from sqlalchemy import func


class DrinkDbInter:

    def get_drink(self, drink_id):
        drink = Drink.query.filter_by(drink_id=drink_id).first()
        return drink

    def get_drinks(self):
        drinks = Drink.query.order_by(Drink.name).all()
        return drinks

    def search_by_category(self, category):
        drinks = Drink.query.filter_by(category=category).all()
        return drinks

    def search_by_user(self, user_id):
        drinks = Drink.query.filter_by(author=user_id).all()
        return drinks

    def add_drink(self, drink, img=None):
        db.session.add(drink)
        current_user.drinks_number += 1
        if img:
            img_name = ImgInter().upload_img(img, drink)
            drink.image = img_name
        db.session.commit()

    def update_drink(self, drink, name, category, technique, description,
                     preparation, ingredients, img):
        drink.name = name
        drink.category = category
        drink.technique = technique
        drink.description = description
        drink.preparation = preparation
        drink.ingredients = ingredients
        if img:
            if drink.image != 'default.jpg':
                ImgInter().delete_img(drink)
            img_name = ImgInter().upload_img(img, drink)
            drink.image = img_name
        db.session.commit()

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

    def delete_drink(self, drink_id):
        drink = DrinkDbInter().get_drink(drink_id)
        db.session.delete(drink)
        if drink.image != 'default.jpg':
            ImgInter().delete_img(drink)
        current_user.drinks_number -= 1
        db.session.commit()
