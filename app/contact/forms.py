"""
Contact Forms Module
Contains form classes for contact/inquiry operations:
- Contact Form
"""

# =========================================
# IMPORTS
# =========================================
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


# =========================================
# CONTACT FORM
# =========================================

class ContactForm(FlaskForm):
    """Form for user contact/inquiry submissions"""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')