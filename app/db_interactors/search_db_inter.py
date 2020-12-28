from app.models import Drink, Ingredient

from config import Config


class SearchDbInter:

    def get_ingredients_by_name(self, search_string):
        r = Ingredient().query.filter_by(ingr_name=search_string.lower()).all()
        return r

    def get_drinks_by_ingredient(self, search_string, page):
        ingredients = SearchDbInter().get_ingredients_by_name(search_string)
        d_ids = [i.drink for i in ingredients]
        drinks = Drink.query.filter(Drink.drink_id.in_(d_ids)).paginate(
            page=page,
            per_page=Config().PER_PAGE)
        return drinks

    def get_drinks_by_name(self, search_string, page):
        search_string = search_string.lower()
        d = Drink.query.filter_by(name=search_string).paginate(
           page=page,
           per_page=Config().PER_PAGE)
        return d

    def search_by_category(self, category, page):
        drinks = Drink.query.filter_by(category=category).paginate(
            page=int(page),
            per_page=Config().PER_PAGE)
        return drinks

    def search_by_user(self, user_id, page):
        drinks = Drink.query.filter_by(author=user_id).paginate(
            page=page,
            per_page=Config().PER_PAGE)
        return drinks
