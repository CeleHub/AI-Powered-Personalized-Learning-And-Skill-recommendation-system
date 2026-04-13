from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

from backend import gemini_util
from backend import engine

app = FastAPI(title="AI-Powered Course Recommendation System")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserProfile(BaseModel):
    name: str
    academic_type: str # PRE_UNIVERSITY or UNIVERSITY/POST
    academic_performance: Dict
    interests: List[str]
    career_goal: str
    skills: List[Dict] # {name: str, level: str}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Recommendation API"}

@app.get("/health")
@app.head("/health")
def health_check():
    """Endpoint for UptimeRobot to keep the service alive."""
    return {"status": "healthy"}

@app.post("/recommend")
async def get_recommendations(profile: UserProfile):
    try:
        # 1. Extract skills from career goal using AI
        extracted_skills = gemini_util.extract_required_skills(profile.career_goal)
        
        # 2. Suggest a university course if pre-university
        uni_suggestion = ""
        eligibility_status = {"eligible": True, "message": ""}
        
        if profile.academic_type == "PRE_UNIVERSITY":
            uni_suggestion = gemini_util.suggest_university_course(profile.career_goal, profile.academic_performance)
            eligible, msg = engine.check_uni_eligibility(profile.dict(), uni_suggestion)
            eligibility_status = {"eligible": eligible, "message": msg}
        
        # 3. Get course recommendations
        recommendations = engine.recommend_courses(profile.dict(), extracted_skills)
        
        return {
            "user_name": profile.name,
            "target_skills": extracted_skills,
            "university_recommendation": uni_suggestion,
            "eligibility": eligibility_status,
            "course_recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Use environment variable for port, defaulting to 8000 for local development
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
