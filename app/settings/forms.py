from flask.ext.babel import Babel
from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, TextAreaField, IntegerField, SelectField,
					SelectMultipleField, DecimalField, RadioField, widgets)
from wtforms.validators import DataRequired, Length, Email
from ..products.models import Product, Category
from ..suppliers.models import Supplier
from .models import VAT


class AddVAT(Form):
	name = StringField('Name', validators=[DataRequired()])
	amount = DecimalField('Amount', validators=[DataRequired()])