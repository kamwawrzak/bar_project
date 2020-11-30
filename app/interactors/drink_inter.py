import pickle

from app.db_interactors.drink_db_inter import DrinkDbInter


class DrinkInter:

    def get_ingredients(self, drink):
        ingredients = pickle.loads(drink.ingredients)
        return ingredients

    def get_ingr_list(self, drink):
        ingr_names = []
        ingredients = DrinkInter().get_ingredients(drink)
        for i in ingredients:
            i_name = i['ingredient'].upper()
            ingr_names.append(i_name)
        return ingr_names

    def search_by_name(self, search_string):
        drinks = DrinkDbInter().get_drinks()
        d = [drink for drink in drinks if search_string.upper() ==
             drink.name.upper()]
        return d

    def search_by_ingredient(self, search_string):
        d = []
        drinks = DrinkDbInter().get_drinks()
        for drink in drinks:
            ingr_list = DrinkInter().get_ingr_list(drink)
            if search_string.upper() in ingr_list:
                d.append(drink)
        return d

    def ingredient_iterator(self, i):
        return i
