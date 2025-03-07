import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Order, Dog, User
from app import db
from app.controllers.api_server import get_random_dog
from app.forms import EditProfileForm

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



@admin_bp.route('/make-admin/<int:user_id>', methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('home.index'))

    user = User.query.get_or_404(user_id)

    if user.is_admin:
        flash(f"{user.username} is already an admin!", "info")
    else:
        user.is_admin = True
        db.session.commit()
        flash(f"{user.username} is now an admin!", "success")

    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/manage-users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('You do not have access!', 'danger')
        return redirect(url_for('home.index'))

    users = User.query.all()
    return render_template('manage_users.html', users=users)


@admin_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def admin_edit_profile():
    if not current_user.is_admin:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('home.index'))
    
    form = EditProfileForm(obj=current_user)

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
        flash("Profile updated successfully!", "success")
        return redirect(url_for('admin.admin_edit_profile'))

    return render_template('edit_profile.html', form=form, user=current_user)