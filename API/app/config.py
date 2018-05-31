"""Configuration classes for the application"""
import os


class Configuration:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class Development(Configuration):
    """Development configuration class"""
    DEBUG = True


class Production(Development):
    """Production configuration class"""
    pass


class Testing(Development):
    """Testing configuration class"""
    TESTING = True


config = {
    "TESTING": Testing,
    "DEVELOPMENT": Development,
    "PRODUCTION": Production
}

default_config = config['DEVELOPMENT']
