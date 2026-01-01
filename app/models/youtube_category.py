from app.extensions import db
from app.models.base import BaseModel

class YouTubeCategory(BaseModel):
    """Model for YouTube Video Categories"""
    __tablename__ = 'youtube_categories'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f"YouTubeCategory('{self.name}')"
