#!/usr/bin/env python3
"""
Create demo user for Agent Arthritis application
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.user import User
import hashlib

def get_password_hash(password: str) -> str:
    # Use simple SHA256 for demo
    return 'sha256:' + hashlib.sha256(password.encode()).hexdigest()

def create_demo_user():
    """Create demo user in the database"""
    db = SessionLocal()
    try:
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == 'demo@agentarthritis.com').first()
        if demo_user:
            print('Demo user already exists')
            return
        
        # Create demo user
        demo_user = User(
            email='demo@agentarthritis.com',
            full_name='Demo User',
            hashed_password=get_password_hash('demo123'),
            is_active=True,
            age=45,
            arthritis_type='rheumatoid',
            severity_level=3,
            email_reminders_enabled=True,
            reminder_frequency='daily',
            preferred_reminder_time='09:00'
        )
        db.add(demo_user)
        db.commit()
        print('Demo user created successfully!')
        print('Email: demo@agentarthritis.com')
        print('Password: demo123')
        
    except Exception as e:
        print(f'Error creating demo user: {str(e)}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()