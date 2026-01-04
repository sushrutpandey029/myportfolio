"""
About Content Model Module
Manages editable about page content
"""

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.models.base import BaseModel


# =========================================
# ABOUT CONTENT MODEL
# =========================================

class AboutContent(BaseModel):
    """Model for managing about page content"""
    
    __tablename__ = 'about_content'
    
    # Hero Section
    hero_title = db.Column(db.String(200), nullable=False, default="About Our Platform")
    hero_subtitle = db.Column(db.Text, nullable=False, default="Learn more about who we are and what we do")
    hero_stat_1_count = db.Column(db.String(50), nullable=False, default="50+")
    hero_stat_1_label = db.Column(db.String(100), nullable=False, default="Team Members")
    hero_stat_2_count = db.Column(db.String(50), nullable=False, default="150+")
    hero_stat_2_label = db.Column(db.String(100), nullable=False, default="Projects")
    hero_stat_3_count = db.Column(db.String(50), nullable=False, default="99%")
    hero_stat_3_label = db.Column(db.String(100), nullable=False, default="Success Rate")
    hero_image_url = db.Column(db.String(255), nullable=True, default="https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=1200&auto=format&fit=crop")
    
    # Mission Section
    mission_title = db.Column(db.String(100), nullable=False, default="Our Mission")
    mission_content = db.Column(db.Text, nullable=False, default="We are dedicated to providing excellent services...")
    
    # Vision Section
    vision_title = db.Column(db.String(100), nullable=False, default="Our Vision")
    vision_content = db.Column(db.Text, nullable=False, default="To be the leading platform in our industry...")
    
    # Values Section
    values_title = db.Column(db.String(100), nullable=False, default="Our Values")
    value1_title = db.Column(db.String(100), nullable=False, default="Innovation")
    value1_description = db.Column(db.Text, nullable=False, default="We constantly innovate to serve you better")
    value2_title = db.Column(db.String(100), nullable=False, default="Quality")
    value2_description = db.Column(db.Text, nullable=False, default="Quality is at the heart of everything we do")
    value3_title = db.Column(db.String(100), nullable=False, default="Transparency")
    value3_description = db.Column(db.Text, nullable=False, default="We believe in open and honest communication")
    value4_title = db.Column(db.String(100), nullable=False, default="Excellence Driven")
    value4_description = db.Column(db.Text, nullable=False, default="We set high standards and continuously strive to exceed them.")
    value5_title = db.Column(db.String(100), nullable=False, default="Continuous Learning")
    value5_description = db.Column(db.Text, nullable=False, default="Growth never stops. We invest in learning at every level.")
    value6_title = db.Column(db.String(100), nullable=False, default="People First")
    value6_description = db.Column(db.Text, nullable=False, default="Our team is our greatest asset. We prioritize well-being.")
    
    # Story Section
    story_title = db.Column(db.String(100), nullable=False, default="Our Story")
    story_content = db.Column(db.Text, nullable=False, default="Founded in 2024, we started with a simple idea...")
    
    # Timeline Section
    timeline_year_1 = db.Column(db.String(20), nullable=False, default="2019")
    timeline_title_1 = db.Column(db.String(100), nullable=False, default="The Beginning")
    timeline_content_1 = db.Column(db.Text, nullable=False, default="Founded with a vision to revolutionize team collaboration.")
    timeline_year_2 = db.Column(db.String(20), nullable=False, default="2021")
    timeline_title_2 = db.Column(db.String(100), nullable=False, default="Major Milestone")
    timeline_content_2 = db.Column(db.Text, nullable=False, default="Reached 10,000 users and launched our mobile app.")
    timeline_year_3 = db.Column(db.String(20), nullable=False, default="2023")
    timeline_title_3 = db.Column(db.String(100), nullable=False, default="Enterprise Growth")
    timeline_content_3 = db.Column(db.Text, nullable=False, default="Launched enterprise features and AI-powered tools.")
    timeline_year_4 = db.Column(db.String(20), nullable=False, default="2025 & Beyond")
    timeline_title_4 = db.Column(db.String(100), nullable=False, default="The Future")
    timeline_content_4 = db.Column(db.Text, nullable=False, default="Continuing innovation with advanced AI features.")
    
    # Team Section
    team_title = db.Column(db.String(100), nullable=False, default="Meet Our Team")
    team_subtitle = db.Column(db.Text, nullable=False, default="The talented people behind our success")
    
    # CTA Section
    cta_title = db.Column(db.String(100), nullable=False, default="Ready to Get Started?")
    cta_subtitle = db.Column(db.Text, nullable=False, default="Join us today and experience the difference")
    cta_button_text = db.Column(db.String(50), nullable=False, default="Explore Services")
    cta_button_2_text = db.Column(db.String(50), nullable=False, default="View Projects")
    cta_button_link = db.Column(db.String(100), nullable=False, default="services.services_list")
    cta_button_2_link = db.Column(db.String(100), nullable=False, default="projects.projects_list")
    
    # Singleton Guard
    singleton_guard = db.Column(db.Integer, unique=True, default=1)
    
    def __repr__(self):
        return f"AboutContent('{self.hero_title}')"
    
    @staticmethod
    def get_content():
        """Get the about page content, create if doesn't exist"""
        content = AboutContent.query.first()
        if not content:
            content = AboutContent()
            db.session.add(content)
            db.session.commit()
        return content
