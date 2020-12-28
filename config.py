import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bar.db/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FB_ID = os.environ.get('FB_ID')
    FB_SECRET = os.environ.get('FB_SECRET')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    S3_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
    S3_ACCESS_SECRET_KEY = os.environ.get('S3_ACCESS_SECRET_KEY')
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)
    PER_PAGE = 10
