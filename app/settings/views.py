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
from .forms import AddVAT

# Import the models
from .models import VAT
from ..suppliers.models import Supplier
from ..products.models import Product, Category

# Import Babel
from app import babel
from config import LANGUAGES

# Set the route and accepted methods
@settings.route('/', methods=['GET', 'POST'])
def settings_list():
	
	add_vat = AddVAT()

	if add_vat.validate_on_submit():
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
                            vat_items=vat_items,
                            add_vat=add_vat)

@settings.route('/vat/delete/<int:id>', methods=['GET', 'POST'])
def vat_delete(id):
	vat = VAT.query.get_or_404(id)
	db.session.delete(vat)
	db.session.commit()
	flash('VAT deleted!', 'success')
	return redirect(url_for('settings.settings_list'))