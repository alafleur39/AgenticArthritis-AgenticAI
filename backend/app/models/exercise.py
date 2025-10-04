from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)  # JSON string of step-by-step instructions
    target_joints = Column(Text, nullable=False)  # JSON string of target joints
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    duration_minutes = Column(Integer, default=5)
    repetitions = Column(Integer, default=10)
    category = Column(String, nullable=False)  # flexibility, strength, range_of_motion
    video_url = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # AI-generated metadata
    ai_generated = Column(Boolean, default=False)
    effectiveness_score = Column(Float, default=0.0)  # Based on user feedback
    
    # Relationships
    user_exercises = relationship("UserExercise", back_populates="exercise")


class UserExercise(Base):
    __tablename__ = "user_exercises"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    
    # Personalization
    custom_repetitions = Column(Integer)
    custom_duration = Column(Integer)
    difficulty_adjustment = Column(Integer, default=0)  # -2 to +2 adjustment
    
    # Tracking
    times_completed = Column(Integer, default=0)
    last_completed = Column(DateTime(timezone=True))
    is_favorite = Column(Boolean, default=False)
    is_assigned = Column(Boolean, default=True)
    assigned_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Feedback
    average_pain_level = Column(Float)  # 1-10 scale
    average_difficulty = Column(Float)  # 1-10 scale
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="user_exercises")