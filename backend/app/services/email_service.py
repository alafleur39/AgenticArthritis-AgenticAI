import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.reminder import Reminder
from app.services.ai_agent import ArthritisAIAgent
from app.core.config import settings
import logging
import json

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service for sending automated email reminders and notifications
    """
    
    def __init__(self):
        self.sg = None
        if settings.sendgrid_api_key:
            self.sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
        self.ai_agent = ArthritisAIAgent()
    
    def send_exercise_reminder(
        self, 
        user: User, 
        db: Session,
        reminder_type: str = "daily"
    ) -> bool:
        """
        Send personalized exercise reminder email
        """
        try:
            if not self.sg:
                logger.warning("SendGrid not configured, skipping email")
                return False
            
            # Generate personalized content
            motivational_message = self.ai_agent.generate_motivational_message(
                user, db, context=reminder_type
            )
            
            # Get user's current exercises
            current_exercises = self._get_user_current_exercises(user, db)
            
            # Create email content
            subject = self._get_reminder_subject(user, reminder_type)
            html_content = self._create_reminder_email_html(
                user, motivational_message, current_exercises, reminder_type
            )
            
            # Send email
            success = self._send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content
            )
            
            if success:
                # Log the reminder
                self._log_reminder_sent(user, db, reminder_type, subject)
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending exercise reminder: {str(e)}")
            return False
    
    def send_progress_summary(
        self, 
        user: User, 
        db: Session,
        period: str = "weekly"
    ) -> bool:
        """
        Send progress summary email with AI insights
        """
        try:
            if not self.sg:
                logger.warning("SendGrid not configured, skipping email")
                return False
            
            # Get AI analysis
            progress_analysis = self.ai_agent.analyze_progress_and_recommend(user, db)
            
            # Get progress data
            progress_data = self._get_progress_summary_data(user, db, period)
            
            # Create email content
            subject = f"Your {period.title()} Arthritis Progress Summary"
            html_content = self._create_progress_summary_html(
                user, progress_analysis, progress_data, period
            )
            
            # Send email
            success = self._send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content
            )
            
            if success:
                self._log_reminder_sent(user, db, f"progress_{period}", subject)
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending progress summary: {str(e)}")
            return False
    
    def send_custom_reminder(
        self, 
        user: User, 
        db: Session,
        title: str,
        message: str,
        reminder_type: str = "custom"
    ) -> bool:
        """
        Send custom reminder email
        """
        try:
            if not self.sg:
                logger.warning("SendGrid not configured, skipping email")
                return False
            
            html_content = self._create_custom_reminder_html(user, title, message)
            
            success = self._send_email(
                to_email=user.email,
                subject=title,
                html_content=html_content
            )
            
            if success:
                self._log_reminder_sent(user, db, reminder_type, title)
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending custom reminder: {str(e)}")
            return False
    
    def schedule_reminder(
        self,
        user: User,
        db: Session,
        title: str,
        message: str,
        scheduled_time: datetime,
        reminder_type: str = "exercise",
        is_recurring: bool = False,
        frequency: str = "once"
    ) -> Reminder:
        """
        Schedule a reminder to be sent later
        """
        reminder = Reminder(
            user_id=user.id,
            title=title,
            message=message,
            reminder_type=reminder_type,
            scheduled_time=scheduled_time,
            is_recurring=is_recurring,
            frequency=frequency,
            send_email=user.email_reminders_enabled
        )
        
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return reminder
    
    def process_scheduled_reminders(self, db: Session) -> int:
        """
        Process all scheduled reminders that are due
        """
        now = datetime.now()
        
        # Get due reminders
        due_reminders = db.query(Reminder).filter(
            Reminder.scheduled_time <= now,
            Reminder.is_sent == False,
            Reminder.is_active == True,
            Reminder.send_email == True
        ).all()
        
        sent_count = 0
        
        for reminder in due_reminders:
            try:
                user = db.query(User).filter(User.id == reminder.user_id).first()
                if not user or not user.is_active:
                    continue
                
                # Send the reminder
                if reminder.reminder_type == "exercise":
                    success = self.send_exercise_reminder(user, db, "scheduled")
                else:
                    success = self.send_custom_reminder(
                        user, db, reminder.title, reminder.message, reminder.reminder_type
                    )
                
                if success:
                    # Mark as sent
                    reminder.is_sent = True
                    reminder.sent_at = now
                    
                    # Handle recurring reminders
                    if reminder.is_recurring:
                        self._schedule_next_occurrence(reminder, db)
                    
                    sent_count += 1
                
            except Exception as e:
                logger.error(f"Error processing reminder {reminder.id}: {str(e)}")
        
        db.commit()
        return sent_count
    
    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """
        Send email using SendGrid
        """
        try:
            from_email = Email(settings.from_email)
            to_email = To(to_email)
            content = Content("text/html", html_content)
            
            mail = Mail(from_email, to_email, subject, content)
            
            response = self.sg.client.mail.send.post(request_body=mail.get())
            
            return response.status_code in [200, 202]
            
        except Exception as e:
            logger.error(f"SendGrid error: {str(e)}")
            return False
    
    def _get_user_current_exercises(self, user: User, db: Session) -> List[Dict]:
        """
        Get user's current assigned exercises
        """
        from app.models.exercise import UserExercise, Exercise
        
        user_exercises = db.query(UserExercise, Exercise).join(
            Exercise, UserExercise.exercise_id == Exercise.id
        ).filter(
            UserExercise.user_id == user.id,
            UserExercise.is_assigned == True
        ).limit(3).all()  # Limit to top 3 for email
        
        exercises = []
        for user_exercise, exercise in user_exercises:
            exercises.append({
                "name": exercise.name,
                "description": exercise.description,
                "duration": user_exercise.custom_duration or exercise.duration_minutes,
                "repetitions": user_exercise.custom_repetitions or exercise.repetitions
            })
        
        return exercises
    
    def _get_progress_summary_data(self, user: User, db: Session, period: str) -> Dict:
        """
        Get progress summary data for the specified period
        """
        from app.models.progress import Progress
        
        # Calculate date range
        now = datetime.now()
        if period == "weekly":
            start_date = now - timedelta(days=7)
        elif period == "monthly":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=7)
        
        # Get progress records
        progress_records = db.query(Progress).filter(
            Progress.user_id == user.id,
            Progress.session_date >= start_date
        ).all()
        
        if not progress_records:
            return {
                "total_sessions": 0,
                "period": period,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": now.strftime("%Y-%m-%d")
            }
        
        # Calculate metrics
        total_sessions = len(progress_records)
        total_duration = sum(p.duration_minutes for p in progress_records if p.duration_minutes)
        
        pain_before_values = [p.pain_level_before for p in progress_records if p.pain_level_before]
        pain_after_values = [p.pain_level_after for p in progress_records if p.pain_level_after]
        
        avg_pain_before = sum(pain_before_values) / len(pain_before_values) if pain_before_values else 0
        avg_pain_after = sum(pain_after_values) / len(pain_after_values) if pain_after_values else 0
        
        return {
            "total_sessions": total_sessions,
            "total_duration": total_duration,
            "avg_pain_before": round(avg_pain_before, 1),
            "avg_pain_after": round(avg_pain_after, 1),
            "pain_improvement": round(avg_pain_before - avg_pain_after, 1),
            "period": period,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": now.strftime("%Y-%m-%d")
        }
    
    def _get_reminder_subject(self, user: User, reminder_type: str) -> str:
        """
        Generate appropriate subject line for reminder
        """
        subjects = {
            "daily": f"Daily Exercise Reminder - {user.full_name}",
            "weekly": f"Weekly Exercise Check-in - {user.full_name}",
            "scheduled": f"Time for Your Arthritis Exercises - {user.full_name}",
            "motivation": f"Stay Strong, {user.full_name}!"
        }
        
        return subjects.get(reminder_type, f"Arthritis Care Reminder - {user.full_name}")
    
    def _create_reminder_email_html(
        self, 
        user: User, 
        motivational_message: str, 
        exercises: List[Dict],
        reminder_type: str
    ) -> str:
        """
        Create HTML content for exercise reminder email
        """
        exercises_html = ""
        if exercises:
            exercises_html = "<h3>Your Today's Exercises:</h3><ul>"
            for exercise in exercises:
                exercises_html += f"""
                <li>
                    <strong>{exercise['name']}</strong><br>
                    {exercise['description']}<br>
                    <em>Duration: {exercise['duration']} minutes, Repetitions: {exercise['repetitions']}</em>
                </li>
                """
            exercises_html += "</ul>"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Exercise Reminder</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9fafb; }}
                .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
                ul {{ padding-left: 20px; }}
                li {{ margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Agent Arthritis</h1>
                    <p>Your Personal Arthritis Care Assistant</p>
                </div>
                
                <div class="content">
                    <h2>Hello {user.full_name}!</h2>
                    
                    <p>{motivational_message}</p>
                    
                    {exercises_html}
                    
                    <p>Remember:</p>
                    <ul>
                        <li>Start slowly and listen to your body</li>
                        <li>Stop if you experience increased pain</li>
                        <li>Consistency is more important than intensity</li>
                        <li>Track your progress to see improvements</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="#" class="button">Log Your Exercise Session</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This email was sent by Agent Arthritis. If you no longer wish to receive these reminders, you can update your preferences in your account settings.</p>
                    <p>&copy; 2024 Agent Arthritis. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _create_progress_summary_html(
        self, 
        user: User, 
        progress_analysis: Dict, 
        progress_data: Dict,
        period: str
    ) -> str:
        """
        Create HTML content for progress summary email
        """
        recommendations_html = ""
        if progress_analysis.get("recommendations"):
            recommendations_html = "<h3>AI Recommendations:</h3><ul>"
            for rec in progress_analysis["recommendations"]:
                recommendations_html += f"<li>{rec}</li>"
            recommendations_html += "</ul>"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Progress Summary</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #059669; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9fafb; }}
                .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
                .stat-box {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #059669; }}
                .progress-indicator {{ display: inline-block; padding: 5px 10px; border-radius: 15px; color: white; font-size: 12px; }}
                .improving {{ background-color: #059669; }}
                .stable {{ background-color: #d97706; }}
                .declining {{ background-color: #dc2626; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Your {period.title()} Progress Summary</h1>
                    <p>Agent Arthritis Progress Report</p>
                </div>
                
                <div class="content">
                    <h2>Hello {user.full_name}!</h2>
                    
                    <p>{progress_analysis.get('motivational_message', 'Keep up the great work!')}</p>
                    
                    <div class="stat-box">
                        <h3>Your Progress Overview</h3>
                        <p><strong>Overall Progress:</strong> 
                            <span class="progress-indicator {progress_analysis.get('overall_progress', 'stable')}">
                                {progress_analysis.get('overall_progress', 'stable').title()}
                            </span>
                        </p>
                        <p><strong>Exercise Sessions:</strong> {progress_data.get('total_sessions', 0)}</p>
                        <p><strong>Total Exercise Time:</strong> {progress_data.get('total_duration', 0)} minutes</p>
                        <p><strong>Pain Level Improvement:</strong> {progress_data.get('pain_improvement', 0)} points</p>
                    </div>
                    
                    {recommendations_html}
                    
                    <p>Keep up the excellent work! Your consistency in managing your arthritis is making a real difference.</p>
                </div>
                
                <div class="footer">
                    <p>This summary covers the period from {progress_data.get('start_date')} to {progress_data.get('end_date')}.</p>
                    <p>&copy; 2024 Agent Arthritis. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _create_custom_reminder_html(self, user: User, title: str, message: str) -> str:
        """
        Create HTML content for custom reminder email
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #7c3aed; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9fafb; }}
                .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Agent Arthritis</h1>
                    <p>Personal Reminder</p>
                </div>
                
                <div class="content">
                    <h2>Hello {user.full_name}!</h2>
                    <h3>{title}</h3>
                    <p>{message}</p>
                </div>
                
                <div class="footer">
                    <p>&copy; 2024 Agent Arthritis. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _log_reminder_sent(
        self, 
        user: User, 
        db: Session, 
        reminder_type: str, 
        subject: str
    ):
        """
        Log that a reminder was sent
        """
        try:
            reminder = Reminder(
                user_id=user.id,
                title=subject,
                message=f"Automated {reminder_type} reminder sent",
                reminder_type=reminder_type,
                scheduled_time=datetime.now(),
                is_sent=True,
                sent_at=datetime.now(),
                send_email=True
            )
            
            db.add(reminder)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error logging reminder: {str(e)}")
    
    def _schedule_next_occurrence(self, reminder: Reminder, db: Session):
        """
        Schedule the next occurrence of a recurring reminder
        """
        try:
            next_time = None
            
            if reminder.frequency == "daily":
                next_time = reminder.scheduled_time + timedelta(days=1)
            elif reminder.frequency == "weekly":
                next_time = reminder.scheduled_time + timedelta(weeks=1)
            elif reminder.frequency == "monthly":
                next_time = reminder.scheduled_time + timedelta(days=30)
            
            if next_time:
                new_reminder = Reminder(
                    user_id=reminder.user_id,
                    title=reminder.title,
                    message=reminder.message,
                    reminder_type=reminder.reminder_type,
                    scheduled_time=next_time,
                    frequency=reminder.frequency,
                    is_recurring=True,
                    send_email=reminder.send_email,
                    ai_generated=reminder.ai_generated,
                    personalization_data=reminder.personalization_data
                )
                
                db.add(new_reminder)
                db.commit()
                
        except Exception as e:
            logger.error(f"Error scheduling next occurrence: {str(e)}")