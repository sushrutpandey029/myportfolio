"""
Admin User Creation Script
Provides utilities to create admin users for the application:
- Interactive admin user creation
- Default admin creation
- Password validation
- Database interaction
"""

# =========================================
# STANDARD LIBRARY IMPORTS
# =========================================
import sys
from getpass import getpass

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app import create_app, db
from app.models.user import User


# =========================================
# ADMIN CREATION FUNCTIONS
# =========================================

def create_admin_user():
    """
    Create a custom admin user with interactive prompts.
    
    Prompts for username, email, and password with validation.
    """
    app = create_app()
    
    with app.app_context():
        # Get username
        username = input("Enter admin username: ").strip()
        
        if User.query.filter_by(username=username).first():
            print(f"Error: User '{username}' already exists!")
            sys.exit(1)
        
        # Get email
        email = input("Enter admin email: ").strip()
        
        if User.query.filter_by(email=email).first():
            print(f"Error: Email '{email}' is already registered!")
            sys.exit(1)
        
        # Get and validate password
        while True:
            password = getpass("Enter admin password: ")
            password_confirm = getpass("Confirm password: ")
            
            if password != password_confirm:
                print("Passwords don't match! Try again.")
                continue
            
            if len(password) < 6:
                print("Password must be at least 6 characters!")
                continue
            
            break
        
        # Create admin user
        try:
            admin = User(
                username=username,
                email=email,
                password=password,
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            
            print(f"\n✓ Admin user '{username}' created successfully!")
            print(f"Login at: http://127.0.0.1:5000/admin/login")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            sys.exit(1)


def create_default_admin():
    """
    Create a default admin user with preset credentials.
    
    Username: admin
    Password: admin123
    Email: admin@freelancingplatform.com
    """
    app = create_app()
    
    with app.app_context():
        if User.query.filter_by(username='admin').first():
            print("Default admin already exists!")
            return
        
        try:
            admin = User(
                username='admin',
                email='admin@freelancingplatform.com',
                password='admin123',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            
            print("\n✓ Default admin created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("Login at: http://127.0.0.1:5000/admin/login")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            sys.exit(1)


# =========================================
# MAIN EXECUTION
# =========================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("   Admin User Creation Utility")
    print("="*50)
    print("\nOptions:")
    print("  1. Create custom admin (interactive)")
    print("  2. Create default admin (admin/admin123)")
    print("="*50)
    
    choice = input("\nSelect option (1 or 2): ").strip()
    
    if choice == '1':
        create_admin_user()
    elif choice == '2':
        create_default_admin()
    else:
        print("\n✗ Invalid choice! Please select 1 or 2.")
        sys.exit(1)
