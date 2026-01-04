"""
Service Category Model Module
Manages service categorization
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel


# =========================================
# SERVICE CATEGORY MODEL
# =========================================

class ServiceCategory(BaseModel):
    """Model for service categories"""
    
    __tablename__ = 'service_categories'
    
    # Columns
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    
    # Relationships
    services = db.relationship('Service', backref='category_rel', lazy=True)
    
    def __repr__(self):
        return f"ServiceCategory('{self.name}')"
