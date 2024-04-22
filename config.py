# import os
#
# BASE_DIR = os.path.dirname(__file__)
#
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'shop.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False
#
import os

class Config(object):


    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1111@localhost/shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 추가적인 설정이 필요할 경우 이곳에 추가

    SECRET_KEY = "dev"
