

import imp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import click
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate(db)



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    UPLOAD_FOLDER = 'static/images/'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
   
    from .views import views
    from .auth import auth
    from .cmd import cmd

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(cmd)

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    create_database(app)
    
    # @app.cli.add_command('initdb')
    # def reset_db():
    #     db.drop_all()
    #     db.create_all()
    #     print('initialised database')
    
  
        
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
def populate_database():
    print(" happy")
