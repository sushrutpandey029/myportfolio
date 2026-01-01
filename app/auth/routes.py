from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app.extensions import db, limiter
from app.auth import auth
from app.auth.forms import LoginForm
from app.models.user import User



# Public login removed - Admin login only
# Users can only be created by admin from admin panel

@auth.route("/admin/login", methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.admin_dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Check if user is admin
            if user.role != 'admin':
                flash('Access Denied: You are not an administrator.', 'danger')
                return redirect(url_for('auth.admin_login'))
                
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_bp.admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/admin_login.html', title='Admin Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('pages.home'))