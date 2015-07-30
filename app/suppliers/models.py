from app import db

suppliers_products = db.Table('suppliers_products',
	db.Column('supplier_id', db.Integer, db.ForeignKey('supplier.id')),
	db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
	)

class Supplier(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	name = db.Column(db.String(100))
	address = db.Column(db.String(50))
	zip_code = db.Column(db.Integer)
	city = db.Column(db.String(50))
	country = db.Column(db.String(50))
	phone = db.Column(db.String(50))
	email = db.Column(db.String(50))
	products = db.relationship('Product',
								secondary=suppliers_products,
								backref=db.backref('supplier', lazy='dynamic'),
								lazy='dynamic')

	def __repr__(self):
		return '<Supplier %r>' % self.name