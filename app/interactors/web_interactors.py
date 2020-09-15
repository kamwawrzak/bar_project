import pickle

from flask import request

from flask_login import current_user


class WebInteractors():

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
        d = {request.form.get('ingredient1'): request.form.get('amount1'),
             request.form.get('ingredient2'): request.form.get('amount2'),
             request.form.get('ingredient3'): request.form.get('amount3'),
             request.form.get('ingredient4'): request.form.get('amount4'),
             request.form.get('ingredient5'): request.form.get('amount5'),
             request.form.get('ingredient6'): request.form.get('amount6')}
        return d
