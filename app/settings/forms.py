from flask.ext.babel import Babel
from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, TextAreaField, IntegerField, SelectField,
					SelectMultipleField, DecimalField, RadioField, HiddenField, widgets)
from wtforms.validators import DataRequired, Length, Email
from ..products.models import Product, Category
from ..suppliers.models import Supplier
from .models import VAT, Settings


class AddVAT(Form):
	name = StringField('Name', validators=[DataRequired()])
	amount = DecimalField('Amount', validators=[DataRequired()])
	vat_hidden = HiddenField('VAT', default="vat")


class UpdateSettings(Form):
	currency = SelectField('Currency', 
							choices=[('euro', 'Euros'), ('gbp', 'GBP')],
							validators=[DataRequired()])
	file_repo = SelectField('File Repository',
							choices=[('local', 'Local'), ('s3', 'Amazon S3')], 
							validators=[DataRequired()])
	nb_of_stores = IntegerField('Number of Stores', validators=[DataRequired()])
	settings_hidden = HiddenField('Settings', default="settings")