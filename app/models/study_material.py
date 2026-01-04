"""
Study Material Model Module
Manages educational resources and downloadable materials
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel
from app.utils.constants import MATERIAL_FREE, MATERIAL_PAID


# =========================================
# STUDY MATERIAL MODEL
# =========================================

class StudyMaterial(BaseModel):
    """Model for study materials (PDFs, documents, etc.)"""
    
    __tablename__ = 'study_materials'
    
    # Columns
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=True)  # None for free materials
    file_path = db.Column(db.String(200), nullable=True)  # Path to the PDF file (optional if doc_url is provided)
    doc_url = db.Column(db.String(500), nullable=True)  # External document URL (Google Docs, etc.)
    thumbnail = db.Column(db.String(200), nullable=True)  # Path to thumbnail image
    material_type = db.Column(db.String(20), nullable=False, default=MATERIAL_FREE)  # free or paid
    is_active = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"StudyMaterial('{self.title}', '{self.material_type}')"