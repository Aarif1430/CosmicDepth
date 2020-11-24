import os
from boto.s3.connection import S3Connection



class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245' #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' #os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = S3Connection(os.environ['EMAIL'])
    MAIL_PASSWORD = S3Connection(os.environ['PWD'])#os.environ.get('EMAIL_PASS')
