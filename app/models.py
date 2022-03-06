from itertools import product
from time import timezone
from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import  check_password_hash
'''
many to many tables declared here
'''
favourite_shops = db.Table('favourite_shops',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('favourite_shop_id', db.Integer, db.ForeignKey('stores.id'))
)
favourite_niche = db.Table('favourite_niche',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('favourite_niche_id', db.Integer, db.ForeignKey('niche.id'))
)

store_niches = db.Table('store_niches',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id')),
    db.Column('niche_id', db.Integer, db.ForeignKey('niche.id'))
)
product_niches = db.Table('product_niches',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('niche_id', db.Integer, db.ForeignKey('niche.id'))
)
'''end of many tp many tables'''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150) )
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    is_retailer = db.Column(db.Boolean(),default= False)
    mailing_address = db.Column(db.String(150))
    city = db.Column(db.String(150) )
    state = db.Column(db.String(150) )
    zip_ = db.Column(db.String(150) )
    mailing_phone_number = db.Column(db.String(150))
    stores = db.relationship("Stores", uselist=False)
    favoutite_stores = db.relationship("Stores",secondary = favourite_shops)
    favoutite_niche = db.relationship("Niche",secondary = favourite_niche)
    def __repr__(self):
        return '<User {}>'.format(self.email)
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
class Stores(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    store_name = db.Column(db.String(150),unique = True)
    store_icon = db.Column(db.String(150),nullable=True)
    store_description = db.Column(db.String(150))
    niches = db.relationship("Niche", secondary = store_niches)
    products = db.relationship("Product")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    price = db.Column(db.Numeric)
    product_name  = db.Column(db.String(150))
    ansii = db.Column(db.String(150))
    product_link =  db.Column(db.String(500))
    number_available =  db.Column(db.Numeric)
    number_shipped =  db.Column(db.Numeric)
    number_clicks =  db.Column(db.Numeric)
    description = db.Column(db.String(300))
    product_image  = db.Column(db.String(150))
    date_added = db.Column(db.DateTime(timezone = True) ,default = datetime.now)
    date_editted = db.Column(db.DateTime(timezone = True) ,default = datetime.now)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    niche = db.relationship("Niche", secondary= product_niches)
    
class Niche(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(150))

