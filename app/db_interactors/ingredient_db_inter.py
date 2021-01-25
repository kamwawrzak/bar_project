from app import db
from app.models import Ingredient


class IngredientDbInter:

    def get_ingredients(self, drink_id):
        """Ingredients getter.

        Function find all Ingredient objects assigned to Drink and returns list
        of these objects.

        Parameters
        ----------
        drink_id: int

        Returns
        ----------
        []
            List of Ingredient objects.
        """
        return Ingredient.query.filter_by(drink=drink_id).all()

    def add_ingredients(self, ingredients, drink):
        """Add ingredients to database.

        Function accepts list of ingredients and drink object. Next it creates
        new Ingredient object for every position in the list and assign it to
        Drink object. Next it add the objects to database.

        Parameters
        ----------
        ingredients: []
        drink: Drink
        """
        for i in ingredients:
            ingredient = Ingredient(ingr_name=i['ingredient'].lower(),
                                    ingr_amount=i['amount'],
                                    ingr_unit=i['unit'],
                                    drink=drink.drink_id)
            db.session.add(ingredient)
        db.session.commit()

    def delete_ingredients(self, drink_id):
        """Delete drink's ingredients.

        Function deletes all Ingredients assigned to specific Drink.

        Parameters
        ----------
        drink_id: int
        """
        ingredients = IngredientDbInter().get_ingredients(drink_id)
        for i in ingredients:
            db.session.delete(i)
        db.session.commit()

    def update_ingredients(self, drink, new_ingr):
        """Update ingredients.

        Function deletes all current drink's ingredients and assign list of new
        ingredients.

        Parameters
        ----------
        drink: Drink
        new_ingr: []
        """
        IngredientDbInter().delete_ingredients(drink.drink_id)
        IngredientDbInter().add_ingredients(new_ingr, drink)
