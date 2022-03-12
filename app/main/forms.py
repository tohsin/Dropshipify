from flask_wtf import FlaskForm
from sqlalchemy import Numeric
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, IntegerField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms.validators import DataRequired,Length,ValidationError, EqualTo
from app.models import User
from wtforms.widgets import TextArea


class CreateProductFromAmazon(FlaskForm):
    amazon_link = StringField('Amazon Link', validators=[DataRequired(),Length(min=4)])
    submit = SubmitField('Automatically Add By Amazon Link')
    
class CreateProduct(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(),Length(min=2)])
    price = IntegerField('Price', validators=[DataRequired()])
    ansii = StringField('Ansii Number' )
    product_link = StringField('Link If Any' )
    number_available = IntegerField('Number Available', validators=[DataRequired()])
    product_description = TextAreaField("Product Description" ,validators=[DataRequired(),Length(min=20)])
    upload = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'png','jpeg'], 'Images only!')])
    submit = SubmitField('Become a Retailer')
