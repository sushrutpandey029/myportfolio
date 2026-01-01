from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    """Decorator to restrict access to admin users only"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.admin_login'))
        if not current_user.is_admin():
            flash('You do not have permission to access the admin area.', 'danger')
            return redirect(url_for('pages.home'))
        return f(*args, **kwargs)
    return decorated_function

def login_required_ajax(f):
    """Decorator for AJAX endpoints that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return {'error': 'Authentication required'}, 401
        return f(*args, **kwargs)
    return decorated_function