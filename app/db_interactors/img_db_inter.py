from app import db


class ImgDbInter:

    def update_db_image(self, db_model, img_name):
        db_model.image = img_name
        db.session.commit()
