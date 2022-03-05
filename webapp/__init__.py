

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate(db)



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
   
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    create_database(app)
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        populate_database()
        print('Created Database!')
        
def populate_database():
    print(" happy")
    # username = 'user_name'
    # last_name = 'big bum'
    # email_add = '@gmail.com'
    # password = '123456789'
    # people = 20
    # for i in range(people):
    #     name = username + str(i)
    #     email =  name+ email_add
    #     mailing_address = name + " @ lagos state govt" 
        
    #     new_user = User(email=email, password=generate_password_hash(password, method='sha256'),\
    #                     frist_name = name , last_name =  last_name+ str(i),\
    #     mailing_address = mailing_address , mailing_phone_number= password + str(i))
            
    #     db.session.add( new_user)
    #     db.session.commit()
