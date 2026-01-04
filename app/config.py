"""
Application Configuration Module
Manages all configuration settings loaded from environment variables:
- Security Settings
- Database Configuration
- Brand Information
- Contact Details
- Social Media Links
- Email Settings
"""

# =========================================
# STANDARD LIBRARY IMPORTS
# =========================================
import os

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# =========================================
# CONFIGURATION CLASS
# =========================================

class Config:
    """Main configuration class for the application"""
    
    # =====================================
    # SECURITY SETTINGS
    # =====================================
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # =====================================
    # DATABASE CONFIGURATION
    # =====================================
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # =====================================
    # BRAND INFORMATION
    # =====================================
    BRAND_NAME = os.environ.get('BRAND_NAME', 'Platform')
    BRAND_TAGLINE = os.environ.get('BRAND_TAGLINE', '')
    
    # =====================================
    # CONTACT INFORMATION
    # =====================================
    SUPPORT_EMAIL = os.environ.get('SUPPORT_EMAIL', '')
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', '')
    CONTACT_PHONE = os.environ.get('CONTACT_PHONE', '')
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '')
    
    # =====================================
    # BUSINESS ADDRESS
    # =====================================
    BUSINESS_ADDRESS_LINE1 = os.environ.get('BUSINESS_ADDRESS_LINE1', '')
    BUSINESS_ADDRESS_LINE2 = os.environ.get('BUSINESS_ADDRESS_LINE2', '')
    BUSINESS_COUNTRY = os.environ.get('BUSINESS_COUNTRY', '')
    
    # =====================================
    # SOCIAL MEDIA LINKS
    # =====================================
    TWITTER_URL = os.environ.get('TWITTER_URL', '#')
    FACEBOOK_URL = os.environ.get('FACEBOOK_URL', '#')
    LINKEDIN_URL = os.environ.get('LINKEDIN_URL', '#')
    GITHUB_URL = os.environ.get('GITHUB_URL', '#')
    DISCORD_URL = os.environ.get('DISCORD_URL', '#')
    
    # =====================================
    # COPYRIGHT INFORMATION
    # =====================================
    COPYRIGHT_YEAR = os.environ.get('COPYRIGHT_YEAR', '2025')
    COPYRIGHT_TEXT = os.environ.get('COPYRIGHT_TEXT', 'All rights reserved.')

    # =====================================
    # EMAIL CONFIGURATION
    # =====================================
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')