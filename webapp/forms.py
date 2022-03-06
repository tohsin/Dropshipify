from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired,Length,ValidationError, EqualTo
from webapp.models import User
from wtforms.widgets import TextArea
class LoginFormUser(FlaskForm):
    Email = StringField('Email', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignUpFormUser(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(min=4)])
    password1 = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    password2 = PasswordField('Password (Confirm)', validators=[DataRequired(),Length(min=8), EqualTo('password1')])
    first_name = StringField('First Name', validators=[DataRequired(),Length(min=4)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(min=4)])
    mailing_address =  StringField('Mailing Address', validators=[DataRequired(),Length(min=4)])
    city =  StringField('City', validators=[DataRequired()])
    state =  StringField('State', validators=[DataRequired()])
    zip_ =  StringField('ZIP', validators=[DataRequired()])
    mailing_phone_number =  StringField('Mailing Phone Number', validators=[DataRequired(),Length(min=4)])
    submit = SubmitField('Submit')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
class SignUpFormRetailer(FlaskForm):
    store_name = StringField('Name of Store', validators=[DataRequired(),Length(min=4)])
    store_icon = FileField(validators=[FileRequired()])
    store_description = TextAreaField("Store Description" ,validators=[DataRequired(),Length(min=20)])
    submit = SubmitField('Become a Retailer')
    