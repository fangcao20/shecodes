import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_not_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:Phiphi05@localhost:3306/place_together'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
