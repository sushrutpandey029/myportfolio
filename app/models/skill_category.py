"""
Skill Category Model Module
Manages skill categorization
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel


# =========================================
# SKILL CATEGORY MODEL
# =========================================

class SkillCategory(BaseModel):
    """Model for skill categories"""
    
    __tablename__ = 'skill_categories'
    
    # Columns
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f"SkillCategory('{self.name}')"
