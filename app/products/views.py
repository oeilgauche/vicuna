# Import flask dependencies
from flask import (Blueprint, request, render_template,
                  flash, g, session, redirect, url_for)

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
products = Blueprint('products', __name__, url_prefix='/backend/products')

# Import the forms
from .forms import AddProduct

# Import the models
from .models import Product
from ..suppliers.models import Supplier

# Import Babel
from app import babel
from config import LANGUAGES

# Set the route and accepted methods
@products.route('/')
def products_list():
    products = Product.query.order_by(Product.reference)
    return render_template('products/list.html',
                            title='Products',
                            products=products)


@products.route('/add', methods=['GET', 'POST'])
def product_add():
	form = AddProduct()
	suppliers = [(s.id, s.name) for s in Supplier.query.order_by(Supplier.name)]
	form.suppliers.choices = suppliers
	if form.validate_on_submit():
		# Storing the buying price as an integer
		buying_price_int = int(form.buying_price.data * 100)

		product = Product(name=form.name.data, reference=form.reference.data,
							supplier_reference=form.supplier_reference.data,
							ean=form.ean.data, description=form.description.data,
							buying_price=buying_price_int)
		db.session.add(product)
		db.session.commit()

		for s in form.suppliers.data:
			supp = Supplier.query.filter_by(id=s).first()
			supp.products.append(product)
			db.session.add(supp)
			db.session.commit()
		
		flash('Product %s added!' % form.name.data, 'success')
		return redirect(url_for('products.products_list'))
	return render_template('products/add.html',
							title='Add a Product',
							form=form)


@products.route('/edit/<int:id>', methods=['GET', 'POST'])
def product_edit(id):
	# Initialize form
	product = Product.query.get_or_404(id)
	form = AddProduct()
	# Create list of suppliers
	form.suppliers.choices = [(s.id, s.name) for s in Supplier.query.order_by(Supplier.name)]
	
	if form.validate_on_submit():
		product.name = form.name.data
		product.reference = form.reference.data
		product.supplier_reference = form.supplier_reference.data
		product.ean = form.ean.data
		product.description = form.description.data
		product.buying_price = form.buying_price.data * 100
		product.supplier = []
		db.session.add(product)
		db.session.commit()
		for s in form.suppliers.data:
			supp = Supplier.query.filter_by(id=s).first()
			supp.products.append(product)
			db.session.add(supp)
			db.session.commit()
		flash('Product %s (Reference %s) modified!' % (product.name, product.reference), 'success')
		return redirect(url_for('products.products_list'))

	#Populate the fields
	form.suppliers.data = [s.id for s in product.supplier]
	form.name.data = product.name
	form.reference.data = product.reference
	form.supplier_reference.data = product.supplier_reference
	form.ean.data = product.ean
	form.description.data = product.description
	form.buying_price.data = product.buying_price / 100
	
	return render_template('products/edit.html',
							title='Edit product',
							action="edit",
							form=form)


@products.route('/delete/<int:id>', methods=['GET', 'POST'])
def product_delete(id):
	product = Product.query.get_or_404(id)
	db.session.delete(product)
	db.session.commit()
	flash('Product ' + product.name + ' deleted!', 'success')
	return redirect(url_for('products.products_list'))


@products.route('/view/<int:id>', methods=['GET', 'POST'])
def product_view(id):
	product = Product.query.get_or_404(id)
	return render_template('products/view.html', title='Products',
							product=product)