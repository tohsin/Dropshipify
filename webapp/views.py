from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for , session
from flask_login import  login_required, current_user
from webapp.forms import CreateProductFromAmazon, CreateProduct
from werkzeug.utils import secure_filename
from webapp.models import User, Product, Store, Order, OrderItem
import uuid as uuid
from . import db
import os
from flask import abort
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ["GET", "POST"])
@login_required
def home():
    # session['info'] = current_user
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
            f = manualform.upload.data
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
                           user = current_user)

@views.route('/view-products/<int:user_id>', methods = [ "GET"])
def view_products(user_id):
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    user = User.query.get_or_404(user_id)
    if user is None:
        abort(404)
    # items = Pending_orders.query.filter_by(user_id = user_id, done = False)
    return render_template("view_products.html", 
                           user = current_user)

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
    product_id = data['productid']
    
    '''first check if we have that order item there should be one unique to each product id per user
    1 first we access the user orders
    '''
    prod = Product.query.get_or_404(product_id)
    # a = db.session.query(User).outerjoin(Order, User.id== Order.id).group_by(#variavle in User.name)
    # Order.query.filter_by(store_id = prod.store_id).first()
    orders = current_user.orders
    found_store_for_order = False
    order_v = None
    for order in orders:
        if order.store_id == prod.store_id:
            #found a order id that matches the store id
            
            for order_item in order:
                #check if we have a product in that order from order item
                if order_item.product_id == product_id:
                #we found the product of that cart now we adding to it
                    order_item_.quantity+=1
                    break
            
       
  
            
    else:
        #we didnt find an order attached to user attached to store so we create
        print('store order didnt exist for user so creating new one')
        order1 = Order(user_id = current_user.id, store_id = prod.store_id, user=current_user)
        db.session.add(order1)
        db.session.commit()
        #now add the cart item too
        
    # order1 = Order(user_id=current_user.id, store_id=prod.store_id)
    # val = current_user.orders.order_item.query.filter_by(product_id = product_id).first()
    # print('checking if exists',val)
    # if not val:
    #     order1 = Order(user_id=current_user.id, store_id=prod.store_id)
        
    
    flash ("Item succesfully addded to Cart", category='success')
    return jsonify({})
@views.route('/add-fav', methods = [ "POST"])
@login_required
def addToFav():
    data = json.loads(request.data)
    product_id = data['productid']
    prod = Product.query.get_or_404(product_id)
    user = User.query.get_or_404(current_user.id)
    user.favoutite_products.append(prod)
    db.session.commit()
    return jsonify({})



# <button type='button' class='close' onclick='addToCart({{user.id, product.id}})'>
# </button>