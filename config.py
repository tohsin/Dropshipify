import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, "database.db")
config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,

    'default': DevelopmentConfig
}

  


