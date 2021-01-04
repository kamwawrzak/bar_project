from app import db
from app.models import Ingredient


class IngredientDbInter:

    def get_ingredients(self, drink_id):
        ingredients = Ingredient.query.filter_by(drink=drink_id).all()
        return ingredients

    def add_ingredients(self, ingredients, drink):
        for i in ingredients:
            ingredient = Ingredient(ingr_name=i['ingredient'].lower(),
                                    ingr_amount=i['amount'],
                                    ingr_unit=i['unit'],
                                    drink=drink.drink_id)
            db.session.add(ingredient)
        db.session.commit()

    def update_ingredients(self, drink, new_ingr):
        IngredientDbInter().delete_ingredient(drink.drink_id)
        IngredientDbInter().add_ingredients(new_ingr, drink)

    def delete_ingredient(self, drink_id):
        ingredients = IngredientDbInter().get_ingredients(drink_id)
        for i in ingredients:
            db.session.delete(i)
        db.session.commit()
