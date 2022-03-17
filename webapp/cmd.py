from flask import Blueprint, render_template , request,flash,redirect,url_for
from webapp import views
from . import db
import os
import webapp
from webapp.models import User, Store
from webapp.forms import SignUpFormUser,LoginFormUser, SignUpFormRetailer
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
from flask_login import login_user, login_required, logout_user,current_user
import click
cmd = Blueprint('cmd', __name__)

@cmd.cli.command("create_db")
def create_user():
        db.drop_all()
        db.create_all()
        print('***** Datebase created ****')
        db.session.add(
            User(email='lilynw@gmail.com', password=generate_password_hash('elysium8', method='sha256'),first_name= 'Lily', last_name='nwobodo',\
                mailing_address = 'abuja under the left side of love', city= 'abuja',\
                    state = 'Abuja', zip_ = '23424',mailing_phone_number="+23495896056"))
        db.session.add(
            User(email='oluwatosinoseni@gmail.com', password=generate_password_hash('elysium8', method='sha256'),first_name= 'Tosin', last_name='oseni',\
                mailing_address = '2 kazzem ajayo close ogudu association', city= 'Lagos',\
                    state = 'Lagos', zip_ = '100242',mailing_phone_number="+2349026287884"))
        db.session.commit()