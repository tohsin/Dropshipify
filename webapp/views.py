from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import  login_required,current_user
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ["GET", "POST"])
@login_required
def home():
    return render_template("home.html",user =current_user)

@views.route('/retailer', methods = ["GET", "POST"])
@login_required
def home_retailer():
    return render_template("add_product.html",user =current_user)

@views.route('/profile', methods = ["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html",user =current_user)

@views.route('/sign-up-retailer', methods = ["GET", "POST"])
@login_required
def sign_up_retailer():
    return render_template("sign_up_retailer.html",user =current_user)
