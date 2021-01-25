from app import db
from app.db_interactors.comment_db_inter import CommentDbInter
from app.db_interactors.ingredient_db_inter import IngredientDbInter
from app.db_interactors.vote_db_inter import VoteDbInter
from app.interactors.img_inter import ImgInter
from app.interactors.web_inter import WebInter
from app.models import Drink

from config import Config

from flask_login import current_user

from sqlalchemy import func


class DrinkDbInter:

    def get_drink(self, drink_id):
        """Drink getter.

        Function returns single Drink object.

        Parameters
        ----------
        drink_id: int

        Returns
        -------
        Drink
            Single Drink object.
        """
        return Drink.query.filter_by(drink_id=drink_id).first()

    def get_all_drinks(self, page):
        """All Drinks getter.

        Function returns Pagination object of all Drink objects from database
        divided to pages. Maximum number of objects per page is set by PER_PAGE
        value. Drinks are sorted in alphabetical order.

        Parameters
        ----------
        page: int

        Returns
        -------
        Pagination
            Pagination object including all Drinks objects.
        """
        return Drink.query.order_by(Drink.name).paginate(
                                            page=int(page),
                                            per_page=Config().PER_PAGE)

    def user_all_drinks(self, user_id):
        """User Drinks getter.

        Function returns single Drink object.

        Parameters
        ----------
        user_id: int

        Returns
        -------
        []
            List of all Drink objects assigned to the User.
        """
        return Drink.query.filter_by(author=user_id).all()

    def add_drink(self, drink, img=None):
        """Add new Drink object.

        Function adds new Drink object to database and upload Image to S3
        bucket. Also it adds Drink's ingredients to Ingredient table and
        increments added drinks number of currently logged in user.

        Parameters
        ----------
        drink: Drink
        img: FileStorage
        """
        db.session.add(drink)
        current_user.drinks_number += 1
        db.session.commit()
        IngredientDbInter().add_ingredients(WebInter().get_ingredients(),
                                            drink)
        if img:
            img_name = ImgInter().upload_img(img, drink)
            drink.image = img_name
            db.session.commit()

    def update_drink(self, drink, name, category, technique, description,
                     preparation, img=None):
        """Drink update.

        Function updates Drink data in database. If image is passed to the
        function it also deletes old image from S3 bucket and uploads the new
        image.

        Parameters
        ----------
        drink: Drink
        name: string
        category: string
        technique: string
        description: string
        preparation: string
        img: FileStorage
        """
        drink.name = name
        drink.category = category
        drink.technique = technique
        drink.description = description
        drink.preparation = preparation
        if img:
            img_name = ImgInter().upload_img(img, drink)
            if drink.image != ImgInter().get_default_img('drink'):
                ImgInter().delete_img(drink)
            drink.image = img_name
        db.session.commit()

    def delete_drink(self, drink_id):
        """Delete Drink.

        Function delete single Drink object as well as Vote, Comment and
        Ingredient objects assigned to the Drink. Also if the Drink image was
        different than default.jpg the function delete it from S3 bucket.
        The added drinks number of currently logged in user is decremented.

        Parameters
        ----------
        drink_id: int
        """
        drink = DrinkDbInter().get_drink(drink_id)
        if drink.image != ImgInter().get_default_img('drink'):
            ImgInter().delete_img(drink)
        IngredientDbInter().delete_ingredients(drink_id)
        VoteDbInter().delete_drink_votes(drink_id)
        CommentDbInter().delete_many_comments(drink_id=drink_id)
        db.session.delete(drink)
        current_user.drinks_number -= 1
        db.session.commit()

    def views_counter(self, drink):
        """Drink views counter.

        When the function is called out it increments view property of Drink
        object in database.

        Parameters
        ----------
        drink: Drink
        """
        drink.views += 1
        db.session.commit()

    def get_most_viewed(self):
        """Most viewed Drink getter.

        Function finds maximum views value in Drink table. Next it creates list
        of Drink objects meeting this condition. If there are more than 1 this
        kind of objects the list is sorted by avg_rate property of the Drinks
        in decreasing order. In the creates dictionary of drink_id, name and
        image of first position on the list.

        Returns
        ----------
        {}
            Dictionary including id, name and image of Drink object.
        """
        max_views = db.session.query(func.max(Drink.views))
        drinks = Drink.query.filter_by(views=max_views).all()
        if len(drinks) > 1:
            drinks.sort(key=lambda x: x.avg_rate, reverse=True)
        d = {'id': drinks[0].drink_id,
             'image': drinks[0].image,
             'name': drinks[0].name}
        return d

    def get_top_rated(self):
        """Top rated Drink getter.

        Function finds maximum abg_rate value in Drink table. Next it creates
        list of Drink objects meeting this condition. If there are more than 1
        this kind of objects the list is sorted by views property of the Drinks
        in decreasing order. In the creates dictionary of drink_id, name and
        image of first position on the list.

        Returns
        ----------
        {}
            Dictionary including id, name and image of Drink object.
        """
        max_rate = db.session.query(func.max(Drink.avg_rate))
        drinks = Drink.query.filter_by(avg_rate=max_rate).all()
        if len(drinks) > 1:
            drinks.sort(key=lambda x: x.views, reverse=True)
        d = {'id': drinks[0].drink_id,
             'image': drinks[0].image,
             'name': drinks[0].name}
        return d
