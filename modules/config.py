import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://<DB_USERNAME>:<DB_PASSWORD>@/<DB_NAME>'
        '?unix_socket=/cloudsql/<INSTANCE_CONNECTION_NAME>'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
