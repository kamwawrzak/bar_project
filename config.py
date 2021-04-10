import os
from os.path import dirname, join

from dotenv import load_dotenv


env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_IMG_SIZE = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FB_ID = os.environ.get('FB_ID')
    FB_SECRET = os.environ.get('FB_SECRET')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    S3_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
    S3_ACCESS_SECRET_KEY = os.environ.get('S3_ACCESS_SECRET_KEY')
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)
    PER_PAGE = 10
