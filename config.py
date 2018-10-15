import os

class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your-jwt-signing-key'
    ADMIN_SECRET = os.getenv('ADMIN_SECRET') or 'your-admin-key'
    DB_SECRET = os.getenv('DB_SECRET') or 'database-manager-key'

class Development(Config):
    DEBUG = True
    DEVELOPMENT = True  

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False