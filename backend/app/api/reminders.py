from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.db.database import get_db
from app.models.user import User
from app.models.reminder import Reminder
from app.api.auth import get_current_user
from app.services.email_service import EmailService
from app.services.scheduler import automation_scheduler

router = APIRouter()
email_service = EmailService()


class ReminderCreate(BaseModel):
    title: str
    message: str
    reminder_type: str = "exercise"
    scheduled_time: datetime
    is_recurring: bool = False
    frequency: str = "once"
    send_email: bool = True


class ReminderResponse(BaseModel):
    id: int
    title: str
    message: str
    reminder_type: str
    scheduled_time: datetime
    frequency: str
    is_recurring: bool
    is_sent: bool
    sent_at: Optional[datetime] = None
    is_active: bool
    send_email: bool
    ai_generated: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    is_active: Optional[bool] = None
    send_email: Optional[bool] = None


class UserPreferencesUpdate(BaseModel):
    email_reminders_enabled: bool
    reminder_frequency: str  # daily, weekly, custom
    preferred_reminder_time: str  # HH:MM format


class SendReminderRequest(BaseModel):
    reminder_type: str = "daily"


@router.post("/", response_model=ReminderResponse)
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new reminder"""
    
    db_reminder = Reminder(
        user_id=current_user.id,
        **reminder.dict()
    )
    
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    
    # Schedule the reminder if it's in the future
    if reminder.scheduled_time > datetime.now():
        automation_scheduler.schedule_custom_reminder(
            user_id=current_user.id,
            title=reminder.title,
            message=reminder.message,
            scheduled_time=reminder.scheduled_time,
            reminder_type=reminder.reminder_type
        )
    
    return db_reminder


@router.get("/", response_model=List[ReminderResponse])
def get_reminders(
    skip: int = 0,
    limit: int = 50,
    active_only: bool = True,
    reminder_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's reminders"""
    
    query = db.query(Reminder).filter(Reminder.user_id == current_user.id)
    
    if active_only:
        query = query.filter(Reminder.is_active == True)
    
    if reminder_type:
        query = query.filter(Reminder.reminder_type == reminder_type)
    
    reminders = query.order_by(Reminder.scheduled_time.desc()).offset(skip).limit(limit).all()
    return reminders


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific reminder"""
    
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    return reminder


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    reminder_update: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a reminder"""
    
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Update fields
    for field, value in reminder_update.dict(exclude_unset=True).items():
        setattr(reminder, field, value)
    
    db.commit()
    db.refresh(reminder)
    
    return reminder


@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a reminder"""
    
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    db.delete(reminder)
    db.commit()
    
    return {"message": "Reminder deleted successfully"}


@router.post("/send-now")
def send_reminder_now(
    request: SendReminderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a reminder immediately"""
    
    try:
        if request.reminder_type == "exercise":
            success = email_service.send_exercise_reminder(current_user, db, "manual")
        elif request.reminder_type == "progress":
            success = email_service.send_progress_summary(current_user, db, "weekly")
        else:
            raise HTTPException(status_code=400, detail="Invalid reminder type")
        
        if success:
            return {"message": "Reminder sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send reminder")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending reminder: {str(e)}")


@router.post("/schedule-daily")
def schedule_daily_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Schedule daily exercise reminders based on user preferences"""
    
    if not current_user.email_reminders_enabled:
        raise HTTPException(status_code=400, detail="Email reminders are disabled")
    
    if current_user.reminder_frequency != "daily":
        raise HTTPException(status_code=400, detail="User is not set up for daily reminders")
    
    # Parse preferred time
    try:
        hour, minute = map(int, current_user.preferred_reminder_time.split(":"))
    except:
        hour, minute = 9, 0  # Default to 9 AM
    
    # Schedule for the next 7 days
    reminders_created = 0
    for i in range(1, 8):  # Next 7 days
        reminder_time = datetime.now().replace(
            hour=hour, minute=minute, second=0, microsecond=0
        ) + timedelta(days=i)
        
        # Check if reminder already exists for this time
        existing = db.query(Reminder).filter(
            Reminder.user_id == current_user.id,
            Reminder.scheduled_time == reminder_time,
            Reminder.reminder_type == "exercise",
            Reminder.is_active == True
        ).first()
        
        if not existing:
            reminder = Reminder(
                user_id=current_user.id,
                title="Daily Exercise Reminder",
                message="Time for your daily arthritis exercises!",
                reminder_type="exercise",
                scheduled_time=reminder_time,
                is_recurring=False,
                frequency="daily",
                send_email=True
            )
            
            db.add(reminder)
            reminders_created += 1
    
    db.commit()
    
    return {"message": f"Scheduled {reminders_created} daily reminders"}


@router.put("/preferences")
def update_reminder_preferences(
    preferences: UserPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user's reminder preferences"""
    
    # Validate preferred time format
    if preferences.preferred_reminder_time:
        try:
            hour, minute = map(int, preferences.preferred_reminder_time.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time")
        except:
            raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM")
    
    # Update user preferences
    current_user.email_reminders_enabled = preferences.email_reminders_enabled
    current_user.reminder_frequency = preferences.reminder_frequency
    current_user.preferred_reminder_time = preferences.preferred_reminder_time
    
    db.commit()
    
    return {"message": "Reminder preferences updated successfully"}


@router.get("/preferences/current")
def get_reminder_preferences(
    current_user: User = Depends(get_current_user)
):
    """Get current reminder preferences"""
    
    return {
        "email_reminders_enabled": current_user.email_reminders_enabled,
        "reminder_frequency": current_user.reminder_frequency,
        "preferred_reminder_time": current_user.preferred_reminder_time
    }


@router.get("/stats/summary")
def get_reminder_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get reminder statistics"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get reminder statistics
    total_reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.created_at >= start_date
    ).count()
    
    sent_reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.created_at >= start_date,
        Reminder.is_sent == True
    ).count()
    
    pending_reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.scheduled_time > datetime.now(),
        Reminder.is_active == True,
        Reminder.is_sent == False
    ).count()
    
    # Get reminder types breakdown
    reminder_types = db.query(
        Reminder.reminder_type,
        db.func.count(Reminder.id).label('count')
    ).filter(
        Reminder.user_id == current_user.id,
        Reminder.created_at >= start_date
    ).group_by(Reminder.reminder_type).all()
    
    types_breakdown = {reminder_type: count for reminder_type, count in reminder_types}
    
    return {
        "total_reminders": total_reminders,
        "sent_reminders": sent_reminders,
        "pending_reminders": pending_reminders,
        "delivery_rate": round((sent_reminders / total_reminders * 100), 1) if total_reminders > 0 else 0,
        "types_breakdown": types_breakdown,
        "preferences": {
            "email_enabled": current_user.email_reminders_enabled,
            "frequency": current_user.reminder_frequency,
            "preferred_time": current_user.preferred_reminder_time
        }
    }