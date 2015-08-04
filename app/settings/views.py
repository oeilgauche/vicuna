# Import flask dependencies
from flask import (Blueprint, request, render_template,
                  flash, g, session, redirect, url_for)

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

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

# Import Babel
from app import babel
from config import LANGUAGES

# Set the route and accepted methods
@settings.route('/', methods=['GET', 'POST'])
def settings_list():
	
	# Settings area
	settings_items = Settings.query.first()
	settings = UpdateSettings(prefix="settings")

	if settings.validate_on_submit() and settings.settings_hidden.data:
		update_settings = Settings(currency=settings.currency.data,
									file_repo=settings.file_repo.data,
									nb_of_stores=settings.nb_of_stores.data)
		db.session.add(update_settings)
		db.session.commit()
		flash('Settings updated!', 'success')

	
	settings.currency.data = settings_items.currency
	settings.file_repo.data = settings_items.file_repo
	settings.nb_of_stores.data = settings_items.nb_of_stores

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
                            title='Products',
                            settings=settings,
                            vat_items=vat_items,
                            add_vat=add_vat)

@settings.route('/vat/delete/<int:id>', methods=['GET', 'POST'])
def vat_delete(id):
	vat = VAT.query.get_or_404(id)
	db.session.delete(vat)
	db.session.commit()
	flash('VAT deleted!', 'success')
	return redirect(url_for('settings.settings_list'))