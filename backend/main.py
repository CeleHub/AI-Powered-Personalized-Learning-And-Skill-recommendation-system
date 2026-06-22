from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import os

from backend import gemini_util
from backend import engine

app = FastAPI(title="MTU Computer Science Elective Recommender API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class StudentSignup(BaseModel):
    name: str
    matric_number: str
    password: str
    career_goal: str
    interests: List[str]

class StudentLogin(BaseModel):
    matric_number: str
    password: str

class RecommendationRequest(BaseModel):
    matric_number: str
    career_goal: str
    interests: List[str]

@app.on_event("startup")
def startup_event():
    # Automatically initialize SQLite database on startup
    engine.init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the MTU Computer Science Elective Recommender API"}

@app.get("/health")
@app.head("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/signup")
async def signup(profile: StudentSignup):
    success, message = engine.register_student(
        name=profile.name,
        matric_number=profile.matric_number,
        password=profile.password,
        career_goal=profile.career_goal,
        interests=profile.interests
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@app.post("/login")
async def login(credentials: StudentLogin):
    student = engine.login_student(credentials.matric_number, credentials.password)
    if not student:
        raise HTTPException(status_code=401, detail="Invalid matric number or password.")
    return student

@app.post("/recommend")
async def get_recommendations(req: RecommendationRequest):
    try:
        # Validate matric
        matric = req.matric_number.replace("-", "").strip()
        if not engine.validate_matric_number(matric):
            raise HTTPException(status_code=400, detail="Invalid MTU Computer Science Matric Number.")
            
        # Calculate level
        level = engine.calculate_level(matric)
        
        # If level is 100, return empty electives with a special block message
        if level == 100:
            return {
                "level": 100,
                "message": "All courses are compulsory for 100 Level Computer Science students. Electives start at 200 Level.",
                "electives": [],
                "api_status": "local"
            }
            
        # Fetch level-specific electives
        all_electives = engine.load_electives()
        level_electives = [e for e in all_electives if e['level'] == level]
        
        if not level_electives:
            return {
                "level": level,
                "message": f"No electives found for {level} Level.",
                "electives": [],
                "api_status": "local"
            }
            
        api_status = "online"
        # Attempt Gemini ranking
        ranked_results = gemini_util.rank_electives_with_ai(level, level_electives, req.career_goal, req.interests)
        
        recommendations = []
        if ranked_results:
            # Map code to result
            rank_map = {res['code']: res for res in ranked_results if 'code' in res}
            for e in level_electives:
                code = e['code']
                if code in rank_map:
                    justification = rank_map[code].get('justification', "Matches your profile.")
                    score = rank_map[code].get('rank_score', 50)
                else:
                    justification = "Aligns with core Computer Science foundation requirements."
                    score = 0
                    
                recommendations.append({
                    "code": e['code'],
                    "title": e['title'],
                    "units": e['units'],
                    "level": e['level'],
                    "semester": e['semester'],
                    "skills": ", ".join(e['skills_covered']),
                    "match_score": score,
                    "justification": justification
                })
            # Sort by match score descending, then by course code ascending
            recommendations = sorted(recommendations, key=lambda x: (-x['match_score'], x['code']))
        else:
            # Fallback to local matching
            recommendations = engine.get_local_fallback_recommendations(level, req.career_goal, req.interests)
            api_status = "fallback"
            
        return {
            "level": level,
            "message": f"Recommended electives for {level} Level based on your profile.",
            "electives": recommendations,
            "api_status": api_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
