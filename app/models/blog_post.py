"""
Blog Post Model Module
Manages blog posts and articles
"""

# =========================================
# STANDARD LIBRARY IMPORTS
# =========================================
from datetime import datetime

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db


# =========================================
# BLOG POST MODEL
# =========================================

class BlogPost(db.Model):
    """Model for blog posts"""
    
    __tablename__ = 'blog_posts'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    read_time = db.Column(db.String(20), default='5 min read')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'
