from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import  login_required,current_user
from webapp.forms import CreateProductFromAmazon, CreateProduct
from werkzeug.utils import secure_filename
from webapp.models import User, Product, Store, Cart
import uuid as uuid
from . import db
import os
from flask import abort
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ["GET", "POST"])
@login_required
def home():
    return render_template("home.html",user =current_user)

@views.route('/retailer', methods = ["GET", "POST"])
@login_required
def home_retailer():
    return render_template("add_product.html",user = current_user)

@views.route('/profile', methods = ["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html", user = current_user)

@views.route('/add-product/<int:id>', methods = ["GET", "POST"])
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
                return redirect(url_for('views.retailer_home'))
            except Exception as e:
                print(e)
                flash ("Error Looks like something broke", category='error')
    return render_template("add_product.html", 
                           user = current_user,
                           linkform = linkform,
                           manualform = manualform)


@views.route('/retailer-home', methods = ["GET"])
@login_required
def retailer_home():
    return render_template("retailer_home.html", user = current_user)
    
@views.route('/store-home/<int:store_id>', methods = ["GET"])
@login_required
def store_home(store_id):
    store = Store.query.get_or_404(store_id)
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    if store is None:
        abort(404)
    prod = store.products.order_by(Product.date_added.desc()).all()
    return render_template("store_home.html", 
                           user = current_user,
                           products = prod)
@views.route('/product-detail/<int:product_id>', methods = ["GET"])
@login_required
def product_detail(product_id):
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    product = Product.query.get_or_404(product_id)
    if product is None:
        abort(404)
    return render_template("product_detail.html", 
                           user = current_user,
                           product = product)
    
@views.route('/view-cart/<int:user_id>', methods = ["GET"])
@login_required
def view_cart(user_id):
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    user = User.query.get_or_404(user_id)
    if user is None:
        abort(404)
    items = Cart.query.filter_by(user_id = user_id, done = False)
    return render_template("view_cart.html", 
                           user = current_user,
                           items = items)

@views.route('/pending-orders/<int:user_id>', methods = [ "GET"])
def view_pending_orders(user_id):
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    user = User.query.get_or_404(user_id)
    if user is None:
        abort(404)
    # items = Pending_orders.query.filter_by(user_id = user_id, done = False)
    return render_template("pending_orders.html", 
                           user = current_user
                           )


@views.route('/order-history/<int:user_id>', methods = [ "GET"])
def view_order_history(user_id):
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    user = User.query.get_or_404(user_id)
    if user is None:
        abort(404)
    # items = Pending_orders.query.filter_by(user_id = user_id, done = False)
    return render_template("order_history.html", 
                           user = current_user,
                           )

@views.route('/view-products/<int:user_id>', methods = [ "GET"])
def view_products(user_id):
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    user = User.query.get_or_404(user_id)
    if user is None:
        abort(404)
    # items = Pending_orders.query.filter_by(user_id = user_id, done = False)
    return render_template("view_products.html", 
                           user = current_user,
                           )

# @main.route('/move-to-cart', methods = [ "POST"])
# @login_required
# def moveToCart():
#     data = json.loads(request.data)
#     items = data['items']
#     productid = data['productid']
#     cartItem = CartItem(product_id = productid, user_id= userid)
#     db.session.add(cartItem)
#     db.session.commit()
#     flash ("Item succesfully addded to Cart", category='success')
#     return jsonify({})


@views.route('/add-cart', methods = [ "POST"])
@login_required
def addToCart():
    data = json.loads(request.data)
    userid = data['userid']
    productid = data['productid']
    cartItem = Cart(product_id = productid, user_id= userid)
    db.session.add(cartItem)
    db.session.commit()
    flash ("Item succesfully addded to Cart", category='success')
    return jsonify({})


# <button type='button' class='close' onclick='addToCart({{user.id, product.id}})'>
# </button>