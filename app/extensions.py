"""
Extensions Module
Initializes all Flask extensions used throughout the application:
- Database (SQLAlchemy)
- Authentication (Flask-Login, Bcrypt)
- Database Migrations (Flask-Migrate)
- Admin Panel (Flask-Admin)
- Security (CSRF Protection, Rate Limiting)
- Email (Flask-Mail)
"""

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from sqlalchemy import MetaData


# =========================================
# DATABASE CONFIGURATION
# =========================================
# Define naming convention for SQLite compatibility with Alembic
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# =========================================
# EXTENSION INSTANCES
# =========================================
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
admin = Admin()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()