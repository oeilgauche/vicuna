from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from .models import Supplier

class AddSupplier(Form):
	name = StringField('Name', validators=[DataRequired()])
	address = StringField('address', validators=[DataRequired()])
	zip_code = IntegerField('Zip Code', validators=[DataRequired()])
	city = StringField('city', validators=[DataRequired()])
	country = StringField('country', validators=[DataRequired()])
	phone = StringField('phone', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(),Email()])