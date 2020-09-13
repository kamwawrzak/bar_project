import pickle

from app.models import Drink


class DbInteractors:

    def get_drink(self, drink_id):
        drink = Drink.query.filter_by(drink_id=drink_id).first()
        return drink

    def get_ingredients(self, drink):
        ingredients = pickle.loads(drink.ingredients)
        return ingredients

    def get_drinks_from_db(self):
        drinks = Drink.query.order_by(Drink.name).all()
        return drinks

    def drinks_by_name(self, search_words):
        d = None
        words = search_words['search'].split(' ')
        drinks = DbInteractors().get_drinks_from_db()
        for w in words:
            d = [drink for drink in drinks if w in drink.name]
        return d
