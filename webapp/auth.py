from flask import Blueprint, render_template , request,flash,redirect,url_for
from webapp import views
from . import db
from webapp import webapp
from webapp.models import User,Stores
from webapp.forms import SignUpFormUser,LoginFormUser
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
from flask_login import login_user, login_required, logout_user,current_user

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

@webapp.app_errorhandler(404)
def page_not_found(e):
    print("work")
    return render_template("404.html"), 404


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
        
        
        
          


#    <a class="nav-item nav-link" id="home" href="/">Home</a>  
#           <a class="nav-item nav-link" id="logout" href="/logout">Logout</a>
#           {% else %}

#             <a class="nav-item nav-link" id="login" href="/login">Login</a>
#             <a class="nav-item nav-link" id="signUp" href="/sign-up">Sign Up</a>