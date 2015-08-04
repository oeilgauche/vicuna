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
from .forms import AddProduct, AddCategory

# Import the models
from .models import Product, Category, StockHistory
from ..suppliers.models import Supplier

# Import helpers
from ..helpers.helpers import to_int, to_dec

# Import Babel
from app import babel
from config import LANGUAGES

# Set the route and accepted methods
@products.route('/')
def products_list():
    products = Product.query.order_by(Product.reference)
    for product in products:
    	product.stock = to_dec(product.stock)
    return render_template('products/list.html',
                            title='Products',
                            products=products)


@products.route('/add', methods=['GET', 'POST'])
def product_add():
	form = AddProduct()
	suppliers = [(s.id, s.name) for s in Supplier.query.order_by(Supplier.name)]
	categories = [(c.id, c.name) for c in Category.query.order_by(Category.code)]
	form.suppliers.choices = suppliers
	form.categories.choices = categories
	if form.validate_on_submit():
		# Storing the buying price as an integer
		buying_price_int = to_int(form.buying_price.data)
		stock_int = to_int(form.stock.data)

		product = Product(name=form.name.data, reference=form.reference.data,
							supplier_reference=form.supplier_reference.data,
							ean=form.ean.data, description=form.description.data,
							buying_price=buying_price_int, stock=stock_int)
		db.session.add(product)
		db.session.commit()

		# Add stock to History
		stock_history = StockHistory(amount=stock_int, product=product)
		db.session.add(stock_history)
		db.session.commit()

		for s in form.suppliers.data:
			supp = Supplier.query.filter_by(id=s).first()
			supp.products.append(product)
			db.session.add(supp)
			db.session.commit()
		
		for c in form.categories.data:
			cat = Category.query.filter_by(id=c).first()
			cat.products.append(product)
			db.session.add(cat)
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
	form.categories.choices = [(c.id, c.name) for c in Category.query.order_by(Category.code)]
	
	if form.validate_on_submit():
		product.name = form.name.data
		product.reference = form.reference.data
		product.supplier_reference = form.supplier_reference.data
		product.ean = form.ean.data
		product.description = form.description.data
		product.buying_price = to_int(form.buying_price.data)
		product.stock = to_int(form.stock.data)
		product.supplier = []
		#product.category = []
		db.session.add(product)
		db.session.commit()

		stock_history = StockHistory(amount=to_int(form.stock.data), product=product)
		db.session.add(stock_history)
		db.session.commit()

		for s in form.suppliers.data:
			supp = Supplier.query.filter_by(id=s).first()
			supp.products.append(product)
			db.session.add(supp)
			db.session.commit()

		for c in form.categories.data:
			cat = Category.query.filter_by(id=c).first()
			cat.products.append(product)
			db.session.add(cat)
			db.session.commit()

		flash('Product %s (Reference %s) modified!' % (product.name, product.reference), 'success')
		return redirect(url_for('products.products_list'))

	#Populate the fields
	form.suppliers.data = [s.id for s in product.supplier]
	form.categories.data = [0, product.category.id]
	cat = product.category.id
	form.name.data = product.name
	form.reference.data = product.reference
	form.supplier_reference.data = product.supplier_reference
	form.ean.data = product.ean
	form.description.data = product.description
	form.buying_price.data = to_dec(product.buying_price)
	form.stock.data = to_dec(product.stock)
	
	return render_template('products/edit.html',
							title='Edit product',
							action="edit",
							form=form,
							cat=cat)


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
	product.buying_price = to_dec(product.buying_price)
	product.stock = to_dec(product.stock)
	return render_template('products/view.html', title='Product',
							product=product)


@products.route('/categories', methods=['GET', 'POST'])
def categories():
	form = AddCategory()
	categories = Category.query.order_by(Category.code)
	if form.validate_on_submit():
		category = Category(name=form.name.data, code=form.code.data)
		db.session.add(category)
		db.session.commit()
		flash('Category %s added!' % form.name.data, 'success')
		return redirect(url_for('products.categories'))
	return render_template('products/categories.html',
							title='Categories',
							categories=categories,
							form=form)


@products.route('/categories/delete/<int:id>', methods=['GET', 'POST'])
def category_delete(id):
	category = Category.query.get_or_404(id)
	db.session.delete(category)
	db.session.commit()
	flash('Category %s deleted!' % category.name, 'success')
	return redirect(url_for('products.categories'))