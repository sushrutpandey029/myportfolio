"""
User Model Module
Handles user authentication and account management
- User registration and login
- Password hashing and verification
- Role-based access control (admin/user)
"""

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from flask_login import UserMixin

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db, bcrypt
from app.models.base import BaseModel


# =========================================
# USER MODEL
# =========================================

class User(UserMixin, BaseModel):
    """User model for both admins and regular users"""
    
    __tablename__ = 'users'
    
    # Columns
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    downloads = db.relationship('Download', backref='user', lazy=True)
    
    def __init__(self, username, email, password, role='user'):
        """Initialize user with hashed password"""
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
        
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        """Check if the provided password matches the hashed password"""
        return bcrypt.check_password_hash(self.password_hash, password)
        
    def is_admin(self):
        """Check if the user has admin privileges"""
        return self.role == 'admin'
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"