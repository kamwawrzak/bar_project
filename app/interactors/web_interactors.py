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
        d = {}
        flag = True
        i = 0
        while flag:
            d_key = request.form.get('ingredient{}'.format(i))
            if d_key is None:
                break
            else:
                d_value = request.form.get('amount{}'.format(i))
                d[d_key] = d_value
                i = i+1
        return d
