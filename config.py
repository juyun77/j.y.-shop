

##sqlite
# import os
#
# BASE_DIR = os.path.dirname(__file__)
#
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'shop.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False
#

##mysql
import os

class Config(object):


    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1111@192.168.0.80/shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 추가적인 설정이 필요할 경우 이곳에 추가

    SECRET_KEY = "dev"

##aws rds
# import os
#
# class Config(object):
#
#
#     # 데이터베이스 설정
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:It12345!@database-1.cluster-ro-cmg5rcfhykpl.ap-northeast-2.rds.amazonaws.com/shop'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     SECRET_KEY = "dev"