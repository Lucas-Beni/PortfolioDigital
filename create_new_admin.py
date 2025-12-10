"""
Script to create a new admin user for the portfolio
"""
import os
import sys

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def create_admin():
    with app.app_context():
        # Admin credentials
        admin_email = "admin@portfolio.com"
        admin_password = "admin123"
        
        # Check if admin exists
        existing_admin = User.query.filter_by(email=admin_email).first()
        
        if existing_admin:
            # Update existing admin password
            existing_admin.set_password(admin_password)
            existing_admin.is_admin = True
            db.session.commit()
            print(f"Admin user updated!")
            print(f"Email: {admin_email}")
            print(f"Password: {admin_password}")
        else:
            # Create new admin
            admin = User.create_local_user(
                email=admin_email,
                password=admin_password,
                first_name="Lucas",
                last_name="Admin",
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"New admin user created!")
            print(f"Email: {admin_email}")
            print(f"Password: {admin_password}")
        
        return admin_email, admin_password

if __name__ == "__main__":
    create_admin()
