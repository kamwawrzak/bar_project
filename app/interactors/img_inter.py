import imghdr
import os
from datetime import datetime


from app import db
from app.models import Drink, User

from flask import abort, current_app


class ImgInter:

    def upload_img(self, img, db_obj):
        img_name = None
        if img.filename != '':
            ext = os.path.splitext(img.filename)[1]
            if ext not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            else:
                if isinstance(db_obj, Drink):
                    img_name = ImgInter().create_img_name(img, db_obj.drink_id)
                    img.save(os.path.join(current_app.config['DRINKS_PATH'],
                                          img_name))
                elif isinstance(db_obj, User):
                    img_name = ImgInter().create_img_name(img, db_obj.user_id)
                    img.save(os.path.join(current_app.config['USERS_PATH'],
                             img_name))
            return img_name

    def validate_format(self, stream):
        head = stream.read(512)
        stream.seek(0)
        img_format = imghdr.what(None, head)
        if not img_format:
            return None
        else:
            return '.' + (img_format if img_format != 'jpeg' else 'jpg')

    def create_img_name(self, img, model_id):
        img_format = ImgInter().validate_format(img.stream)
        t_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = str(model_id) + '_' + str(t_stamp) + img_format
        return img_name

    def get_img_path(self, db_obj):
        img_path = None
        if isinstance(db_obj, Drink):
            img_path = '/static/images/drinks/' + str(db_obj.image)
        elif isinstance(db_obj, User):
            img_path = '/static/images/users/' + str(db_obj.image)
        return img_path

    def get_all_img(self, db_obj):
        if isinstance(db_obj, Drink):
            return os.listdir(current_app.config['DRINKS_PATH'])
        elif isinstance(db_obj, User):
            return os.listdir(current_app.config['USERS_PATH'])

    def delete_img(self, db_obj):
        img = None
        if isinstance(db_obj, Drink) and db_obj.image != 'default.jpg':
            img = os.path.join(current_app.config['DRINKS_PATH'], db_obj.image)
        elif isinstance(db_obj, User) and db_obj.image != 'default.jpg':
            img = os.path.join(current_app.config['USERS_PATH'], db_obj.image)
        if img:
            os.remove(img)
            db_obj.image = 'default.jpg'
            db.session.commit()
        else:
            pass
