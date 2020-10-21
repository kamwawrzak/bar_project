import pickle

from app.db_interactors.drink_db_inter import DrinkDbInter


class DrinkInter:

    def unpickle_ingredients(self, drink):
        ingredients = pickle.loads(drink.ingredients)
        return ingredients

    def get_shorter_ingredients(self, drink):
        d = {}
        ingredients = DrinkInter().unpickle_ingredients(drink)
        for i in ingredients:
            d[i['ingredient']] = i['amount']
        return d

    def search_by_name(self, search_string):
        drinks = DrinkDbInter().get_drinks()
        d = [drink for drink in drinks if search_string.upper() ==
             drink.name.upper()]
        return d

    def search_by_ingredient(self, search_string):
        d = []
        drinks = DrinkDbInter().get_drinks()
        for drink in drinks:
            ingredients = DrinkInter().get_shorter_ingredients(drink)
            i = DrinkInter().capitalize_keys(ingredients)
            for k in i.items():
                if search_string.upper() in k:
                    d.append(drink)
        return d

    def capitalize_keys(self, d):
        result = {}
        for k, v in d.items():
            upp = k.upper()
            result[upp] = v
        return result
