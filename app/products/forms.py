from flask.ext.babel import Babel
from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, TextAreaField,
					IntegerField, SelectField, SelectMultipleField,
					DecimalField, RadioField, widgets)
from wtforms.validators import DataRequired, Length, Email
from .models import Product, Category
from ..suppliers.models import Supplier

class AddProduct(Form):
	name = StringField('Name', validators=[DataRequired()])
	reference = IntegerField('Reference', validators=[DataRequired()])
	unit = SelectField('Unit', validators=[DataRequired()])
	packing = IntegerField('Packing', validators=[DataRequired()])
	conditioning = IntegerField('Conditioning')
	conditioning_unit = SelectField('Unit')
	supplier_reference = StringField('Supplier Reference', validators=[DataRequired()])
	buying_price = DecimalField('Buying Price', validators=[DataRequired()])
	selling_price_no_tax = DecimalField('Price b/ VAT', validators=[DataRequired()])
	ean = IntegerField('EAN', validators=[DataRequired()])
	description = TextAreaField('Description')
	vat = SelectField('VAT', coerce=int, validators=[(DataRequired())])
	suppliers = SelectMultipleField('Suppliers',
									option_widget=widgets.CheckboxInput(),
									coerce=int,
									validators=[DataRequired()])
	categories = SelectField('Categories',
									coerce=int,
									validators=[DataRequired()])
	stock = DecimalField('Stock', validators=[DataRequired()])


class AddCategory(Form):
	name = StringField('Label', validators=[DataRequired()])
	code = IntegerField('Code', validators=[DataRequired()])