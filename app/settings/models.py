from app import db

class VAT(db.Model):
	"""Define VAT Model"""
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
								onupdate=db.func.current_timestamp())
	name = db.Column(db.String(25))
	amount = db.Column(db.Integer)
