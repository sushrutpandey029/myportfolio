from app import create_app, db
from app.models.user import User
from getpass import getpass
import sys

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        username = input("Enter admin username: ").strip()
        
        if User.query.filter_by(username=username).first():
            print(f"Error: User '{username}' already exists!")
            sys.exit(1)
        
        email = input("Enter admin email: ").strip()
        
        if User.query.filter_by(email=email).first():
            print(f"Error: Email '{email}' is already registered!")
            sys.exit(1)
        
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
        
        try:
            admin = User(username=username, email=email, is_admin=True)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            
            print(f"\nAdmin user '{username}' created successfully!")
            print(f"Login at: http://127.0.0.1:5000/admin/login")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            sys.exit(1)

def create_default_admin():
    app = create_app()
    
    with app.app_context():
        if User.query.filter_by(username='admin').first():
            print("Default admin already exists!")
            return
        
        try:
            admin = User(username='admin', email='admin@freelancingplatform.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
            print("\nDefault admin created: admin / admin123")
            print("Login at: http://127.0.0.1:5000/admin/login")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    print("\n1. Create custom admin")
    print("2. Create default admin (admin/admin123)")
    
    choice = input("\nChoice (1 or 2): ").strip()
    
    if choice == '1':
        create_admin_user()
    elif choice == '2':
        create_default_admin()
    else:
        print("Invalid choice!")
        sys.exit(1)
