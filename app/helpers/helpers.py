import os

# Configurations
from config import BASE_DIR

# Import JSON
import json

# Import the models
from ..settings.models import VAT

def to_int(num):
	"""Convert decimal to integer for storage in DB"""
	return int(num * 100)

def to_dec(num):
	"""Convert to decimal after being retrieved from DB"""
	return float(num) / 100

def to_dec_string(num):
	"""Convert to decimal after being retrieved from DB"""
	return "%.2f" % (float(num) / 100)

def add_vat(price, vat):
	"""Add VAT to selling price before taxes"""
	vat_amount = VAT.query.get_or_404(vat)
	vat_coeff = (float(vat_amount.amount) / 10000) + 1
	return price * vat_coeff

def calc_margin(buying_price, selling_price):
	"""Compute gross margin for products"""
	selling_price = float(selling_price)
	buying_price = float(buying_price)
	margin = ((selling_price - buying_price) / buying_price) * 100
	return "%.2f" % margin

def read_setting(setting):
	with open(os.path.join(BASE_DIR, 'app/settings/config.json')) as json_data_file:
		config_data = json.load(json_data_file)
	return config_data[setting]