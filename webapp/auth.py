from flask import Blueprint, render_template , request,flash,redirect,url_for
from webapp import views
from . import db
from webapp.models import User
from webapp.forms import SignUpFormUser
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
from flask_login import login_user, login_required, logout_user,current_user

@auth.route('/login',methods = ["GET", "POST"])
def login():
    # data = request.form
    # print(data)
    
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')

    #     user = User.query.filter_by(email=email).first()
    #     if user:
    #         if check_password_hash(user.password, password):
    #             flash('Logged in successfully!', category='success')
    #             login_user(user, remember=True)
    #             return redirect(url_for('views.home'))
    #         else:
    #             flash('Incorrect password, try again.', category='error')
    #     else:
    #         flash('Email does not exist.', category='error')

    return render_template("login.html", user = current_user)
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
            new_user = User(email=form.Email.data, frist_name= form.first_name.data, last_name=form.last_name.data,\
                mailing_address = form.mailing_address.data, mailing_phone_number=form.mailing_phone_number.data)
            new_user.set_password(form.password1.data)
            db.session.add(new_user)
            db.session.commit()
            flash ("Created succesfully", category='success')
            return redirect(url_for('auth.login'))
            
    return render_template("sign_up.html",user = current_user,form = form) 
