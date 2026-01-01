import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Secret key for signing cookies and other security-related needs
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Brand Information
    BRAND_NAME = os.environ.get('BRAND_NAME', 'Platform')
    BRAND_TAGLINE = os.environ.get('BRAND_TAGLINE', '')
    
    # Contact Information
    SUPPORT_EMAIL = os.environ.get('SUPPORT_EMAIL', '')
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', '')
    CONTACT_PHONE = os.environ.get('CONTACT_PHONE', '')
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '')
    
    # Business Address
    BUSINESS_ADDRESS_LINE1 = os.environ.get('BUSINESS_ADDRESS_LINE1', '')
    BUSINESS_ADDRESS_LINE2 = os.environ.get('BUSINESS_ADDRESS_LINE2', '')
    BUSINESS_COUNTRY = os.environ.get('BUSINESS_COUNTRY', '')
    
    # Social Media Links
    TWITTER_URL = os.environ.get('TWITTER_URL', '#')
    FACEBOOK_URL = os.environ.get('FACEBOOK_URL', '#')
    LINKEDIN_URL = os.environ.get('LINKEDIN_URL', '#')
    GITHUB_URL = os.environ.get('GITHUB_URL', '#')
    DISCORD_URL = os.environ.get('DISCORD_URL', '#')
    
    # Copyright
    COPYRIGHT_YEAR = os.environ.get('COPYRIGHT_YEAR', '2025')
    COPYRIGHT_TEXT = os.environ.get('COPYRIGHT_TEXT', 'All rights reserved.')

    # Mail configuration (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')