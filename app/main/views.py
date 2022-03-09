from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import  login_required,current_user
from .forms import CreateProductFromAmazon, CreateProduct
from werkzeug.utils import secure_filename
from app.models import User,Product
import uuid as uuid
from .. import db
from . import main
import os
import json

# views = Blueprint('views', __name__)

@main.route('/', methods = ["GET", "POST"])
@login_required
def home():
    return render_template("home.html",user =current_user)

@main.route('/retailer', methods = ["GET", "POST"])
@login_required
def home_retailer():
    return render_template("add_product.html",user =current_user)

@main.route('/profile', methods = ["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html", user = current_user)

@main.route('/add-product/<int:id>', methods = ["GET", "POST"])
@login_required
def add_product(id):
    linkform = CreateProductFromAmazon()
    manualform = CreateProduct()
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    if manualform.validate_on_submit():
            #add user to database
            user_to_get_store = User.query.get_or_404(id)
            f= manualform.upload.data
            pic_filename = secure_filename(f.filename)
            #set pic name
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            new_product = Product(product_name = manualform.product_name.data, 
                                  price = manualform.price.data,
                                  ansii = manualform.ansii.data, 
                                  product_link = manualform.product_link.data,
                                  number_available = manualform.number_available.data,
                                  description = manualform.product_description.data,
                                  number_shipped = manualform.number_available.data,
                                  product_image = pic_name,
                                  store_id = user_to_get_store.store.id
                                  )
            db.session.add(new_product)
            
            try:
                f.save(os.path.join('webapp/static/products', pic_name))
                db.session.commit()
                flash ("Product Created succesfully", category='success')
                return redirect(url_for('views.store_home'))
            except Exception as e:
                print(e)
                flash ("Error Looks like something broke", category='error')
    return render_template("add_product.html", 
                           user = current_user,
                           linkform = linkform,
                           manualform = manualform)

@main.route('/store', methods = ["GET", "POST"])
@login_required
def store_home():
    linkform = CreateProductFromAmazon()
    return render_template("store_home.html", 
                           user = current_user,
                           linkform = linkform)
