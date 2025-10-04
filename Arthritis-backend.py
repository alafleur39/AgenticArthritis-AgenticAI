from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from openai import OpenAI
import os
import json
import re

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client (uses OPENAI_API_KEY env var)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client: Optional[OpenAI] = None
if OPENAI_API_KEY:
    client = OpenAI()

# In-memory storage (use Firebase/Supabase in production)
users_db = {}
sessions_db = []

# Models
class User(BaseModel):
    user_id: str
    name: str
    severity: str  # mild, moderate, severe
    affected_joints: List[str]

class GenerateExercisesRequest(BaseModel):
    user_id: str
    pain_level: int  # 1-10
    duration_minutes: Optional[int] = 10

class Exercise(BaseModel):
    name: str
    description: str
    duration_seconds: int
    reps: int
    target_joints: List[str]

class SessionLog(BaseModel):
    user_id: str
    exercises_completed: List[str]
    pain_before: int
    pain_after: int
    timestamp: Optional[str] = None


# Helpers
def _parse_json_array_from_text(text: str):
    """Attempt to parse a JSON array from arbitrary text.
    Handles code fences and stray commentary around the JSON.
    Returns a Python list on success, raises ValueError otherwise.
    """
    if text is None:
        raise ValueError("Empty response")
    s = text.strip()

    # Remove code fences if present
    if s.startswith("```"):
        parts = s.split("```")
        # take the first fenced content block if any
        if len(parts) >= 2:
            s = parts[1].strip()
            if s.lower().startswith("json"):
                s = s[4:].strip()

    # Quick path: try direct load
    try:
        obj = json.loads(s)
        if isinstance(obj, list):
            return obj
    except Exception:
        pass

    # Heuristic: extract the first bracketed JSON array region
    first_bracket = s.find("[")
    last_bracket = s.rfind("]")
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        candidate = s[first_bracket : last_bracket + 1]
        try:
            obj = json.loads(candidate)
            if isinstance(obj, list):
                return obj
        except Exception:
            pass

    # Try to fix common trailing commas using a simple regex (non-destructive)
    candidate = re.sub(r",\s*([\]}])", r"\1", s)
    try:
        obj = json.loads(candidate)
        if isinstance(obj, list):
            return obj
    except Exception:
        pass

    raise ValueError("Could not parse JSON array from model output")


def _mock_exercises(user: dict, pain_level: int, duration_minutes: int):
    """Fallback exercises when no API key is set."""
    joints = user.get("affected_joints", ["fingers"]) or ["fingers"]
    per_ex_duration = max(20, int((duration_minutes * 60) / 5))
    base = [
        {
            "name": "Warm Hand Open/Close",
            "description": "Gently open your hand wide, then make a soft fist. Repeat with smooth breathing.",
            "duration_seconds": per_ex_duration,
            "reps": 10,
            "target_joints": joints,
        },
        {
            "name": "Finger Walk",
            "description": "On a table, walk each finger forward and back without pain.",
            "duration_seconds": per_ex_duration,
            "reps": 8,
            "target_joints": joints,
        },
        {
            "name": "Thumb Opposition",
            "description": "Touch thumb to each fingertip slowly, then slide to the base.",
            "duration_seconds": per_ex_duration,
            "reps": 8,
            "target_joints": ["thumb"] + [j for j in joints if j != "thumb"],
        },
        {
            "name": "Wrist Flex/Extend",
            "description": "With forearm supported, gently bend wrist up and down within comfort.",
            "duration_seconds": per_ex_duration,
            "reps": 10,
            "target_joints": ["wrist"],
        },
        {
            "name": "Finger Spread/Pinch",
            "description": "Spread fingers apart, then bring them together with light pinch.",
            "duration_seconds": per_ex_duration,
            "reps": 10,
            "target_joints": joints,
        },
    ]
    # Lightly modulate reps by pain level (lower pain -> more reps, within gentle bounds)
    for ex in base:
        ex["reps"] = max(6, min(12, ex["reps"] - max(0, pain_level - 5)))
    return base

# Endpoints
@app.post("/api/users")
async def create_user(user: User):
    users_db[user.user_id] = user.dict()
    return {"message": "User created", "user": user}

@app.post("/api/generate-exercises")
async def generate_exercises(req: GenerateExercisesRequest):
    if req.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[req.user_id]
    
    # AI Prompt
    prompt = f"""Generate 5 hand exercises for arthritis patients.
    
Patient details:
- Severity: {user['severity']}
- Affected joints: {', '.join(user['affected_joints'])}
- Current pain level: {req.pain_level}/10
- Session duration: {req.duration_minutes} minutes

Return ONLY a JSON array with this exact format:
[
  {{
    "name": "Exercise name",
    "description": "Clear step-by-step instructions",
    "duration_seconds": 30,
    "reps": 10,
    "target_joints": ["fingers"]
  }}
]

Make exercises gentle, safe, and appropriate for their severity level."""

    try:
        if client is None:
            exercises = _mock_exercises(user, req.pain_level, req.duration_minutes or 10)
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a physical therapist specializing in arthritis. Return only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )

            content = response.choices[0].message.content if response.choices else ""
            exercises = _parse_json_array_from_text(content)

        return {
            "user_id": req.user_id,
            "exercises": exercises,
            "generated_at": datetime.now().isoformat(),
            "source": "mock" if client is None else "openai",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@app.post("/api/sessions")
async def log_session(session: SessionLog):
    session_data = session.dict()
    session_data["timestamp"] = datetime.now().isoformat()
    sessions_db.append(session_data)
    
    pain_reduction = session.pain_before - session.pain_after
    return {
        "message": "Session logged",
        "pain_reduction": pain_reduction,
        "session": session_data
    }

@app.get("/api/progress/{user_id}")
async def get_progress(user_id: str):
    user_sessions = [s for s in sessions_db if s["user_id"] == user_id]
    
    if not user_sessions:
        return {"user_id": user_id, "total_sessions": 0, "message": "No sessions yet"}
    
    # Calculate stats
    total_sessions = len(user_sessions)
    avg_pain_before = sum(s["pain_before"] for s in user_sessions) / total_sessions
    avg_pain_after = sum(s["pain_after"] for s in user_sessions) / total_sessions
    avg_reduction = avg_pain_before - avg_pain_after
    
    total_exercises = sum(len(s["exercises_completed"]) for s in user_sessions)
    
    # Recent trend (last 7 sessions)
    recent_sessions = sorted(user_sessions, key=lambda x: x["timestamp"], reverse=True)[:7]
    
    return {
        "user_id": user_id,
        "total_sessions": total_sessions,
        "total_exercises_completed": total_exercises,
        "average_pain_before": round(avg_pain_before, 1),
        "average_pain_after": round(avg_pain_after, 1),
        "average_pain_reduction": round(avg_reduction, 1),
        "recent_sessions": recent_sessions,
        "improvement_percentage": round((avg_reduction / avg_pain_before) * 100, 1) if avg_pain_before > 0 else 0
    }

@app.get("/")
async def root():
    return {
        "message": "Arthritis Exercise API",
        "endpoints": {
            "POST /api/users": "Create user",
            "POST /api/generate-exercises": "Generate AI exercises",
            "POST /api/sessions": "Log session",
            "GET /api/progress/{user_id}": "Get progress"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
