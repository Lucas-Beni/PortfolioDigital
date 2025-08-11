#!/usr/bin/env python3
"""
Script to create the admin user
"""
from app import app, db
from models import User

def create_admin_user():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='lucgarcbeni@gmail.com').first()
        
        if admin:
            print("Admin user already exists!")
            print(f"Email: {admin.email}")
            print(f"Is Admin: {admin.is_admin}")
            return admin
        
        # Create admin user
        admin = User.create_local_user(
            email='lucgarcbeni@gmail.com',
            password='Pitanga13*',
            first_name='Lucas',
            last_name='Garcia'
        )
        admin.is_admin = True
        
        db.session.add(admin)
        db.session.commit()
        
        print("✓ Admin user created successfully!")
        print(f"Email: {admin.email}")
        print(f"Name: {admin.display_name}")
        print(f"Is Admin: {admin.is_admin}")
        
        return admin

if __name__ == '__main__':
    create_admin_user()