from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Order, Dog
from app import db
from app.controllers.api_server import get_random_dog

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')




@admin_bp.route('/orders')
@login_required
def manage_orders():
    if not current_user.is_admin:
        flash('You do not have access!', 'danger')
        return redirect(url_for('home.index'))
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)



@admin_bp.route('/orders/update/<int:order_id>', methods = ['POST'])
@login_required
def update_orders(order_id):
    if not current_user.is_admin:
        flash('You do not have access!', 'danger')
        return redirect(url_for('home.index'))
    order = Order.query.get_or_404(order_id)
    new_satus = request.form.get('status')
    order.status = new_satus
    db.session.commit()
    flash(f'The order status of {order.id} has changed!', 'success')
    return redirect(url_for('admin.manage_orders'))



@admin_bp.route('/add-dog', methods =['POST'])
@login_required
def add_dog():
    if not current_user.is_admin:
        flash('You do not have access!', 'danger')
        return redirect(url_for('home.index'))
    dog_data = get_random_dog()
    if dog_data:
        new_dog = Dog(breed= dog_data["breed"], image_url= dog_data["image_url"], price = 100.0 )
        db.session.add(new_dog)
        db.session.commit()
        flash("New dog added from API!", "success")
    else:
        flash("Failed to fetch dog data.", "danger")
    return redirect(url_for('admin.manage_orders'))