import os


class Config:
    
    # Upload directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'store')

    # Database
    DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Server
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = '5000'
