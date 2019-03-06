import os

from dotenv import load_dotenv

# Load secrets into environment.
load_dotenv()

class BaseConfig:
  DB_USER = 'admin'
  DB_PASSWORD = os.environ['DB_PASSWORD']
  DB_HOST = 'localhost'
  DB_PORT = '5432'
  SALT_SIZE = 32
  SECRET_KEY = os.environ['SECRET_KEY']

class DevelopmentConfig(BaseConfig):
  FLASK_STATIC_DIR = 'src/static'
  FLASK_TEMPLATES_DIR = 'src/templates'
  DB_NAME = 'dev'

class ProductionConfig(BaseConfig):
  FLASK_STATIC_DIR = 'dist'
  FLASK_TEMPLATES_DIR = 'dist'
  DB_NAME = 'prod'
