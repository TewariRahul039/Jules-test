# This file will contain Flask configuration settings.
# For example, DEBUG, SECRET_KEY, DATABASE_URI, etc.

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = '9316a873130ea8cf86d1152919ebe1ecac72bd49af59bfae' # Generated random key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = 'HS256'
    # Add other configuration variables here

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    # Production specific config
    pass
