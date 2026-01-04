"""
Contact Routes Module
Handles contact form submissions and inquiry management:
- Contact Form Processing
- Email Notifications
- Rate Limiting
"""

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from flask import render_template, redirect, url_for, flash, current_app
from flask_mail import Message

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db, limiter, mail
from app.contact import contact
from app.contact.forms import ContactForm
from app.models.inquiry import Inquiry


# =========================================
# CONTACT FORM ROUTES
# =========================================

@contact.route("/contact", methods=['GET', 'POST'])
@limiter.limit("2 per minute")
def contact_form():
    """Handle contact form submissions with rate limiting"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Save inquiry to database
        inquiry = Inquiry(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(inquiry)
        db.session.commit()
        
        # Send email notification
        try:
            msg = Message(
                subject=f"New Inquiry: {form.subject.data}",
                sender=current_app.config.get('MAIL_USERNAME'),
                recipients=[current_app.config.get('SUPPORT_EMAIL') or current_app.config.get('CONTACT_EMAIL')],
                body=f"Name: {form.name.data}\nEmail: {form.email.data}\n\nMessage:\n{form.message.data}"
            )
            mail.send(msg)
        except Exception as e:
            # Log error but still show success as inquiry is saved in DB
            print(f"Error sending email: {e}")

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact.contact_form'))
        
    return render_template('contact/contact.html', title='Contact Us', form=form)