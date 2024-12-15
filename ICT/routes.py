from flask import render_template, url_for, flash, redirect, request
from ICT import app, db
from ICT.models import User, Item
from ICT.forms import RegistrationForm, LoginForm, ItemForm
from flask_login import login_user, current_user, logout_user, login_required

# Home Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Register Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('That username is already taken. Please choose a different one.', 'danger')
            return render_template('signup.html', form=form)
        
        # Create a new user and store in the database
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Check password as plain text
            login_user(user, remember=True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check username and password.', 'danger')
    
    return render_template('login.html', form=form)

# Logout Route
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Admin Route - Restricted to Admin User   
# (Username - admin, Password - Joker) 
# To access the admin page first you need to login with the admin credentials then type in -
# " http://127.0.0.1:5000/admin " to access the admin page.
@app.route('/admin')
@login_required
def admin():
    if current_user.username != 'admin':
        flash('You must be an admin to view this page.', 'danger')
        return redirect(url_for('home'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)

# Edit User Route (Admin Only)
@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.username != 'admin':
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Update the username
        user.username = new_username

        # Check if password fields are filled and match
        if new_password:
            if new_password != confirm_password:
                flash('Passwords do not match. Please try again.', 'danger')
                return render_template('edit_user.html', user=user)
            user.password = new_password  # Save the new password (stored as plain text here)

        db.session.commit()
        flash('User details have been updated!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('edit_user.html', user=user)

# Delete User Route (Admin Only)
@app.route('/admin/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.username != 'admin':
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted!', 'success')
    return redirect(url_for('admin'))

# Coming Soon Route
@app.route('/coming_soon', methods=['POST'])
def coming_soon():
    flash('Coming Soon!', 'info')
    return redirect(url_for('home'))

# Item Routes 
@app.route('/items', methods=['GET', 'POST'])
@login_required
def items():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data)
        db.session.add(item)
        db.session.commit()
        flash('Item has been added!', 'success')
        return redirect(url_for('items'))
    
    items = Item.query.all()
    return render_template('items.html', items=items, form=form)

# Edit Item Route
@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        db.session.commit()
        flash('Item has been updated!', 'success')
        return redirect(url_for('items'))
    
    return render_template('edit_item.html', form=form, item=item)

# Delete Item Route
@app.route('/item/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Item {item.name} has been deleted!', 'success')
    return redirect(url_for('items'))
