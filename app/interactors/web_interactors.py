import pickle
from datetime import datetime, timedelta

from flask import request

from flask_login import current_user


class WebInteractors:

    def get_form_data(*args):
        d = {}
        for arg in args:
            d[arg] = request.form.get(arg)
        return d

    def get_drink_data(self):
        d = WebInteractors().get_form_data('name', 'category', 'technique',
                                           'description', 'preparation')
        d['author'] = current_user.get_id()
        d['ingredients'] = pickle.dumps(WebInteractors().get_ingredients())
        d['add_date'] = WebInteractors().get_date()
        return d

    def get_comment_data(self, drink_id):
        d = {'content': request.form.get('content'),
             'author': current_user.get_id(),
             'author_nick': current_user.nick,
             'drink': drink_id,
             'date': WebInteractors().get_date()}
        return d

    def get_user_data(self):
        d = WebInteractors().get_form_data('email', 'nick', 'password',
                                           'confirm_pass')
        d['register_date'] = WebInteractors().get_date()
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

    def get_date(self):
        ms = timedelta(microseconds=datetime.now().microsecond)
        dt = datetime.now() - ms
        return dt
