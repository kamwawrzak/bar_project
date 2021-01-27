from app.models import Drink, Ingredient

from config import Config


class SearchDbInter:

    def get_ingredients_by_name(self, search):
        """Ingredients by name getter.

        Function returns list of ingredients where Ingredient name property
        equals search string.

        Parameters
        ----------
        search: string

        Returns
        ----------
        []
            List of Ingredient objects.
        """
        return Ingredient().query.filter_by(ingr_name=search.lower()).all()

    def get_drinks_by_ingredient(self, search, page):
        """Drinks by ingredients getter.

        Function gets list of ingredients and then creates list of drinks
        connected to that ingredients. At the end it return Pagination object
        of the Drinks in alphabetical order.

        Parameters
        ----------
        search: string
        page: int

        Returns
        ----------
        Pagination
            Pagination object including Drink objects.
        """
        ingredients = SearchDbInter().get_ingredients_by_name(search)
        d_ids = [i.drink for i in ingredients]
        drinks = Drink.query.filter(Drink.drink_id.in_(d_ids)).order_by(
            Drink.name).paginate(page=page, per_page=Config().PER_PAGE)
        return drinks

    def get_drinks_by_name(self, search, page):
        """Drinks by name getter.

        Function find all Drink objects where Drink name property equals search
        string. It returns Pagination object including objects in alphabetical
        order.

        Parameters
        ----------
        search: string
        page: int

        Returns
        ----------
        Pagination
            Pagination object including Drink objects.
        """
        drinks = Drink.query.filter_by(name=search.lower()).order_by(
            Drink.name).paginate(page=page, per_page=Config().PER_PAGE)
        return drinks

    def search_by_category(self, category, page):
        """Drinks by category getter.

        Function find all Drink objects where Drink category property equals
        category string. It returns Pagination object including objects in
        alphabetical order.

        Parameters
        ----------
        category: string
        page: int

        Returns
        ----------
        Pagination
            Pagination object including Drink objects.
        """
        drinks = Drink.query.filter_by(category=category).order_by(
            Drink.name).paginate(page=page, per_page=Config().PER_PAGE)
        return drinks

    def search_by_user(self, user_id, page):
        """Drinks by name getter.

        Function find all Drink objects asssigned to specific User object.
        It returns Pagination object including objects in alphabetical order.

        Parameters
        ----------
        user_id: int
        page: int

        Returns
        ----------
        Pagination
            Pagination object including Drink objects.
        """
        drinks = Drink.query.filter_by(author=user_id).order_by(
            Drink.name).paginate(page=page, per_page=Config().PER_PAGE)
        return drinks
