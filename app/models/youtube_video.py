"""
YouTube Video Model Module
Manages YouTube video entries and educational content
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel


# =========================================
# YOUTUBE VIDEO MODEL
# =========================================

class YouTubeVideo(BaseModel):
    """Model for YouTube video entries"""
    
    __tablename__ = 'youtube_videos'
    
    # Columns
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_id = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"YouTubeVideo('{self.title}', '{self.video_id}')"