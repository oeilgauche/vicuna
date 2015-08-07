# Import flask dependencies
from flask import (Blueprint, request, render_template,
                  flash, g, session, redirect, url_for)
import os

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Configurations
from config import BASE_DIR

# Import JSON
import json

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
settings = Blueprint('settings', __name__, url_prefix='/backend/settings')

# Import the forms
from .forms import AddVAT, UpdateSettings

# Import the models
from .models import VAT, Settings
from ..suppliers.models import Supplier
from ..products.models import Product, Category

# Import helpers
from ..helpers.helpers import read_setting

# Import Babel
from app import babel
from config import LANGUAGES

# Set the route and accepted methods
@settings.route('/', methods=['GET', 'POST'])
def settings_list():
	
	# Settings area (read-only)

	config_units = read_setting("units")
	config_conditioning = read_setting("conditioning")
	config_currency = read_setting("currency")
	config_stores = read_setting("stores")
	config_repo = read_setting("repo")


	# VAT area
	add_vat = AddVAT(prefix="add_vat")

	if add_vat.validate_on_submit() and add_vat.vat_hidden.data:
		amount = int(add_vat.amount.data * 100)
		vat = VAT(name=add_vat.name.data,
					amount=amount)
		db.session.add(vat)
		db.session.commit()
		flash('VAT added!', 'success')

	# Build VAT section
	vat_items = VAT.query.order_by(VAT.amount)
	for vat_item in vat_items:
		vat_item.amount = float(vat_item.amount) / 100

	return render_template('settings/settings.html',
                            title='Settings',
                            config_units=config_units,
                            config_conditioning=config_conditioning,
                            config_currency=config_currency,
                            config_stores=config_stores,
                            config_repo=config_repo,
                            vat_items=vat_items,
                            add_vat=add_vat)

@settings.route('/vat/delete/<int:id>', methods=['GET', 'POST'])
def vat_delete(id):
	vat = VAT.query.get_or_404(id)
	db.session.delete(vat)
	db.session.commit()
	flash('VAT deleted!', 'success')
	return redirect(url_for('settings.settings_list'))