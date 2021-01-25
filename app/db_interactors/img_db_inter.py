from app import db


class ImgDbInter:

    def update_db_image(self, db_model, img_link):
        """Update image links in database.

        Function accepts Drink or User objects and assign new img_link to the
        current image property of the objects.

        Parameter
        ---------
        db_model: Drink or User
        img_link: string
        """
        db_model.image = img_link
        db.session.commit()
