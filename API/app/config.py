"""Configuration classes for the application"""


class Configuration:
    """Base configuration class"""

    DEBUG = False
    TESTING = False

    DEFAULT_ADMIN_FIRST_NAME = "Moses"
    DEFAULT_ADMIN_LAST_NAME = "Gitau"
    DEFAULT_ADMIN_USER_NAME = "admin"
    DEFAULT_ADMIN_PASSWORD = "admin"
    DEFAULT_ADMIN_EMAIL = "gitaumoses4@gmail.com"
    DEFAULT_ADMIN_PROFILE_PICTURE = ""
    JWT_SECRET_KEY = "my_awesome_key"


class Development(Configuration):
    """Configuration class for the development"""
    DEBUG = True


class Production(Development):
    """Configuration class for production"""
    pass


class Testing(Development):
    """ Configuration class for testing"""

    TESTING = True


config = {
    "TESTING": Testing,
    "DEVELOPMENT": Development,
    "PRODUCTION": Production
}


default_config = config['DEVELOPMENT']
