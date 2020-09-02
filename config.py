import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///bar.db/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
