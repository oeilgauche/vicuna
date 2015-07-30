from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, TextAreaField, IntegerField, SelectField,
					SelectMultipleField, DecimalField, widgets)
from wtforms.validators import DataRequired, Length, Email
from .models import Product
from ..suppliers.models import Supplier

class AddProduct(Form):
	name = StringField('Name', validators=[DataRequired()])
	reference = IntegerField('Reference', validators=[DataRequired()])
	supplier_reference = StringField('Supplier Reference', validators=[DataRequired()])
	buying_price = DecimalField('Buying Price', validators=[DataRequired()])
	suppliers = SelectMultipleField('Suppliers',
									option_widget=widgets.CheckboxInput(),
									widget=widgets.ListWidget(prefix_label=False),
									coerce=int,
									validators=[DataRequired()])