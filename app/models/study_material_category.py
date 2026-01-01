from app.extensions import db
from app.models.base import BaseModel

class StudyMaterialCategory(BaseModel):
    """Model for study material categories"""
    
    __tablename__ = 'study_material_categories'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f"StudyMaterialCategory('{self.name}')"
