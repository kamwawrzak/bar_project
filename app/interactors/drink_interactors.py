import pickle

from app.models import Drink


class DrinkInteractors:

    def get_drink(self, drink_id):
        drink = Drink.query.filter_by(drink_id=drink_id).first()
        return drink

    def get_ingredients(self, drink):
        ingredients = pickle.loads(drink.ingredients)
        return ingredients

    def get_drinks(self):
        drinks = Drink.query.order_by(Drink.name).all()
        return drinks

    def search_by_name(self, search_string):
        drinks = DrinkInteractors().get_drinks()
        d = [drink for drink in drinks if search_string.upper() ==
             drink.name.upper()]
        return d

    def search_by_ingredient(self, search_string):
        d = []
        drinks = DrinkInteractors().get_drinks()
        for drink in drinks:
            ingredients = DrinkInteractors().get_ingredients(drink)
            i = DrinkInteractors().capitalize_keys(ingredients)
            print(i)
            print(search_string.upper())
            for k in i.items():
                if search_string.upper() in k:
                    d.append(drink)
        return d

    def search_by_category(self, category):
        drinks = Drink.query.filter_by(category=category).all()
        return drinks

    def search_by_user(self, user_id):
        drinks = Drink.query.filter_by(author=user_id).all()
        return drinks

    def capitalize_keys(self, d):
        result = {}
        for k, v in d.items():
            upp = k.upper()
            result[upp] = v
        return result