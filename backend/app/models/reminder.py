from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Reminder details
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    reminder_type = Column(String, nullable=False)  # exercise, medication, appointment
    
    # Scheduling
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    frequency = Column(String, default="once")  # once, daily, weekly, monthly
    is_recurring = Column(Boolean, default=False)
    
    # Status
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Delivery preferences
    send_email = Column(Boolean, default=True)
    send_push = Column(Boolean, default=False)  # Future: push notifications
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # AI personalization
    ai_generated = Column(Boolean, default=False)
    personalization_data = Column(Text)  # JSON string of personalization factors
    
    # Relationships
    user = relationship("User", back_populates="reminders")