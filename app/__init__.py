from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.extensions import db, bcrypt, login_manager, migrate, admin, limiter, csrf, mail

# Import extensions from extensions.py
db = db
bcrypt = bcrypt
login_manager = login_manager
login_manager.login_view = 'auth.admin_login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))
migrate = migrate
admin = admin

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Security headers
    @app.after_request
    def after_request(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    admin.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    
    # Context processor to inject environment variables into all templates
    @app.context_processor
    def inject_env_vars():
        import os
        from dotenv import load_dotenv
        
        # In debug mode, reload .env on every request to pick up changes automatically
        if app.debug:
            load_dotenv()
            # Update app.config with new values from OS environment
            for key in app.config.keys():
                if key in os.environ:
                    app.config[key] = os.environ.get(key)

        return {
            'env': {
                'CONTACT_EMAIL': app.config.get('CONTACT_EMAIL', ''),
                'SUPPORT_EMAIL': app.config.get('SUPPORT_EMAIL', ''),
                'CONTACT_PHONE': app.config.get('CONTACT_PHONE', ''),
                'WHATSAPP_NUMBER': app.config.get('WHATSAPP_NUMBER', ''),
                'BUSINESS_ADDRESS_LINE1': app.config.get('BUSINESS_ADDRESS_LINE1', ''),
                'BUSINESS_ADDRESS_LINE2': app.config.get('BUSINESS_ADDRESS_LINE2', ''),
                'BUSINESS_COUNTRY': app.config.get('BUSINESS_COUNTRY', ''),
                'TWITTER_URL': app.config.get('TWITTER_URL', '#'),
                'LINKEDIN_URL': app.config.get('LINKEDIN_URL', '#'),
                'GITHUB_URL': app.config.get('GITHUB_URL', '#'),
                'DISCORD_URL': app.config.get('DISCORD_URL', '#'),
                'FACEBOOK_URL': app.config.get('FACEBOOK_URL', '#'),
                'BRAND_NAME': app.config.get('BRAND_NAME', 'Platform'),
                'BRAND_TAGLINE': app.config.get('BRAND_TAGLINE', ''),
                'COPYRIGHT_YEAR': app.config.get('COPYRIGHT_YEAR', '2025'),
                'COPYRIGHT_TEXT': app.config.get('COPYRIGHT_TEXT', 'All rights reserved.')
            }
        }
    
    # Import and register blueprints
    from app.auth.routes import auth
    from app.admin.routes import admin_bp
    from app.pages.routes import pages
    from app.services.routes import services
    from app.projects.routes import projects
    from app.study_material.routes import study_material
    from app.youtube.routes import youtube
    from app.contact.routes import contact
    
    app.register_blueprint(auth)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pages)
    app.register_blueprint(services)
    app.register_blueprint(projects)
    app.register_blueprint(study_material)
    app.register_blueprint(youtube)
    app.register_blueprint(contact)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Disable cache for development (prevents image caching issues)
    @app.after_request
    def add_header(response):
        if app.debug:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
        return response
    
    return app