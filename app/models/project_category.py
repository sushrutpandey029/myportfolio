"""
Project Category Model Module
Manages project categorization
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel


# =========================================
# PROJECT CATEGORY MODEL
# =========================================

class ProjectCategory(BaseModel):
    """Model for project categories"""
    
    __tablename__ = 'project_categories'
    
    # Columns
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    
    # Relationships
    projects = db.relationship('Project', backref='project_category', lazy=True)
    
    def __repr__(self):
        return f"ProjectCategory('{self.name}')"
