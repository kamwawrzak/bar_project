import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    DRINKS_PATH = os.environ.get('DRINKS_PATH')
    USERS_PATH = os.environ.get('USERS_PATH')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bar.db/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FB_ID = os.environ.get('FB_ID')
    FB_SECRET = os.environ.get('FB_SECRET')
