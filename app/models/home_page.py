"""
Home Page Models Module
Manages home page content, skills, and team members
"""

# =========================================
# STANDARD LIBRARY IMPORTS
# =========================================
from datetime import datetime

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app import db


# =========================================
# HOME PAGE CONTENT MODEL
# =========================================

class HomePageContent(db.Model):
    """Model for home page content management"""
    
    __tablename__ = 'home_page_content'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Hero Section
    hero_title_line1 = db.Column(db.String(200), nullable=False, default="Building Digital Solutions")
    hero_title_line2 = db.Column(db.String(200), nullable=False, default="That Scale")
    hero_subtitle = db.Column(db.Text, nullable=False, default="Full-stack developer specializing in creating modern, scalable applications")
    cv_button_text = db.Column(db.String(100), default="Download CV")
    cv_button_link = db.Column(db.String(500))
    hire_button_text = db.Column(db.String(100), default="Hire Me")
    profile_image = db.Column(db.String(500), default="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=400&auto=format&fit=crop")
    
    # Stats Section
    stat1_value = db.Column(db.String(20), default="150+")
    stat1_label = db.Column(db.String(100), default="Active Projects")
    stat2_value = db.Column(db.String(20), default="500+")
    stat2_label = db.Column(db.String(100), default="Study Materials")
    stat3_value = db.Column(db.String(20), default="50+")
    stat3_label = db.Column(db.String(100), default="Team Members")
    stat4_value = db.Column(db.String(20), default="1.2k")
    stat4_label = db.Column(db.String(100), default="Monthly Downloads")
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<HomePageContent {self.id}>'


# =========================================
# SKILL MODEL
# =========================================

class Skill(db.Model):
    """Model for user skills and proficiency levels"""
    
    __tablename__ = 'skills'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    percentage = db.Column(db.Integer, nullable=False, default=50)
    icon_text = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(50), default="blue")
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Skill {self.name}>'


# =========================================
# TEAM MEMBER MODEL
# =========================================

class TeamMember(db.Model):
    """Model for team members and their information"""
    
    __tablename__ = 'team_members'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(500), nullable=False)
    linkedin_url = db.Column(db.String(500))
    twitter_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    dribbble_url = db.Column(db.String(500))
    behance_url = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TeamMember {self.name}>'
