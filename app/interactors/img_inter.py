import imghdr
import os

from app import db, s3
from app.interactors.date_time_inter import DatetimeInter
from app.models import Drink, User

from config import Config

from flask import abort


class ImgInter:

    def upload_img(self, img, db_obj):
        """Upload Image to S3 bucket

        Function image file and Drink or User object. It verify what kind of
        object has been passed, validate size and type of passed file and
        upload it to S3 bucket. In the end it return path to the image.

        Parameters
        ----------
        db_obj: Drink or User
        img: FileStorage

        Returns
        -------
        String
            Uploaded Image path.

        Raises
        ------
        400
            Raises if passed upload file is incorrect.
        """
        img_name = None
        if img.filename != '':
            ext = os.path.splitext(img.filename)[1]
            if ext not in Config.UPLOAD_EXTENSIONS:
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

    def validate_format(self, img):
        """File format validation.

        Function takes file and use imghdr module to read extension from file
        name. If extension is recognized it returns it as String. For .jpeg
        format it returns extension .jpg.

        Parameters
        ----------
        img: FileStorage

        Returns
        -------
        None
            If img_format has not been detected.
        String
            File extension: '.jpg'. or '.png'.
        """
        img.seek(0)
        img_format = imghdr.what(img, h=None)
        if not img_format:
            return None
        else:
            return '.' + (img_format if img_format != 'jpeg' else 'jpg')

    def validate_size(self, file):
        """File size validation.

        Function takes file and determines its size (maximum 130% of
        MAX_IMG_Size set in Config file. If file size is greater it raise
        413 'Too large file.' error.

        Parameters
        ----------
        file: FileStorage

        Returns
        -------
        None
            If file size meets requirements.

        Raises
        ------
        413
            If passed file size is too large.
        """
        file_len = len(file.read((int(1.3 * Config.MAX_IMG_SIZE))))
        if file_len > Config.MAX_IMG_SIZE:
            abort(413, 'Too large file.')
        else:
            pass

    def img_name(self, img, model_id):
        """Creating image name.

        Function accepts image file and id of Drink or User object from
        database and creates image name including the id, timestamp and file
        extension.

        Parameters
        ----------
        model_id: int
            user_id for User object or drink_id for Drink object
        img: FileStorage

        Returns
        -------
        String
            Name of image.
        """
        img_format = ImgInter().validate_format(img)
        t_stamp = DatetimeInter().create_timestamp()
        img_name = str(model_id) + '_' + str(t_stamp) + str(img_format)
        return img_name

    def get_img_name(self, db_obj):
        """Creating image name.

        Function accepts User or Drink object and basis on its image property
        extracts image filename from image path string.

        Parameters
        ----------
        db_obj: Drink or User

        Returns
        -------
        String
            Name of image.
        """
        return db_obj.image.split('/')[-1]

    def get_default_img(self, img_type):
        """Creating default image path.

        Function accepts string for expected image type and creates path for
        default image.

        Parameters
        ----------
        img_type: String
            It should be 'drink' for Drink object image path or 'user' for User
            object image path.

        Returns
        -------
        String
            Default Image path.
        """
        img_path = ''
        if img_type == 'drink':
            img_path = 'images/drinks/default.jpg'
        elif img_type == 'user':
            img_path = 'images/users/default.jpg'
        return Config.S3_LOCATION + img_path

    def delete_img(self, db_obj):
        """Delete image.

        Function accepts Drink or User objects and check what kind of object
        has been passed. Next it delete the object's image from S3 bucket.
        Also it substitute current object image path to default path.

        Parameters
        ----------
        db_obj: User or Drink
        """
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
