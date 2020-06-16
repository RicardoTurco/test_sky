import sys
from firebase_admin import credentials, firestore, initialize_app


class BaseConfig:

    DEBUG = True
    RESTPLUS_VALIDATE = True
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False
    JWT_SECRET_KEY = 'secret_key_82012796-4da6-4958-8a38-2701d71692ae'

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
