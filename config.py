import os
import boto3
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get("DEVELOPMENT_SECRET_KEY")
    OAUTHLIB_INSECURE_TRANSPORT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOPMENT_DATABASE_URL")

db = SQLAlchemy()
seeder = FlaskSeeder()