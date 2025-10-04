from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.db.database import get_db
from app.models.user import User
from app.models.exercise import Exercise, UserExercise
from app.api.auth import get_current_user
from app.services.ai_agent import ArthritisAIAgent

router = APIRouter()
ai_agent = ArthritisAIAgent()


class ExerciseBase(BaseModel):
    name: str
    description: str
    instructions: str
    target_joints: str
    difficulty_level: int = 1
    duration_minutes: int = 5
    repetitions: int = 10
    category: str


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseResponse(ExerciseBase):
    id: int
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    ai_generated: bool = False
    effectiveness_score: float = 0.0

    class Config:
        from_attributes = True


class UserExerciseResponse(BaseModel):
    id: int
    exercise: ExerciseResponse
    custom_repetitions: Optional[int] = None
    custom_duration: Optional[int] = None
    difficulty_adjustment: int = 0
    times_completed: int = 0
    last_completed: Optional[datetime] = None
    is_favorite: bool = False
    is_assigned: bool = True
    average_pain_level: Optional[float] = None
    average_difficulty: Optional[float] = None

    class Config:
        from_attributes = True


class ExerciseAssignment(BaseModel):
    exercise_id: int
    custom_repetitions: Optional[int] = None
    custom_duration: Optional[int] = None
    difficulty_adjustment: int = 0


class GenerateExercisesRequest(BaseModel):
    count: int = 5
    focus_areas: Optional[List[str]] = None
    difficulty_preference: Optional[int] = None


@router.get("/", response_model=List[ExerciseResponse])
def get_all_exercises(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    difficulty: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available exercises with optional filtering"""
    query = db.query(Exercise).filter(Exercise.is_active == True)
    
    if category:
        query = query.filter(Exercise.category == category)
    if difficulty:
        query = query.filter(Exercise.difficulty_level == difficulty)
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises


@router.get("/my-exercises", response_model=List[UserExerciseResponse])
def get_my_exercises(
    assigned_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's assigned exercises"""
    query = db.query(UserExercise, Exercise).join(
        Exercise, UserExercise.exercise_id == Exercise.id
    ).filter(UserExercise.user_id == current_user.id)
    
    if assigned_only:
        query = query.filter(UserExercise.is_assigned == True)
    
    user_exercises = query.all()
    
    result = []
    for user_exercise, exercise in user_exercises:
        result.append({
            "id": user_exercise.id,
            "exercise": exercise,
            "custom_repetitions": user_exercise.custom_repetitions,
            "custom_duration": user_exercise.custom_duration,
            "difficulty_adjustment": user_exercise.difficulty_adjustment,
            "times_completed": user_exercise.times_completed,
            "last_completed": user_exercise.last_completed,
            "is_favorite": user_exercise.is_favorite,
            "is_assigned": user_exercise.is_assigned,
            "average_pain_level": user_exercise.average_pain_level,
            "average_difficulty": user_exercise.average_difficulty
        })
    
    return result


@router.post("/assign", response_model=UserExerciseResponse)
def assign_exercise(
    assignment: ExerciseAssignment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign an exercise to the current user"""
    # Check if exercise exists
    exercise = db.query(Exercise).filter(Exercise.id == assignment.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Check if already assigned
    existing = db.query(UserExercise).filter(
        UserExercise.user_id == current_user.id,
        UserExercise.exercise_id == assignment.exercise_id
    ).first()
    
    if existing:
        # Update existing assignment
        existing.custom_repetitions = assignment.custom_repetitions
        existing.custom_duration = assignment.custom_duration
        existing.difficulty_adjustment = assignment.difficulty_adjustment
        existing.is_assigned = True
        db.commit()
        db.refresh(existing)
        
        return {
            "id": existing.id,
            "exercise": exercise,
            "custom_repetitions": existing.custom_repetitions,
            "custom_duration": existing.custom_duration,
            "difficulty_adjustment": existing.difficulty_adjustment,
            "times_completed": existing.times_completed,
            "last_completed": existing.last_completed,
            "is_favorite": existing.is_favorite,
            "is_assigned": existing.is_assigned,
            "average_pain_level": existing.average_pain_level,
            "average_difficulty": existing.average_difficulty
        }
    else:
        # Create new assignment
        user_exercise = UserExercise(
            user_id=current_user.id,
            exercise_id=assignment.exercise_id,
            custom_repetitions=assignment.custom_repetitions,
            custom_duration=assignment.custom_duration,
            difficulty_adjustment=assignment.difficulty_adjustment,
            is_assigned=True
        )
        db.add(user_exercise)
        db.commit()
        db.refresh(user_exercise)
        
        return {
            "id": user_exercise.id,
            "exercise": exercise,
            "custom_repetitions": user_exercise.custom_repetitions,
            "custom_duration": user_exercise.custom_duration,
            "difficulty_adjustment": user_exercise.difficulty_adjustment,
            "times_completed": user_exercise.times_completed,
            "last_completed": user_exercise.last_completed,
            "is_favorite": user_exercise.is_favorite,
            "is_assigned": user_exercise.is_assigned,
            "average_pain_level": user_exercise.average_pain_level,
            "average_difficulty": user_exercise.average_difficulty
        }


@router.delete("/unassign/{user_exercise_id}")
def unassign_exercise(
    user_exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unassign an exercise from the current user"""
    user_exercise = db.query(UserExercise).filter(
        UserExercise.id == user_exercise_id,
        UserExercise.user_id == current_user.id
    ).first()
    
    if not user_exercise:
        raise HTTPException(status_code=404, detail="Exercise assignment not found")
    
    user_exercise.is_assigned = False
    db.commit()
    
    return {"message": "Exercise unassigned successfully"}


@router.post("/favorite/{user_exercise_id}")
def toggle_favorite(
    user_exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle favorite status of an exercise"""
    user_exercise = db.query(UserExercise).filter(
        UserExercise.id == user_exercise_id,
        UserExercise.user_id == current_user.id
    ).first()
    
    if not user_exercise:
        raise HTTPException(status_code=404, detail="Exercise assignment not found")
    
    user_exercise.is_favorite = not user_exercise.is_favorite
    db.commit()
    
    return {"message": f"Exercise {'added to' if user_exercise.is_favorite else 'removed from'} favorites"}


@router.post("/generate", response_model=List[dict])
def generate_ai_exercises(
    request: GenerateExercisesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate personalized exercises using AI"""
    try:
        exercises = ai_agent.generate_personalized_exercises(
            current_user, db, count=request.count
        )
        return exercises
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating exercises: {str(e)}")


@router.post("/create", response_model=ExerciseResponse)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new exercise (admin functionality)"""
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific exercise by ID"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.get("/categories/list")
def get_exercise_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of available exercise categories"""
    categories = db.query(Exercise.category).distinct().all()
    return [category[0] for category in categories if category[0]]