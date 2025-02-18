import os
from flask import Blueprint, redirect, render_template, url_for, flash,current_app
from flask_login import login_required , current_user
from werkzeug.utils import secure_filename
from app.models import Cart,Dog,Order ,db
from app.forms import EditProfileForm, ChangePasswordForm

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


@user_bp.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.user_id != current_user.id:
        flash('Unauthorized action!','danger')
        return redirect(url_for('user.cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash("Item removed from your cart.", "success")
    return redirect(url_for('user.cart'))


@user_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.profile_image.data:
            file = form.profile_image.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/uploads', filename)

            file.save(file_path)

            current_user.profile_image = filename
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.edit_profile'))

    form.username.data = current_user.username
    form.email.data = current_user.email

    return render_template('edit_profile.html', form=form, user = current_user)



@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Incorrect current password.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('user.change_password'))

    return render_template('change_password.html', form=form)



@user_bp.route('/my-orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('my_orders.html', orders=orders)
