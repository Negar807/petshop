from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Order, db

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/checkout/<int:order_id>')
@login_required
def checkout(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash("You do not have access!", "danger")
        return redirect(url_for('user.cart'))
    
    return render_template('checkout.html', order=order)
