import sys
from firebase_admin import credentials, firestore, initialize_app


class BaseConfig:

    DEBUG = True
    RESTPLUS_VALIDATE = True
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False

    try:
        SKY_KEY = credentials.Certificate('keys.json')
        SKY_APP = initialize_app(SKY_KEY)
        SKY_DB = firestore.client()
    except Exception as e:
        print(e)
        sys.exit()


class ProdConfig(BaseConfig):

    DEBUG = False


class DevConfig(BaseConfig):

    pass
