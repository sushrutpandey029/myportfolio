"""
Authentication Forms Module
Contains form classes for authentication operations:
- Admin Login Form
Note: Registration forms removed - users created via admin panel only
"""

# =========================================
# IMPORTS
# =========================================
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# Models
from app.models.user import User


# =========================================
# ADMIN LOGIN FORM
# =========================================

class LoginForm(FlaskForm):
    """Form for admin login authentication"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')