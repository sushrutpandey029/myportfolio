from app.extensions import db
from app.models.base import BaseModel

class BlogCategory(BaseModel):
    """Model for blog categories"""
    
    __tablename__ = 'blog_categories'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f"BlogCategory('{self.name}')"
