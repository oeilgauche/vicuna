# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
suppliers = Blueprint('suppliers', __name__, url_prefix='/backend/suppliers')

# Import the forms
from .forms import AddSupplier

# Import the models
from .models import Supplier

# Set the route and accepted methods
@suppliers.route('/')
def suppliers_list():
    suppliers = Supplier.query.order_by(Supplier.name)
    return render_template('suppliers/list.html',
                            title='Suppliers',
                            suppliers=suppliers)


@suppliers.route('/add', methods=['GET', 'POST'])
def suppliers_add():
    form = AddSupplier()
    if form.validate_on_submit():
        supplier = Supplier(name=form.name.data, address=form.address.data, zip_code=form.zip_code.data,
                            city=form.city.data, country=form.country.data, phone=form.phone.data,
                            email=form.email.data)
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added!', 'success')
        return redirect(url_for('suppliers.suppliers_list'))
    return render_template('suppliers/add.html', form=form)


@suppliers.route('/edit/<int:id>', methods=['GET', 'POST'])
def suppliers_edit(id):
    supplier = Supplier.query.get_or_404(id)
    form = AddSupplier()
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.address = form.address.data
        supplier.zip_code = form.zip_code.data
        supplier.city = form.city.data
        supplier.country = form.country.data
        supplier.phone = form.phone.data
        supplier.email = form.email.data
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier modified!', 'success')
        return redirect(url_for('suppliers.suppliers_list'))
    form.name.data = supplier.name
    form.address.data = supplier.address
    form.zip_code.data = supplier.zip_code
    form.city.data = supplier.city
    form.country.data = supplier.country
    form.phone.data = supplier.phone
    form.email.data = supplier.email

    return render_template('suppliers/edit.html', action="edit", form=form)


@suppliers.route('/delete/<int:id>', methods=['GET', 'POST'])
def suppliers_delete(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Supplier ' + supplier.name + ' deleted!', 'success')
    return redirect(url_for('suppliers.suppliers_list'))

@suppliers.route('/view/<int:id>')
def suppliers_view(id):
    supplier = Supplier.query.get_or_404(id)
    return render_template('suppliers/view.html', title='Supplier',
                            supplier=supplier)