import os


class Configuration:
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class Development(Configuration):
    DEBUG = True


class Production(Development):
    pass


class Testing(Development):
    TESTING = True


config = {
    "TESTING": Testing,
    "DEVELOPMENT": Development,
    "PRODUCTION": Production
}

default_config = config['DEVELOPMENT']
