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
	ean = db.Column(db.Integer)
	description = db.Column(db.Text)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

	category = db.relationship('Category',
							backref=db.backref('products', order_by=id))

	def __repr__(self):
		return '<Product %r>' % self.name

class Category(db.Model):
	"""The Model for the Products' Categories"""
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
								onupdate=db.func.current_timestamp())
	name = db.Column(db.String(100)) 
	code = db.Column(db.Integer)