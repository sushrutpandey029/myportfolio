"""
Project Model Module
Manages downloadable projects and demos
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel
from app.utils.constants import PROJECT_FREE, PROJECT_DEMO


# =========================================
# PROJECT MODEL
# =========================================

class Project(BaseModel):
    """Model for projects"""
    
    __tablename__ = 'projects'
    
    # Columns
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('project_categories.id'), nullable=True)
    file_path = db.Column(db.String(200), nullable=True)
    google_drive_link = db.Column(db.String(500), nullable=True)
    github_link = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    project_type = db.Column(db.String(20), nullable=False, default=PROJECT_FREE)
    is_active = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)
    
    # Properties
    @property
    def category(self):
        """Legacy property for backward compatibility"""
        return self.project_category.name if self.project_category else None
    
    def __repr__(self):
        return f"Project('{self.title}', '{self.project_type}')"