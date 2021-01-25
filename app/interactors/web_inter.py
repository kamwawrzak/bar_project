from app.interactors.date_time_inter import DatetimeInter

from flask import request

from flask_login import current_user


class WebInter:

    def get_form_data(*args):
        """Get data from HTML form.

        Function returns data introduced in HTML form by user.

        Parameters
        ----------
        args: String
            String representing input 'name' property in HTML form.

        Returns
        -------
        {}
            Dictionary of keys and values of HTML form data.

        Example
        -------
        For login template for getting login and password data:
            WebInter().get_form_data('login', 'password')
        """
        d = {}
        for arg in args:
            d[arg] = request.form.get(arg)
        return d

    def get_drink_data(self):
        """Get new drink data from HTML form.

        Function creates dictionary of drink data introduced by user. Next it
        adds keys and value for: author (current logged in User user_id),
        author_nick (current logged in User nick and current date.

        Returns
        -------
        {}
            Dictionary including data of new drink added by user.
        """
        d = WebInter().get_form_data('name', 'category', 'technique',
                                     'description', 'preparation')
        d['author'] = current_user.get_id()
        d['author_nick'] = current_user.nick
        d['add_date'] = DatetimeInter().get_date()
        return d

    def get_comment_data(self, drink_id):
        """Get new comment data.

        Function gets new comment body from HTML form, adds date, assigned
        drink and comment author data and returns it in dictionary.

        Parameters
        ----------
        drink_id: int

        Returns
        -------
        {}
            Dictionary including data of new comment added by user.
        """
        d = {'content': request.form.get('content'),
             'author': current_user.get_id(),
             'author_nick': current_user.nick,
             'drink': drink_id,
             'date': DatetimeInter().get_dt_hmin()}
        return d

    def get_user_data(self):
        """Get new user data.

        Function creates dictionary of new user data. Next it adds current date
        as registration date.

        Returns
        -------
        {}
            Dictionary including data of new user.
        """
        d = WebInter().get_form_data('email', 'nick', 'password',
                                     'confirm_pass')
        d['register_date'] = DatetimeInter().get_date()
        return d

    def get_ingredients(self):
        """Get new ingredients data.

        Function creates list of ingredients and appends dictionaries including
        data of every ingredient.

        Returns
        -------
        []
            List of dictionaries including ingredients data: ingredient name,
            ingredient amount and ingredient unit.
        """
        ingredients = []
        flag = True
        i = 0
        while flag:
            ingredient = request.form.get('ingredient{}'.format(i))
            amount = request.form.get('amount{}'.format(i))
            unit = request.form.get('unit{}'.format(i))
            if ingredient == '' or ingredient is None:
                break
            else:
                d = {'ingredient': ingredient,
                     'amount': amount,
                     'unit': unit}
                ingredients.append(d)
                i = i+1
        return ingredients
