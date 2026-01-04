"""
YouTube Category Model Module
Manages YouTube video categorization
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel


# =========================================
# YOUTUBE CATEGORY MODEL
# =========================================

class YouTubeCategory(BaseModel):
    """Model for YouTube video categories"""
    
    __tablename__ = 'youtube_categories'
    
    # Columns
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f"YouTubeCategory('{self.name}')"
