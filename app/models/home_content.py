from app.extensions import db
from app.models.base import BaseModel

class HomeContent(BaseModel):
    """Model for managing home page content"""
    
    __tablename__ = 'home_content'
    
    # Hero Section
    hero_title_line1 = db.Column(db.String(100), nullable=False, default="Collaborate, Manage,")
    hero_title_line2 = db.Column(db.String(100), nullable=False, default="Grow Together.")
    hero_subtitle = db.Column(db.Text, nullable=False, default="Your centralized platform for project management, study materials, and team knowledge sharing.")
    
    # Profile Card
    profile_image = db.Column(db.String(300), nullable=True)
    profile_name = db.Column(db.String(100), nullable=False, default="Michael Chen")
    profile_title = db.Column(db.String(100), nullable=False, default="Lead Developer & Team Manager")
    profile_rating = db.Column(db.String(10), nullable=False, default="5.0")
    
    # Profile Skills (comma separated)
    profile_skills = db.Column(db.String(500), nullable=False, default="Python,React,Node.js,UI/UX")
    
    # Stats
    stat_projects = db.Column(db.String(20), nullable=False, default="150+")
    stat_materials = db.Column(db.String(20), nullable=False, default="500+")
    stat_team = db.Column(db.String(20), nullable=False, default="50+")
    stat_downloads = db.Column(db.String(20), nullable=False, default="1.2k")
    
    # Knowledge Hub Section
    knowledge_hub_title = db.Column(db.String(100), nullable=False, default="Premium Digital Ecosystem.")
    knowledge_hub_subtitle = db.Column(db.Text, nullable=False, default="Unlock elite documentation, strategic training, and global insights designed for peak performance and exponential growth.")
    
    # Workflow Section
    workflow_title = db.Column(db.String(100), nullable=False, default="Master Your Workflow")
    workflow_subtitle = db.Column(db.Text, nullable=False, default="Experience a streamlined journey from registration to project completion with our integrated team tools designed for maximum efficiency.")
    
    # CTA Buttons
    cv_button_text = db.Column(db.String(50), nullable=False, default="Download CV")
    cv_button_link = db.Column(db.String(300), nullable=True)
    hire_button_text = db.Column(db.String(50), nullable=False, default="Hire Me")
    
    # Only one row should exist
    singleton_guard = db.Column(db.Integer, unique=True, default=1)
    
    def __repr__(self):
        return f"HomeContent('{self.hero_title_line1}')"
    
    @staticmethod
    def get_content():
        """Get the home page content, create if doesn't exist"""
        content = HomeContent.query.first()
        if not content:
            content = HomeContent()
            db.session.add(content)
            db.session.commit()
        return content
