from app import db


class Product(db.Model):
	"""The Model for products"""
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
								onupdate=db.func.current_timestamp())
	name = db.Column(db.String(100))
	reference = db.Column(db.Integer)
	supplier_reference = db.Column(db.String(50))
	buying_price = db.Column(db.Integer)
	selling_price_no_tax = db.Column(db.Integer)
	selling_price = db.Column(db.Integer)
	ean = db.Column(db.Integer)
	description = db.Column(db.Text)

	vat_id = db.Column(db.Integer, db.ForeignKey('VAT.id'))
	vat = db.relationship('VAT',
							backref=db.backref('products'))

	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category',
							backref=db.backref('products', order_by=id))

	stock = db.Column(db.Integer)

	def __repr__(self):
		return '<Product %r>' % self.name


class StockHistory(db.Model):
	"""The Model for stock history"""
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
								onupdate=db.func.current_timestamp())
	amount = db.Column(db.Integer)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
	product = db.relationship('Product',
								backref=db.backref('stock_history',
													order_by=date_created))


class Category(db.Model):
	"""The Model for the Products' Categories"""
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
								onupdate=db.func.current_timestamp())
	name = db.Column(db.String(100)) 
	code = db.Column(db.Integer)