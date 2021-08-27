import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = "sqlite://"
BCRYPT_LOG_ROUNDS = 4
WTF_CSRF_ENABLED = False
TESTING = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY')
UPLOADED_PATH = os.path.join(basedir, 'uploads')
XLSX_PATH = os.path.join(basedir, 'xlsx')
STATIC_PATH = os.path.join(basedir, 'static')
