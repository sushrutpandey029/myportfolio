"""
Service Model Module
Manages freelancing services offered on the platform
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel


# =========================================
# SERVICE MODEL
# =========================================

class Service(BaseModel):
    """Model for freelancing services"""
    
    __tablename__ = 'services'
    
    # Columns
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    user = db.relationship('User', backref='services', lazy=True)
    category = db.relationship('ServiceCategory', viewonly=True)
    
    def __repr__(self):
        return f"Service('{self.title}')"