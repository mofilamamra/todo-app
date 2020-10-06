import os

class Config:
    """ basic configurations. """
    DEBUG = False
    PORT = os.environ.get('PORT') or 5000
    ENV = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"

class development(Config):
    """ development configurations """
    DEBUG = True

class production(Config):
    """ production configurations """

    PORT = os.environ.get('PORT') or 8080
