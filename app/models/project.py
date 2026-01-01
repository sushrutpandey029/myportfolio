from app.extensions import db
from app.models.base import BaseModel
from app.utils.constants import PROJECT_FREE, PROJECT_DEMO

class Project(BaseModel):
    """Model for projects"""
    
    __tablename__ = 'projects'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('project_categories.id'), nullable=True)
    file_path = db.Column(db.String(200), nullable=True)  # Path to the project file
    google_drive_link = db.Column(db.String(500), nullable=True)  # Google Drive link for external hosting
    github_link = db.Column(db.String(500), nullable=True)  # GitHub repository link
    image_url = db.Column(db.String(200), nullable=True)  # Path to project image
    project_type = db.Column(db.String(20), nullable=False, default=PROJECT_FREE)  # free or demo
    is_active = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)
    
    # Legacy field for backward compatibility
    @property
    def category(self):
        return self.project_category.name if self.project_category else None
    
    def __repr__(self):
        return f"Project('{self.title}', '{self.project_type}')"