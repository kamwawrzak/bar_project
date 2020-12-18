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

    def update_ingredients(self, old_ingr, new_ingr):
        i = 0
        for ingr in old_ingr:
            ingr.ingr_name = new_ingr[i]['ingredient']
            ingr.ingr_amount = new_ingr[i]['amount']
            ingr.ingr_unit = new_ingr[i]['unit']
            i += 1
        db.session.commit()

    def delete_ingredient(self, drink_id):
        ingredients = IngredientDbInter().get_ingredients(drink_id)
        for i in ingredients:
            db.session.delete(i)
        db.session.commit()
