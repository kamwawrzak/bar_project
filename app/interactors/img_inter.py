import imghdr
import os
from datetime import datetime

from app import db, s3
from app.models import Drink, User

from config import Config

from flask import abort, current_app


class ImgInter:

    def upload_img(self, img, db_obj):
        img_name = None
        if img.filename != '':
            ext = os.path.splitext(img.filename)[1]
            if ext not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400, 'Incorrect file format.')
            else:
                ImgInter().validate_size(img)
                if isinstance(db_obj, Drink):
                    img_name = ImgInter().img_name(img, db_obj.drink_id)
                    img_name = 'images/drinks/' + img_name
                elif isinstance(db_obj, User):
                    img_name = ImgInter().img_name(img, db_obj.user_id)
                    img_name = 'images/users/' + img_name
                img_link = Config.S3_LOCATION + img_name
                s3.upload_fileobj(img, Config.S3_BUCKET_NAME, img_name,
                                  ExtraArgs={"ACL": "public-read"})
                return img_link

    def validate_format(self, stream):
        head = stream.read(512)
        stream.seek(0)
        img_format = imghdr.what(None, head)
        if not img_format:
            return None
        else:
            return '.' + (img_format if img_format != 'jpeg' else 'jpg')

    def validate_size(self, file):
        file_len = len(file.read((int(1.3 * Config.MAX_IMG_SIZE))))
        if file_len > Config.MAX_IMG_SIZE:
            abort(413, 'Too large file.')
        else:
            pass

    def img_name(self, img, model_id):
        img_format = ImgInter().validate_format(img.stream)
        t_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = str(model_id) + '_' + str(t_stamp) + str(img_format)
        return img_name

    def get_img_name(self, db_obj):
        img_name = db_obj.image.split('/')[-1]
        return img_name

    def get_default_img(self, img_type):
        img_path = ''
        if img_type == 'drink':
            img_path = 'images/drinks/default.jpg'
        elif img_type == 'user':
            img_path = 'images/users/default.jpg'
        return Config.S3_LOCATION + img_path

    def delete_img(self, db_obj):
        default_link = ''
        img_name = ImgInter().get_img_name(db_obj)
        if img_name != 'default.jpg':
            if isinstance(db_obj, Drink):
                default_link = ImgInter().get_default_img('drink')
                s3.delete_object(Bucket=Config.S3_BUCKET_NAME,
                                 Key='images/drinks/' + img_name)
            elif isinstance(db_obj, User):
                default_link = ImgInter().get_default_img('user')
                s3.delete_object(Bucket=Config.S3_BUCKET_NAME,
                                 Key='images/users/' + img_name)
            db_obj.image = default_link
            db.session.commit()
        else:
            pass
