from flask import Blueprint, render_template , request,flash,redirect,url_for
from app import views
from . import db
import os
import app
from app.models import User,Stores
from app.forms import SignUpFormUser,LoginFormUser, SignUpFormRetailer
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
from flask_login import login_user, login_required, logout_user,current_user

auth = Blueprint('auth', __name__)
@auth.route('/login',methods = ["GET", "POST"])
def login():
    form = LoginFormUser()
    if current_user.is_authenticated:
            return redirect(url_for('views.home'))
    if form.validate_on_submit():
            #add user to database
            user = User.query.filter_by(email=form.Email.data).first()
            if user:
                if check_password_hash(user.password, form.Password.data):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
    return render_template("login.html", user = current_user,form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',methods = ["GET", "POST"])
def signup():
    #data_p ={'username':"miguel"}
    form = SignUpFormUser()
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if form.validate_on_submit():
            #add user to database
            email = User.query.filter_by(email=form.email.data).first()
            if email:
                flash('Email already exists.', category='error')
            new_user = User(email=form.email.data, password=generate_password_hash(form.password1.data, method='sha256'),first_name= form.first_name.data, last_name=form.last_name.data,\
                mailing_address = form.mailing_address.data, city= form.city.data,\
                    state = form.state.data, zip_ = form.zip_.data,mailing_phone_number=form.mailing_phone_number.data)
            
            db.session.add(new_user)
            db.session.commit()
            flash ("Created succesfully", category='success')
            return redirect(url_for('auth.login'))
            
    return render_template("sign_up.html",user = current_user,form = form) 

@auth.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@auth.app_errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@auth.route('/update/<int:id>',methods = ["GET", "POST"])
def update(id):
    form = SignUpFormUser()
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.email = request.form['email']
        name_to_update.last_name = request.form['last_name']
        name_to_update.first_name = request.form['first_name']
        name_to_update.mailing_address = request.form['mailing_address']
        name_to_update.city = request.form['city']
        name_to_update.state = request.form['state']
        name_to_update.zip_ = request.form['zip_']
        name_to_update.mailing_phone_number = request.form['mailing_phone_number']
        try:
            db.session.commit()
            flash ("User Updated", category='success')
            return render_template("update_user.html",user = current_user,
                                   form = form,name_to_update=name_to_update) 
        except:
            flash ("Error Looks like something broke", category='error')
            return render_template("update_user.html",
                                   user = current_user,
                                   form = form,
                                   name_to_update=name_to_update) 
    else:
        return render_template("update_user.html",
                                   user = current_user,
                                   form = form,
                                   name_to_update=name_to_update) 
        
@auth.route('/sign-up-retailer/<int:id>', methods = ["GET", "POST"])
@login_required
def sign_up_retailer(id):
    form = SignUpFormRetailer()
    if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
    if form.validate_on_submit():
            #add user to database
            user_to_get_store = User.query.get_or_404(id)
            f= form.upload.data
            pic_filename = secure_filename(f.filename)
            #set pic name
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            new_store = Stores(store_name = form.store_name.data, store_icon = pic_name,\
               store_description = form.store_description.data,user_id = user_to_get_store.id )
            db.session.add(new_store)
            user_to_get_store.is_retailer = True
            try:
                f.save(os.path.join('webapp/static/images', pic_name))
                db.session.commit()
                flash ("Registered Retailer succesfully", category='success')
                return redirect(url_for('views.profile'))
            except Exception as e:
                print(e)
                flash ("Error Looks like something broke", category='error')
                return render_template("sign_up_retailer.html",
                                   user = current_user,
                                   form = form) 
    else:
        if current_user.is_retailer:
            store = Stores.query.filter_by(user_id = id)
            return render_template("sign_up_retailer.html", user = current_user, form = form )
        else:
            return render_template("sign_up_retailer.html", user = current_user, form = form)



