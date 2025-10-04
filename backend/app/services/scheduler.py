from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.services.email_service import EmailService
from app.services.ai_agent import ArthritisAIAgent
import logging

logger = logging.getLogger(__name__)


class AutomationScheduler:
    """
    Handles automated tasks like sending reminders, generating exercises, and progress analysis
    """
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.email_service = EmailService()
        self.ai_agent = ArthritisAIAgent()
        self.is_running = False
    
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            self._setup_jobs()
            self.scheduler.start()
            self.is_running = True
            logger.info("Automation scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Automation scheduler stopped")
    
    def _setup_jobs(self):
        """Setup all scheduled jobs"""
        
        # Process scheduled reminders every 5 minutes
        self.scheduler.add_job(
            func=self._process_scheduled_reminders,
            trigger=CronTrigger(minute="*/5"),
            id="process_reminders",
            name="Process Scheduled Reminders",
            replace_existing=True
        )
        
        # Send daily exercise reminders at 9 AM
        self.scheduler.add_job(
            func=self._send_daily_reminders,
            trigger=CronTrigger(hour=9, minute=0),
            id="daily_reminders",
            name="Send Daily Exercise Reminders",
            replace_existing=True
        )
        
        # Send weekly progress summaries on Sundays at 6 PM
        self.scheduler.add_job(
            func=self._send_weekly_summaries,
            trigger=CronTrigger(day_of_week=6, hour=18, minute=0),
            id="weekly_summaries",
            name="Send Weekly Progress Summaries",
            replace_existing=True
        )
        
        # Generate new AI exercises for users weekly on Mondays at 8 AM
        self.scheduler.add_job(
            func=self._generate_weekly_exercises,
            trigger=CronTrigger(day_of_week=0, hour=8, minute=0),
            id="weekly_exercises",
            name="Generate Weekly AI Exercises",
            replace_existing=True
        )
        
        # Analyze user progress and send insights monthly on 1st at 10 AM
        self.scheduler.add_job(
            func=self._monthly_progress_analysis,
            trigger=CronTrigger(day=1, hour=10, minute=0),
            id="monthly_analysis",
            name="Monthly Progress Analysis",
            replace_existing=True
        )
        
        # Clean up old data monthly on 15th at 2 AM
        self.scheduler.add_job(
            func=self._cleanup_old_data,
            trigger=CronTrigger(day=15, hour=2, minute=0),
            id="data_cleanup",
            name="Clean Up Old Data",
            replace_existing=True
        )
    
    def _process_scheduled_reminders(self):
        """Process all scheduled reminders that are due"""
        try:
            db = SessionLocal()
            sent_count = self.email_service.process_scheduled_reminders(db)
            if sent_count > 0:
                logger.info(f"Processed {sent_count} scheduled reminders")
            db.close()
        except Exception as e:
            logger.error(f"Error processing scheduled reminders: {str(e)}")
    
    def _send_daily_reminders(self):
        """Send daily exercise reminders to users who have them enabled"""
        try:
            db = SessionLocal()
            
            # Get users who have daily reminders enabled
            users = db.query(User).filter(
                User.is_active == True,
                User.email_reminders_enabled == True,
                User.reminder_frequency.in_(["daily", "custom"])
            ).all()
            
            sent_count = 0
            for user in users:
                # Check if it's the right time for this user
                if self._is_reminder_time(user):
                    success = self.email_service.send_exercise_reminder(user, db, "daily")
                    if success:
                        sent_count += 1
            
            logger.info(f"Sent {sent_count} daily exercise reminders")
            db.close()
            
        except Exception as e:
            logger.error(f"Error sending daily reminders: {str(e)}")
    
    def _send_weekly_summaries(self):
        """Send weekly progress summaries to active users"""
        try:
            db = SessionLocal()
            
            # Get active users
            users = db.query(User).filter(
                User.is_active == True,
                User.email_reminders_enabled == True
            ).all()
            
            sent_count = 0
            for user in users:
                success = self.email_service.send_progress_summary(user, db, "weekly")
                if success:
                    sent_count += 1
            
            logger.info(f"Sent {sent_count} weekly progress summaries")
            db.close()
            
        except Exception as e:
            logger.error(f"Error sending weekly summaries: {str(e)}")
    
    def _generate_weekly_exercises(self):
        """Generate new AI exercises for users weekly"""
        try:
            db = SessionLocal()
            
            # Get active users
            users = db.query(User).filter(User.is_active == True).all()
            
            generated_count = 0
            for user in users:
                try:
                    # Generate new exercises
                    new_exercises = self.ai_agent.generate_personalized_exercises(user, db, count=2)
                    
                    if new_exercises:
                        # Store exercises in database
                        self._store_generated_exercises(user, new_exercises, db)
                        generated_count += 1
                        
                except Exception as e:
                    logger.error(f"Error generating exercises for user {user.id}: {str(e)}")
                    continue
            
            logger.info(f"Generated exercises for {generated_count} users")
            db.close()
            
        except Exception as e:
            logger.error(f"Error in weekly exercise generation: {str(e)}")
    
    def _monthly_progress_analysis(self):
        """Perform monthly progress analysis and send insights"""
        try:
            db = SessionLocal()
            
            # Get users with progress data
            users = db.query(User).filter(User.is_active == True).all()
            
            analyzed_count = 0
            for user in users:
                try:
                    # Get AI analysis
                    analysis = self.ai_agent.analyze_progress_and_recommend(user, db)
                    
                    # Send monthly summary with insights
                    success = self.email_service.send_progress_summary(user, db, "monthly")
                    if success:
                        analyzed_count += 1
                        
                except Exception as e:
                    logger.error(f"Error analyzing progress for user {user.id}: {str(e)}")
                    continue
            
            logger.info(f"Sent monthly analysis to {analyzed_count} users")
            db.close()
            
        except Exception as e:
            logger.error(f"Error in monthly progress analysis: {str(e)}")
    
    def _cleanup_old_data(self):
        """Clean up old data to maintain database performance"""
        try:
            db = SessionLocal()
            
            # Clean up old reminders (older than 6 months)
            six_months_ago = datetime.now() - timedelta(days=180)
            
            from app.models.reminder import Reminder
            old_reminders = db.query(Reminder).filter(
                Reminder.created_at < six_months_ago,
                Reminder.is_sent == True,
                Reminder.is_recurring == False
            ).delete()
            
            # Clean up very old progress records (older than 2 years, keep monthly summaries)
            two_years_ago = datetime.now() - timedelta(days=730)
            
            from app.models.progress import Progress
            # This is a simplified cleanup - in production, you might want to aggregate old data
            very_old_progress = db.query(Progress).filter(
                Progress.session_date < two_years_ago
            ).count()
            
            db.commit()
            logger.info(f"Cleaned up {old_reminders} old reminders, found {very_old_progress} old progress records")
            db.close()
            
        except Exception as e:
            logger.error(f"Error in data cleanup: {str(e)}")
    
    def _is_reminder_time(self, user: User) -> bool:
        """Check if it's the right time to send a reminder to this user"""
        try:
            if not user.preferred_reminder_time:
                return True  # Default to sending if no preference set
            
            # Parse user's preferred time (format: "HH:MM")
            preferred_hour, preferred_minute = map(int, user.preferred_reminder_time.split(":"))
            
            # Get current time
            now = datetime.now()
            
            # Check if current time matches preferred time (within 1 hour window)
            return (
                now.hour == preferred_hour or 
                (now.hour == preferred_hour + 1 and now.minute < 30)
            )
            
        except Exception as e:
            logger.error(f"Error checking reminder time for user {user.id}: {str(e)}")
            return True  # Default to sending on error
    
    def _store_generated_exercises(self, user: User, exercises: list, db: Session):
        """Store AI-generated exercises in the database"""
        try:
            from app.models.exercise import Exercise, UserExercise
            
            for exercise_data in exercises:
                # Create exercise if it doesn't exist
                exercise = Exercise(
                    name=exercise_data.get("name", "AI Generated Exercise"),
                    description=exercise_data.get("description", ""),
                    instructions=str(exercise_data.get("instructions", [])),
                    target_joints=str(exercise_data.get("target_joints", [])),
                    difficulty_level=exercise_data.get("difficulty_level", 1),
                    duration_minutes=exercise_data.get("duration_minutes", 5),
                    repetitions=exercise_data.get("repetitions", 10),
                    category=exercise_data.get("category", "flexibility"),
                    ai_generated=True
                )
                
                db.add(exercise)
                db.flush()  # Get the ID
                
                # Assign to user
                user_exercise = UserExercise(
                    user_id=user.id,
                    exercise_id=exercise.id,
                    is_assigned=True
                )
                
                db.add(user_exercise)
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing generated exercises: {str(e)}")
            db.rollback()
    
    def schedule_custom_reminder(
        self,
        user_id: int,
        title: str,
        message: str,
        scheduled_time: datetime,
        reminder_type: str = "custom"
    ):
        """Schedule a one-time custom reminder"""
        try:
            job_id = f"custom_reminder_{user_id}_{int(scheduled_time.timestamp())}"
            
            self.scheduler.add_job(
                func=self._send_custom_reminder,
                trigger="date",
                run_date=scheduled_time,
                args=[user_id, title, message, reminder_type],
                id=job_id,
                name=f"Custom Reminder: {title}",
                replace_existing=True
            )
            
            logger.info(f"Scheduled custom reminder for user {user_id} at {scheduled_time}")
            return job_id
            
        except Exception as e:
            logger.error(f"Error scheduling custom reminder: {str(e)}")
            return None
    
    def _send_custom_reminder(self, user_id: int, title: str, message: str, reminder_type: str):
        """Send a custom reminder"""
        try:
            db = SessionLocal()
            user = db.query(User).filter(User.id == user_id).first()
            
            if user and user.is_active:
                self.email_service.send_custom_reminder(user, db, title, message, reminder_type)
            
            db.close()
            
        except Exception as e:
            logger.error(f"Error sending custom reminder: {str(e)}")
    
    def get_scheduler_status(self) -> dict:
        """Get current scheduler status and job information"""
        try:
            jobs = []
            for job in self.scheduler.get_jobs():
                jobs.append({
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                    "trigger": str(job.trigger)
                })
            
            return {
                "running": self.is_running,
                "jobs": jobs,
                "job_count": len(jobs)
            }
            
        except Exception as e:
            logger.error(f"Error getting scheduler status: {str(e)}")
            return {"running": self.is_running, "error": str(e)}


# Global scheduler instance
automation_scheduler = AutomationScheduler()