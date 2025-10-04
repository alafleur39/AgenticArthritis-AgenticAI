from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Profile information
    age = Column(Integer)
    arthritis_type = Column(String)  # rheumatoid, osteoarthritis, etc.
    severity_level = Column(Integer)  # 1-10 scale
    affected_joints = Column(Text)  # JSON string of affected joints
    medical_notes = Column(Text)
    
    # Email preferences
    email_reminders_enabled = Column(Boolean, default=True)
    reminder_frequency = Column(String, default="daily")  # daily, weekly, custom
    preferred_reminder_time = Column(String, default="09:00")  # HH:MM format
    
    # Relationships
    exercises = relationship("UserExercise", back_populates="user")
    progress_records = relationship("Progress", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")