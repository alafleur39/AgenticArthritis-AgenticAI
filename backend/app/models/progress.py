from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    
    # Session details
    session_date = Column(DateTime(timezone=True), server_default=func.now())
    duration_minutes = Column(Integer, nullable=False)
    repetitions_completed = Column(Integer)
    
    # User feedback
    pain_level_before = Column(Integer)  # 1-10 scale
    pain_level_after = Column(Integer)   # 1-10 scale
    difficulty_rating = Column(Integer)  # 1-10 scale
    satisfaction_rating = Column(Integer)  # 1-10 scale
    
    # Performance metrics
    completion_percentage = Column(Float, default=100.0)
    form_quality = Column(Integer)  # 1-10 scale (future: AI assessment)
    
    # Notes and observations
    notes = Column(Text)
    mood_before = Column(String)  # happy, neutral, frustrated, etc.
    mood_after = Column(String)
    
    # AI insights
    ai_recommendations = Column(Text)  # JSON string of AI-generated recommendations
    improvement_detected = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    exercise = relationship("Exercise")