from app.extensions import db
from datetime import datetime

class BaseModel(db.Model):
    """Base model class that provides common columns and methods"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save the current instance to the database"""
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        """Delete the current instance from the database"""
        db.session.delete(self)
        db.session.commit()