import imghdr
import os
from datetime import datetime


from app import db


from flask import abort, current_app


class ImgInteractors:

    def upload_img(self, img, model_id, img_type):
        img_name = None
        if img.filename != '':
            ext = os.path.splitext(img.filename)[1]
            if ext not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            else:
                img_name = ImgInteractors().create_img_name(img, model_id)
                if img_type == 'drink':
                    img.save(os.path.join(current_app.config['DRINKS_PATH'],
                                          img_name))
                elif img_type == 'user':
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
        img_format = ImgInteractors().validate_format(img.stream)
        t_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = str(model_id) + '_' + str(t_stamp) + img_format
        return img_name

    def get_img_name(self, db_object, model_type):
        all_img = ImgInteractors().get_all_img(model_type)
        for img in all_img:
            if img == db_object.image:
                return img

    def get_img_path(self, db_object, model_type):
        img_path = None
        img_name = ImgInteractors().get_img_name(db_object, model_type)
        if model_type == 'drink':
            img_path = '/static/images/drinks/' + img_name
        elif model_type == 'user':
            img_path = '/static/images/users/' + img_name
        return img_path

    def get_all_img(self, model_type):
        if model_type == 'drink':
            return os.listdir(current_app.config['DRINKS_PATH'])
        elif model_type == 'user':
            return os.listdir(current_app.config['USERS_PATH'])

    def delete_img(self, db_obj, type_img):
        img = None
        if type_img == 'drink' and db_obj.image != 'default.jpg':
            img = os.path.join(current_app.config['DRINKS_PATH'], db_obj.image)
        elif type_img == 'user' and db_obj.image != 'default.jpg':
            img = os.path.join(current_app.config['USERS_PATH'], db_obj.image)
        if img:
            os.remove(img)
            db_obj.image = 'default.jpg'
            db.session.commit()
        else:
            pass
