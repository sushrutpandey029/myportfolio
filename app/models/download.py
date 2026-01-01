from app.extensions import db
from app.models.base import BaseModel

class Download(BaseModel):
    """Model to track user downloads of projects and study materials"""
    
    __tablename__ = 'downloads'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'project' or 'study_material'
    item_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f"Download('{self.user_id}', '{self.item_type}', '{self.filename}')"