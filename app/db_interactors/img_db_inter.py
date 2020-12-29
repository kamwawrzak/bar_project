from app import db


class ImgDbInter:

    def update_db_image(self, db_model, img_link):
        db_model.image = img_link
        db.session.commit()
