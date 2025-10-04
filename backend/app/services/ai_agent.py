import json
import openai
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.exercise import Exercise, UserExercise
from app.models.progress import Progress
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ArthritisAIAgent:
    """
    AI Agent for generating personalized arthritis exercises and providing insights
    """
    
    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        
    def generate_personalized_exercises(
        self, 
        user: User, 
        db: Session,
        count: int = 5
    ) -> List[Dict]:
        """
        Generate personalized exercises based on user profile and progress history
        """
        try:
            # Get user's progress history
            recent_progress = db.query(Progress).filter(
                Progress.user_id == user.id
            ).order_by(Progress.session_date.desc()).limit(10).all()
            
            # Build context for AI
            user_context = self._build_user_context(user, recent_progress)
            
            # Generate exercises using OpenAI
            exercises = self._generate_exercises_with_ai(user_context, count)
            
            return exercises
            
        except Exception as e:
            logger.error(f"Error generating personalized exercises: {str(e)}")
            # Fallback to default exercises
            return self._get_default_exercises(user, count)
    
    def analyze_progress_and_recommend(
        self, 
        user: User, 
        db: Session
    ) -> Dict:
        """
        Analyze user's progress and provide AI-powered recommendations
        """
        try:
            # Get comprehensive progress data
            progress_data = self._get_progress_analysis_data(user, db)
            
            # Generate AI insights
            insights = self._generate_progress_insights(progress_data)
            
            return {
                "overall_progress": insights.get("overall_progress", "stable"),
                "recommendations": insights.get("recommendations", []),
                "pain_trend": insights.get("pain_trend", "stable"),
                "exercise_adjustments": insights.get("exercise_adjustments", []),
                "motivational_message": insights.get("motivational_message", "Keep up the great work!")
            }
            
        except Exception as e:
            logger.error(f"Error analyzing progress: {str(e)}")
            return self._get_default_recommendations()
    
    def generate_motivational_message(
        self, 
        user: User, 
        db: Session,
        context: str = "daily"
    ) -> str:
        """
        Generate personalized motivational messages
        """
        try:
            # Get recent activity
            recent_activity = self._get_recent_activity(user, db)
            
            # Generate personalized message
            message = self._generate_ai_message(user, recent_activity, context)
            
            return message
            
        except Exception as e:
            logger.error(f"Error generating motivational message: {str(e)}")
            return self._get_default_motivational_message(user)
    
    def assess_exercise_difficulty(
        self, 
        user: User, 
        exercise: Exercise,
        recent_performance: List[Progress]
    ) -> Dict:
        """
        Assess if exercise difficulty should be adjusted based on performance
        """
        try:
            # Analyze performance data
            performance_metrics = self._analyze_performance_metrics(recent_performance)
            
            # Generate difficulty assessment
            assessment = self._generate_difficulty_assessment(
                user, exercise, performance_metrics
            )
            
            return assessment
            
        except Exception as e:
            logger.error(f"Error assessing exercise difficulty: {str(e)}")
            return {"adjustment": 0, "reason": "Unable to assess"}
    
    def _build_user_context(self, user: User, recent_progress: List[Progress]) -> Dict:
        """Build comprehensive user context for AI"""
        affected_joints = json.loads(user.affected_joints) if user.affected_joints else []
        
        # Calculate average pain levels
        avg_pain_before = 0
        avg_pain_after = 0
        if recent_progress:
            pain_before_values = [p.pain_level_before for p in recent_progress if p.pain_level_before]
            pain_after_values = [p.pain_level_after for p in recent_progress if p.pain_level_after]
            
            avg_pain_before = sum(pain_before_values) / len(pain_before_values) if pain_before_values else 0
            avg_pain_after = sum(pain_after_values) / len(pain_after_values) if pain_after_values else 0
        
        return {
            "age": user.age,
            "arthritis_type": user.arthritis_type,
            "severity_level": user.severity_level,
            "affected_joints": affected_joints,
            "medical_notes": user.medical_notes,
            "recent_sessions": len(recent_progress),
            "average_pain_before": avg_pain_before,
            "average_pain_after": avg_pain_after,
            "pain_improvement": avg_pain_before - avg_pain_after if avg_pain_before and avg_pain_after else 0
        }
    
    def _generate_exercises_with_ai(self, user_context: Dict, count: int) -> List[Dict]:
        """Generate exercises using OpenAI API"""
        if not settings.openai_api_key:
            return self._get_default_exercises_from_context(user_context, count)
        
        try:
            prompt = f"""
            Generate {count} personalized arthritis exercises for a patient with the following profile:
            - Age: {user_context.get('age', 'unknown')}
            - Arthritis Type: {user_context.get('arthritis_type', 'unknown')}
            - Severity Level: {user_context.get('severity_level', 'unknown')}/10
            - Affected Joints: {', '.join(user_context.get('affected_joints', []))}
            - Recent Pain Level (before exercises): {user_context.get('average_pain_before', 'unknown')}/10
            - Recent Pain Level (after exercises): {user_context.get('average_pain_after', 'unknown')}/10
            
            Please provide exercises in JSON format with the following structure:
            {{
                "name": "Exercise Name",
                "description": "Brief description",
                "instructions": ["Step 1", "Step 2", "Step 3"],
                "target_joints": ["joint1", "joint2"],
                "difficulty_level": 1-5,
                "duration_minutes": 5-15,
                "repetitions": 5-20,
                "category": "flexibility|strength|range_of_motion",
                "benefits": "Expected benefits",
                "precautions": "Safety precautions"
            }}
            
            Focus on exercises that are safe, effective, and appropriate for the patient's condition.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a specialized AI assistant for arthritis care, providing safe and effective exercise recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse the response
            content = response.choices[0].message.content
            exercises = json.loads(content)
            
            if isinstance(exercises, list):
                return exercises
            else:
                return [exercises]
                
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return self._get_default_exercises_from_context(user_context, count)
    
    def _generate_progress_insights(self, progress_data: Dict) -> Dict:
        """Generate AI insights from progress data"""
        if not settings.openai_api_key:
            return self._get_default_insights(progress_data)
        
        try:
            prompt = f"""
            Analyze the following arthritis patient progress data and provide insights:
            
            Progress Summary:
            - Total Sessions: {progress_data.get('total_sessions', 0)}
            - Average Pain Before: {progress_data.get('avg_pain_before', 0)}/10
            - Average Pain After: {progress_data.get('avg_pain_after', 0)}/10
            - Pain Improvement: {progress_data.get('pain_improvement', 0)}
            - Consistency Score: {progress_data.get('consistency_score', 0)}/10
            - Most Difficult Exercises: {progress_data.get('difficult_exercises', [])}
            - Most Effective Exercises: {progress_data.get('effective_exercises', [])}
            
            Provide analysis in JSON format:
            {{
                "overall_progress": "improving|stable|declining",
                "pain_trend": "improving|stable|worsening",
                "recommendations": ["recommendation1", "recommendation2"],
                "exercise_adjustments": [
                    {{"exercise": "name", "adjustment": "increase|decrease|maintain", "reason": "explanation"}}
                ],
                "motivational_message": "Personalized encouraging message"
            }}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI physiotherapy assistant specializing in arthritis care analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error generating AI insights: {str(e)}")
            return self._get_default_insights(progress_data)
    
    def _generate_ai_message(self, user: User, recent_activity: Dict, context: str) -> str:
        """Generate personalized motivational message"""
        if not settings.openai_api_key:
            return self._get_default_motivational_message(user)
        
        try:
            prompt = f"""
            Generate a personalized, encouraging message for an arthritis patient:
            
            Patient Info:
            - Name: {user.full_name}
            - Arthritis Type: {user.arthritis_type}
            - Recent Activity: {recent_activity.get('sessions_this_week', 0)} sessions this week
            - Last Session: {recent_activity.get('days_since_last_session', 'unknown')} days ago
            - Context: {context} message
            
            Create a warm, encouraging message (2-3 sentences) that:
            1. Acknowledges their effort or gently motivates if inactive
            2. Provides specific encouragement related to their condition
            3. Includes a positive, actionable suggestion
            
            Keep it personal, supportive, and medically appropriate.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a caring AI assistant providing encouragement to arthritis patients."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating AI message: {str(e)}")
            return self._get_default_motivational_message(user)
    
    def _get_progress_analysis_data(self, user: User, db: Session) -> Dict:
        """Get comprehensive progress data for analysis"""
        # Get last 30 days of progress
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        progress_records = db.query(Progress).filter(
            Progress.user_id == user.id,
            Progress.session_date >= thirty_days_ago
        ).all()
        
        if not progress_records:
            return {"total_sessions": 0}
        
        # Calculate metrics
        pain_before_values = [p.pain_level_before for p in progress_records if p.pain_level_before]
        pain_after_values = [p.pain_level_after for p in progress_records if p.pain_level_after]
        
        avg_pain_before = sum(pain_before_values) / len(pain_before_values) if pain_before_values else 0
        avg_pain_after = sum(pain_after_values) / len(pain_after_values) if pain_after_values else 0
        
        return {
            "total_sessions": len(progress_records),
            "avg_pain_before": round(avg_pain_before, 1),
            "avg_pain_after": round(avg_pain_after, 1),
            "pain_improvement": round(avg_pain_before - avg_pain_after, 1),
            "consistency_score": min(10, len(progress_records) / 3),  # Rough consistency metric
            "difficult_exercises": [],  # TODO: Implement based on difficulty ratings
            "effective_exercises": []   # TODO: Implement based on pain reduction
        }
    
    def _get_recent_activity(self, user: User, db: Session) -> Dict:
        """Get recent activity summary"""
        from datetime import datetime, timedelta
        
        week_ago = datetime.now() - timedelta(days=7)
        recent_sessions = db.query(Progress).filter(
            Progress.user_id == user.id,
            Progress.session_date >= week_ago
        ).count()
        
        last_session = db.query(Progress).filter(
            Progress.user_id == user.id
        ).order_by(Progress.session_date.desc()).first()
        
        days_since_last = 0
        if last_session:
            days_since_last = (datetime.now() - last_session.session_date).days
        
        return {
            "sessions_this_week": recent_sessions,
            "days_since_last_session": days_since_last
        }
    
    # Fallback methods for when AI is not available
    def _get_default_exercises(self, user: User, count: int) -> List[Dict]:
        """Default exercises when AI is not available"""
        default_exercises = [
            {
                "name": "Gentle Finger Stretches",
                "description": "Simple finger flexibility exercises",
                "instructions": [
                    "Make a fist with your hand",
                    "Slowly open your fingers wide",
                    "Hold for 5 seconds",
                    "Repeat 10 times"
                ],
                "target_joints": ["fingers", "wrists"],
                "difficulty_level": 1,
                "duration_minutes": 5,
                "repetitions": 10,
                "category": "flexibility"
            },
            {
                "name": "Wrist Circles",
                "description": "Improve wrist mobility and reduce stiffness",
                "instructions": [
                    "Extend your arm forward",
                    "Make slow circles with your wrist",
                    "Do 10 circles clockwise",
                    "Do 10 circles counterclockwise"
                ],
                "target_joints": ["wrists"],
                "difficulty_level": 1,
                "duration_minutes": 3,
                "repetitions": 20,
                "category": "range_of_motion"
            },
            {
                "name": "Shoulder Rolls",
                "description": "Gentle shoulder mobility exercise",
                "instructions": [
                    "Sit or stand comfortably",
                    "Roll shoulders forward 10 times",
                    "Roll shoulders backward 10 times",
                    "Keep movements slow and controlled"
                ],
                "target_joints": ["shoulders"],
                "difficulty_level": 1,
                "duration_minutes": 3,
                "repetitions": 20,
                "category": "range_of_motion"
            }
        ]
        
        return default_exercises[:count]
    
    def _get_default_exercises_from_context(self, user_context: Dict, count: int) -> List[Dict]:
        """Get default exercises based on user context"""
        return self._get_default_exercises(None, count)
    
    def _get_default_recommendations(self) -> Dict:
        """Default recommendations when AI is not available"""
        return {
            "overall_progress": "stable",
            "recommendations": [
                "Continue with your current exercise routine",
                "Focus on consistency over intensity",
                "Listen to your body and rest when needed"
            ],
            "pain_trend": "stable",
            "exercise_adjustments": [],
            "motivational_message": "You're doing great! Keep up the consistent effort."
        }
    
    def _get_default_insights(self, progress_data: Dict) -> Dict:
        """Default insights when AI is not available"""
        sessions = progress_data.get('total_sessions', 0)
        pain_improvement = progress_data.get('pain_improvement', 0)
        
        if sessions == 0:
            progress_status = "stable"
            message = "Start your exercise journey today!"
        elif pain_improvement > 0.5:
            progress_status = "improving"
            message = "Great progress! Your pain levels are improving."
        elif pain_improvement < -0.5:
            progress_status = "declining"
            message = "Let's focus on gentle exercises and consistency."
        else:
            progress_status = "stable"
            message = "You're maintaining good consistency. Keep it up!"
        
        return {
            "overall_progress": progress_status,
            "pain_trend": "improving" if pain_improvement > 0 else "stable",
            "recommendations": [
                "Maintain regular exercise schedule",
                "Track your pain levels consistently",
                "Consult with your healthcare provider regularly"
            ],
            "exercise_adjustments": [],
            "motivational_message": message
        }
    
    def _get_default_motivational_message(self, user: User) -> str:
        """Default motivational message"""
        messages = [
            f"Hello {user.full_name}! Remember, every small step counts in managing your arthritis.",
            f"Hi {user.full_name}! Your consistency with exercises makes a real difference.",
            f"Good day {user.full_name}! Take a moment today to care for your joints with gentle movement.",
            f"Hello {user.full_name}! Your dedication to managing arthritis is inspiring."
        ]
        
        import random
        return random.choice(messages)