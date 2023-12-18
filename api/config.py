"""Configuration classes for the application"""
import os

from dotenv import load_dotenv

load_dotenv()


class Configuration:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True
    PORT = os.getenv("PORT") or 5000
    DEFAULT_ADMIN_FIRST_NAME = os.getenv("DEFAULT_ADMIN_FIRST_NAME")
    DEFAULT_ADMIN_LAST_NAME = os.getenv("DEFAULT_ADMIN_LAST_NAME")
    DEFAULT_ADMIN_USER_NAME = os.getenv("DEFAULT_ADMIN_USER_NAME")
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD")
    DEFAULT_ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL")
    DEFAULT_ADMIN_PROFILE_PICTURE = os.getenv("DEFAULT_ADMIN_PROFILE_PICTURE")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")


class Development(Configuration):
    """Development configuration class"""
    DEBUG = True


class Production(Development):
    """Production configuration class"""
    pass


class Testing(Development):
    """Testing configuration class"""
    TESTING = True

    DATABASE_NAME = os.getenv("TEST_DATABASE_NAME")


environment = os.getenv("APP_ENVIRONMENT") or "DEVELOPMENT"

config = {
    "TESTING": Testing,
    "DEVELOPMENT": Development,
    "PRODUCTION": Production
}[environment]
