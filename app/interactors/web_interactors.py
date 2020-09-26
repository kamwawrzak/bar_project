import pickle

from flask import request

from flask_login import current_user


class WebInteractors:

    def get_form_data(*args):
        d = {}
        for arg in args:
            d[arg] = request.form.get(arg)
        return d

    def get_drink_data(self):
        d = {'name': request.form.get('name').capitalize(),
             'author': current_user.get_id(),
             'category': request.form.get('category'),
             'technique': request.form.get('technique').capitalize(),
             'description': request.form.get('description'),
             'preparation': request.form.get('preparation'),
             'ingredients': pickle.dumps(WebInteractors().get_ingredients())}
        return d

    def get_ingredients(self):
        ingredients = []
        flag = True
        i = 0
        while flag:
            form_ingr_name = 'ingredient{}'.format(i)
            form_amount_name = 'amount{}'.format(i)
            ingredient = request.form.get(form_ingr_name)
            amount = request.form.get(form_amount_name)
            if ingredient is None:
                break
            else:
                d = {'i_form_name': form_ingr_name,
                     'a_form_name': form_amount_name,
                     'ingredient': ingredient,
                     'amount': amount}
                ingredients.append(d)
                i = i+1
        return ingredients
