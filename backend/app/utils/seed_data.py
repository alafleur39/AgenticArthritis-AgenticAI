"""
Seed data for the Agent Arthritis application
"""
import json
from sqlalchemy.orm import Session
from app.models.exercise import Exercise
from app.db.database import SessionLocal


def create_default_exercises():
    """Create default exercises in the database"""
    
    default_exercises = [
        {
            "name": "Gentle Finger Stretches",
            "description": "Simple finger flexibility exercises to reduce stiffness and improve range of motion",
            "instructions": json.dumps([
                "Sit comfortably with your hands resting on a table",
                "Make a gentle fist with your hand",
                "Slowly open your fingers wide, spreading them apart",
                "Hold the stretch for 5 seconds",
                "Relax and repeat 10 times",
                "Switch to the other hand"
            ]),
            "target_joints": json.dumps(["fingers", "knuckles"]),
            "difficulty_level": 1,
            "duration_minutes": 5,
            "repetitions": 10,
            "category": "flexibility",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Wrist Circles",
            "description": "Improve wrist mobility and reduce stiffness with gentle circular movements",
            "instructions": json.dumps([
                "Extend your arm forward at shoulder height",
                "Keep your elbow straight and hand relaxed",
                "Make slow, gentle circles with your wrist",
                "Complete 10 circles in one direction",
                "Reverse direction and complete 10 more circles",
                "Repeat with the other wrist"
            ]),
            "target_joints": json.dumps(["wrists"]),
            "difficulty_level": 1,
            "duration_minutes": 3,
            "repetitions": 20,
            "category": "range_of_motion",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Shoulder Rolls",
            "description": "Gentle shoulder mobility exercise to reduce tension and improve flexibility",
            "instructions": json.dumps([
                "Sit or stand with your arms at your sides",
                "Slowly roll your shoulders forward in a circular motion",
                "Complete 10 forward rolls",
                "Reverse direction and roll shoulders backward 10 times",
                "Keep movements slow and controlled",
                "Focus on relaxing your neck and shoulders"
            ]),
            "target_joints": json.dumps(["shoulders"]),
            "difficulty_level": 1,
            "duration_minutes": 3,
            "repetitions": 20,
            "category": "range_of_motion",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Ankle Pumps",
            "description": "Simple ankle exercises to improve circulation and reduce stiffness",
            "instructions": json.dumps([
                "Sit in a chair with your feet flat on the floor",
                "Lift one foot slightly off the ground",
                "Point your toes away from you, then flex them back toward you",
                "Repeat this pumping motion 15 times",
                "Switch to the other foot",
                "You can also do both feet at the same time"
            ]),
            "target_joints": json.dumps(["ankles"]),
            "difficulty_level": 1,
            "duration_minutes": 4,
            "repetitions": 15,
            "category": "flexibility",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Neck Stretches",
            "description": "Gentle neck stretches to relieve tension and improve mobility",
            "instructions": json.dumps([
                "Sit up straight with shoulders relaxed",
                "Slowly turn your head to the right, hold for 5 seconds",
                "Return to center, then turn left, hold for 5 seconds",
                "Tilt your head toward your right shoulder, hold for 5 seconds",
                "Return to center, then tilt left, hold for 5 seconds",
                "Repeat the sequence 3 times"
            ]),
            "target_joints": json.dumps(["neck", "cervical spine"]),
            "difficulty_level": 1,
            "duration_minutes": 5,
            "repetitions": 3,
            "category": "flexibility",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Gentle Knee Bends",
            "description": "Seated knee exercises to maintain joint mobility and strength",
            "instructions": json.dumps([
                "Sit in a sturdy chair with your back straight",
                "Slowly straighten one leg in front of you",
                "Hold for 2 seconds, then slowly lower",
                "Repeat 10 times with one leg",
                "Switch to the other leg",
                "Keep movements slow and controlled"
            ]),
            "target_joints": json.dumps(["knees"]),
            "difficulty_level": 2,
            "duration_minutes": 6,
            "repetitions": 10,
            "category": "strength",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Hand Squeezes",
            "description": "Strengthen hand and finger muscles with gentle squeezing exercises",
            "instructions": json.dumps([
                "Hold a soft stress ball or rolled-up towel",
                "Squeeze gently with your whole hand",
                "Hold the squeeze for 3 seconds",
                "Slowly release and relax",
                "Repeat 10 times with one hand",
                "Switch to the other hand"
            ]),
            "target_joints": json.dumps(["hands", "fingers"]),
            "difficulty_level": 2,
            "duration_minutes": 4,
            "repetitions": 10,
            "category": "strength",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Hip Circles",
            "description": "Gentle hip mobility exercise to maintain range of motion",
            "instructions": json.dumps([
                "Stand behind a chair, holding the back for support",
                "Lift one leg slightly to the side",
                "Make small circles with your leg",
                "Complete 5 circles in each direction",
                "Lower your leg and repeat with the other side",
                "Keep movements small and controlled"
            ]),
            "target_joints": json.dumps(["hips"]),
            "difficulty_level": 2,
            "duration_minutes": 5,
            "repetitions": 10,
            "category": "range_of_motion",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Seated Spinal Twist",
            "description": "Gentle spinal mobility exercise to reduce back stiffness",
            "instructions": json.dumps([
                "Sit tall in a chair with feet flat on the floor",
                "Place your right hand on your left knee",
                "Slowly twist your torso to the left",
                "Hold for 10 seconds, breathing normally",
                "Return to center and repeat on the other side",
                "Keep your hips facing forward throughout"
            ]),
            "target_joints": json.dumps(["spine", "lower back"]),
            "difficulty_level": 2,
            "duration_minutes": 4,
            "repetitions": 5,
            "category": "flexibility",
            "video_url": None,
            "image_url": None
        },
        {
            "name": "Calf Raises",
            "description": "Strengthen calf muscles and improve ankle stability",
            "instructions": json.dumps([
                "Stand behind a chair, holding the back for support",
                "Rise up onto your toes, lifting your heels",
                "Hold for 2 seconds at the top",
                "Slowly lower your heels back down",
                "Repeat 10-15 times",
                "Focus on controlled movements"
            ]),
            "target_joints": json.dumps(["ankles", "calves"]),
            "difficulty_level": 2,
            "duration_minutes": 3,
            "repetitions": 15,
            "category": "strength",
            "video_url": None,
            "image_url": None
        }
    ]
    
    db = SessionLocal()
    try:
        # Check if exercises already exist
        existing_count = db.query(Exercise).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} exercises. Skipping seed data.")
            return
        
        # Create exercises
        for exercise_data in default_exercises:
            exercise = Exercise(**exercise_data)
            db.add(exercise)
        
        db.commit()
        print(f"Successfully created {len(default_exercises)} default exercises")
        
    except Exception as e:
        print(f"Error creating default exercises: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_default_exercises()