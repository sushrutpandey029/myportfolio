"""
Inquiry Model Module
Manages contact form submissions and inquiries
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel
from app.utils.constants import INQUIRY_NEW


# =========================================
# INQUIRY MODEL
# =========================================

class Inquiry(BaseModel):
    """Model for contact form inquiries"""
    
    __tablename__ = 'inquiries'
    
    # Columns
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=INQUIRY_NEW)
    
    def __repr__(self):
        return f"Inquiry('{self.name}', '{self.subject}', '{self.status}')"