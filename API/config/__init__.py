class Configuration:
    DEBUG = False
    TESTING = False


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
