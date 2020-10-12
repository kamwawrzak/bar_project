import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    DRINKS_PATH = 'C:/Users/Wawrzu/bar_project/app/static/images/drinks'
    USERS_PATH = 'C:/Users/Wawrzu/bar_project/app/static/images/users'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bar.db/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
