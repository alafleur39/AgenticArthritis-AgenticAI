from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.db.database import get_db
from app.models.user import User
from app.models.progress import Progress
from app.models.exercise import Exercise
from app.api.auth import get_current_user
from app.services.ai_agent import ArthritisAIAgent

router = APIRouter()
ai_agent = ArthritisAIAgent()


class ProgressCreate(BaseModel):
    exercise_id: Optional[int] = None
    duration_minutes: int
    repetitions_completed: Optional[int] = None
    pain_level_before: Optional[int] = None
    pain_level_after: Optional[int] = None
    difficulty_rating: Optional[int] = None
    satisfaction_rating: Optional[int] = None
    completion_percentage: float = 100.0
    notes: Optional[str] = None
    mood_before: Optional[str] = None
    mood_after: Optional[str] = None


class ProgressResponse(BaseModel):
    id: int
    exercise_id: Optional[int] = None
    exercise_name: Optional[str] = None
    session_date: datetime
    duration_minutes: int
    repetitions_completed: Optional[int] = None
    pain_level_before: Optional[int] = None
    pain_level_after: Optional[int] = None
    difficulty_rating: Optional[int] = None
    satisfaction_rating: Optional[int] = None
    completion_percentage: float
    notes: Optional[str] = None
    mood_before: Optional[str] = None
    mood_after: Optional[str] = None
    ai_recommendations: Optional[str] = None
    improvement_detected: bool = False

    class Config:
        from_attributes = True


class ProgressSummary(BaseModel):
    total_sessions: int
    total_duration: int
    average_pain_before: float
    average_pain_after: float
    pain_improvement: float
    average_satisfaction: float
    consistency_score: float
    most_effective_exercises: List[dict]
    recent_trends: dict


class AIInsights(BaseModel):
    overall_progress: str
    pain_trend: str
    recommendations: List[str]
    exercise_adjustments: List[dict]
    motivational_message: str


@router.post("/", response_model=ProgressResponse)
def log_progress(
    progress: ProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Log a new progress entry"""
    
    # Validate exercise if provided
    exercise_name = None
    if progress.exercise_id:
        exercise = db.query(Exercise).filter(Exercise.id == progress.exercise_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
        exercise_name = exercise.name
    
    # Create progress entry
    db_progress = Progress(
        user_id=current_user.id,
        **progress.dict()
    )
    
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    
    # Update user exercise statistics if applicable
    if progress.exercise_id:
        from app.models.exercise import UserExercise
        user_exercise = db.query(UserExercise).filter(
            UserExercise.user_id == current_user.id,
            UserExercise.exercise_id == progress.exercise_id
        ).first()
        
        if user_exercise:
            user_exercise.times_completed += 1
            user_exercise.last_completed = datetime.now()
            
            # Update average ratings
            if progress.pain_level_after:
                if user_exercise.average_pain_level:
                    user_exercise.average_pain_level = (
                        user_exercise.average_pain_level + progress.pain_level_after
                    ) / 2
                else:
                    user_exercise.average_pain_level = progress.pain_level_after
            
            if progress.difficulty_rating:
                if user_exercise.average_difficulty:
                    user_exercise.average_difficulty = (
                        user_exercise.average_difficulty + progress.difficulty_rating
                    ) / 2
                else:
                    user_exercise.average_difficulty = progress.difficulty_rating
            
            db.commit()
    
    # Return response with exercise name
    response_data = db_progress.__dict__.copy()
    response_data['exercise_name'] = exercise_name
    
    return response_data


@router.get("/", response_model=List[ProgressResponse])
def get_progress_history(
    skip: int = 0,
    limit: int = 50,
    exercise_id: Optional[int] = None,
    days: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's progress history with optional filtering"""
    
    query = db.query(Progress).filter(Progress.user_id == current_user.id)
    
    if exercise_id:
        query = query.filter(Progress.exercise_id == exercise_id)
    
    if days:
        start_date = datetime.now() - timedelta(days=days)
        query = query.filter(Progress.session_date >= start_date)
    
    progress_records = query.order_by(desc(Progress.session_date)).offset(skip).limit(limit).all()
    
    # Add exercise names
    result = []
    for record in progress_records:
        record_dict = record.__dict__.copy()
        if record.exercise_id:
            exercise = db.query(Exercise).filter(Exercise.id == record.exercise_id).first()
            record_dict['exercise_name'] = exercise.name if exercise else None
        result.append(record_dict)
    
    return result


@router.get("/summary", response_model=ProgressSummary)
def get_progress_summary(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive progress summary"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get progress records for the period
    progress_records = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.session_date >= start_date
    ).all()
    
    if not progress_records:
        return ProgressSummary(
            total_sessions=0,
            total_duration=0,
            average_pain_before=0,
            average_pain_after=0,
            pain_improvement=0,
            average_satisfaction=0,
            consistency_score=0,
            most_effective_exercises=[],
            recent_trends={}
        )
    
    # Calculate metrics
    total_sessions = len(progress_records)
    total_duration = sum(p.duration_minutes for p in progress_records if p.duration_minutes)
    
    pain_before_values = [p.pain_level_before for p in progress_records if p.pain_level_before]
    pain_after_values = [p.pain_level_after for p in progress_records if p.pain_level_after]
    satisfaction_values = [p.satisfaction_rating for p in progress_records if p.satisfaction_rating]
    
    avg_pain_before = sum(pain_before_values) / len(pain_before_values) if pain_before_values else 0
    avg_pain_after = sum(pain_after_values) / len(pain_after_values) if pain_after_values else 0
    avg_satisfaction = sum(satisfaction_values) / len(satisfaction_values) if satisfaction_values else 0
    
    pain_improvement = avg_pain_before - avg_pain_after
    
    # Calculate consistency score (sessions per week)
    weeks = max(1, days / 7)
    consistency_score = min(10, (total_sessions / weeks) * 2)  # Normalize to 0-10 scale
    
    # Find most effective exercises
    exercise_effectiveness = {}
    for record in progress_records:
        if record.exercise_id and record.pain_level_before and record.pain_level_after:
            improvement = record.pain_level_before - record.pain_level_after
            if record.exercise_id not in exercise_effectiveness:
                exercise_effectiveness[record.exercise_id] = []
            exercise_effectiveness[record.exercise_id].append(improvement)
    
    most_effective = []
    for exercise_id, improvements in exercise_effectiveness.items():
        avg_improvement = sum(improvements) / len(improvements)
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if exercise and avg_improvement > 0:
            most_effective.append({
                "exercise_name": exercise.name,
                "average_improvement": round(avg_improvement, 1),
                "sessions": len(improvements)
            })
    
    most_effective.sort(key=lambda x: x["average_improvement"], reverse=True)
    most_effective = most_effective[:5]  # Top 5
    
    # Calculate recent trends (last 7 days vs previous 7 days)
    recent_trends = _calculate_trends(progress_records, days)
    
    return ProgressSummary(
        total_sessions=total_sessions,
        total_duration=total_duration,
        average_pain_before=round(avg_pain_before, 1),
        average_pain_after=round(avg_pain_after, 1),
        pain_improvement=round(pain_improvement, 1),
        average_satisfaction=round(avg_satisfaction, 1),
        consistency_score=round(consistency_score, 1),
        most_effective_exercises=most_effective,
        recent_trends=recent_trends
    )


@router.get("/insights", response_model=AIInsights)
def get_ai_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI-powered insights and recommendations"""
    
    try:
        insights = ai_agent.analyze_progress_and_recommend(current_user, db)
        return AIInsights(**insights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


@router.get("/charts/pain-levels")
def get_pain_level_chart_data(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get pain level data for charts"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    progress_records = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.session_date >= start_date,
        Progress.pain_level_before.isnot(None),
        Progress.pain_level_after.isnot(None)
    ).order_by(Progress.session_date).all()
    
    chart_data = []
    for record in progress_records:
        chart_data.append({
            "date": record.session_date.strftime("%Y-%m-%d"),
            "pain_before": record.pain_level_before,
            "pain_after": record.pain_level_after,
            "improvement": record.pain_level_before - record.pain_level_after
        })
    
    return chart_data


@router.get("/charts/exercise-frequency")
def get_exercise_frequency_data(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get exercise frequency data for charts"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get exercise frequency
    exercise_counts = db.query(
        Exercise.name,
        func.count(Progress.id).label('count')
    ).join(
        Progress, Exercise.id == Progress.exercise_id
    ).filter(
        Progress.user_id == current_user.id,
        Progress.session_date >= start_date
    ).group_by(Exercise.name).all()
    
    return [{"exercise": name, "count": count} for name, count in exercise_counts]


@router.get("/charts/weekly-progress")
def get_weekly_progress_data(
    weeks: int = 12,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get weekly progress data for charts"""
    
    start_date = datetime.now() - timedelta(weeks=weeks)
    
    # Group by week
    weekly_data = db.query(
        func.date_trunc('week', Progress.session_date).label('week'),
        func.count(Progress.id).label('sessions'),
        func.sum(Progress.duration_minutes).label('total_duration'),
        func.avg(Progress.pain_level_before).label('avg_pain_before'),
        func.avg(Progress.pain_level_after).label('avg_pain_after')
    ).filter(
        Progress.user_id == current_user.id,
        Progress.session_date >= start_date
    ).group_by('week').order_by('week').all()
    
    result = []
    for week, sessions, duration, pain_before, pain_after in weekly_data:
        result.append({
            "week": week.strftime("%Y-%m-%d"),
            "sessions": sessions or 0,
            "total_duration": duration or 0,
            "avg_pain_before": round(pain_before, 1) if pain_before else 0,
            "avg_pain_after": round(pain_after, 1) if pain_after else 0,
            "improvement": round(pain_before - pain_after, 1) if pain_before and pain_after else 0
        })
    
    return result


@router.delete("/{progress_id}")
def delete_progress_entry(
    progress_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a progress entry"""
    
    progress = db.query(Progress).filter(
        Progress.id == progress_id,
        Progress.user_id == current_user.id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    
    db.delete(progress)
    db.commit()
    
    return {"message": "Progress entry deleted successfully"}


def _calculate_trends(progress_records: List[Progress], total_days: int) -> dict:
    """Calculate recent trends in progress data"""
    
    if total_days < 14:
        return {}
    
    now = datetime.now()
    mid_point = now - timedelta(days=total_days // 2)
    
    recent_records = [p for p in progress_records if p.session_date >= mid_point]
    older_records = [p for p in progress_records if p.session_date < mid_point]
    
    def calculate_averages(records):
        if not records:
            return {"sessions": 0, "pain_before": 0, "pain_after": 0, "satisfaction": 0}
        
        pain_before = [p.pain_level_before for p in records if p.pain_level_before]
        pain_after = [p.pain_level_after for p in records if p.pain_level_after]
        satisfaction = [p.satisfaction_rating for p in records if p.satisfaction_rating]
        
        return {
            "sessions": len(records),
            "pain_before": sum(pain_before) / len(pain_before) if pain_before else 0,
            "pain_after": sum(pain_after) / len(pain_after) if pain_after else 0,
            "satisfaction": sum(satisfaction) / len(satisfaction) if satisfaction else 0
        }
    
    recent_avg = calculate_averages(recent_records)
    older_avg = calculate_averages(older_records)
    
    return {
        "sessions_trend": recent_avg["sessions"] - older_avg["sessions"],
        "pain_trend": older_avg["pain_after"] - recent_avg["pain_after"],  # Positive = improvement
        "satisfaction_trend": recent_avg["satisfaction"] - older_avg["satisfaction"]
    }