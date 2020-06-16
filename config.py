class BaseConfig:

    DEBUG = True
    RESTPLUS_VALIDATE = True
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False


class ProdConfig(BaseConfig):

    DEBUG = False


class DevConfig(BaseConfig):

    pass
