from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_required , current_user
from app.models import Cart,Dog,Order ,db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id = current_user.id).all()
    total_price = sum(item.dog.price * item.quantity for item in cart_items)
    current_order = Order.query.filter_by(user_id=current_user.id, status='Pending').first()
    if not current_order and cart_items:
        current_order = Order(user_id=current_user.id, total_price=total_price, status='Pending')
        db.session.add(current_order)
        db.session.commit()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, current_order=current_order)



@user_bp.route('/cart/add/<int:dog_id>')
@login_required
def add_to_cart(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    cart_item = Cart.query.filter_by(user_id = current_user.id, dog_id= dog.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=current_user.id, dog_id = dog.id)
        db.session.add(new_cart_item)
    db.session.commit()
    flash('Item Add to your cart', 'success')
    return redirect(url_for('home.index'))