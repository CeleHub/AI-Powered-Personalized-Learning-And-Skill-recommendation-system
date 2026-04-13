import pandas as pd
import json
import os

def load_courses():
    df = pd.read_csv('data/courses.csv')
    return df

def load_uni_requirements():
    with open('data/uni_requirements.json', 'r') as f:
        return json.load(f)

def get_difficulty_tier(profile: dict):
    """
    Determines the difficulty tier (Beginner, Intermediate, Advanced)
    based on GPA or O-Level performance.
    """
    perf = profile.get('academic_performance', {})
    
    if profile.get('academic_type') == 'UNIVERSITY/POST':
        gpa = float(perf.get('gpa', 0))
        if gpa >= 3.5:
            return ["Intermediate", "Advanced"]
        elif gpa >= 2.5:
            return ["Beginner", "Intermediate"]
        else:
            return ["Beginner"]
    else:
        # Pre-university O-level logic
        # Focus on Math and English grades
        math_grade = perf.get('subjects', {}).get('Mathematics', 'C6')
        english_grade = perf.get('subjects', {}).get('English', 'C6')
        
        # Mapping grades: A1=1, B2=2... C6=6, D7=7
        grade_map = {'A1': 1, 'B2': 2, 'B3': 3, 'C4': 4, 'C5': 5, 'C6': 6, 'D7': 7, 'E8': 8, 'F9': 9}
        m_val = grade_map.get(math_grade, 7)
        e_val = grade_map.get(english_grade, 7)
        
        if m_val <= 3 and e_val <= 3: # A1-B3
            return ["Beginner", "Intermediate"]
        else:
            return ["Beginner"]

def check_uni_eligibility(profile: dict, target_degree: str):
    """
    Checks if a pre-university user is eligible for a degree based on O-levels.
    """
    if profile.get('academic_type') != 'PRE_UNIVERSITY':
        return True, "Academic type is already University level."
        
    reqs = load_uni_requirements()
    if target_degree not in reqs:
        # If the exact degree isn't in our mapping, we look for a close match or return a general status
        return True, "No specific O-Level mapping for this degree yet. Consult a faculty advisor."
        
    user_subjects = profile.get('academic_performance', {}).get('subjects', {})
    degree_reqs = reqs[target_degree]
    
    # Check compulsory subjects (must be C6 or better)
    missing = []
    failed = []
    grade_map = {'A1': 1, 'B2': 2, 'B3': 3, 'C4': 4, 'C5': 5, 'C6': 6} # Credit passes
    
    for sub in degree_reqs['compulsory']:
        if sub not in user_subjects:
            missing.append(sub)
        elif user_subjects[sub] not in grade_map:
            failed.append(sub)
            
    if missing or failed:
        msg = ""
        if missing: msg += f"Missing compulsory subjects: {', '.join(missing)}. "
        if failed: msg += f"Need at least a C6 in: {', '.join(failed)}."
        return False, msg
        
    return True, f"Eligible for {target_degree} at Nigerian Universities."

def get_local_fallback_skills(career_goal: str):
    """
    Standardizes a career goal into skills using local keyword matching.
    Acts as a fail-safe for API limits.
    """
    goal = career_goal.lower()
    
    # Keyword mapping
    mapping = {
        "doctor": ["Anatomy", "Physiology", "Patient Assessment", "Internal Medicine", "Surgery", "Ethics", "Biology"],
        "nurse": ["Patient Care", "Medication Administration", "Anatomy", "Wound Care", "Nursing Ethics", "Clinical Research"],
        "lawyer": ["Litigation", "Legal Drafting", "Constitutional Law", "Contracts", "Legal Ethics", "English Common Law"],
        "accountant": ["Financial Reporting", "Audit", "Management Accounting", "Taxation", "ICAN Prep", "Bookkeeping"],
        "engineer": ["Mathematics", "Physics", "AutoCAD", "Structural Engineering", "Project Management", "COREN Ethics"],
        "architect": ["3D Design", "AutoCAD", "Urban Planning", "Building Codes", "Fine Arts", "Statics"],
        "teacher": ["Pedagogy", "Curriculum Design", "Classroom Management", "Educational Psychology", "Communication"],
        "artist": ["Fine Arts", "Graphic Design", "Illustration", "Color Theory", "Composition", "Digital Art"],
        "farmer": ["Crop Science", "Soil Management", "Agribusiness", "Livestock Management", "Sustainable Farming"],
        "data scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization", "Mathematics"],
        "web developer": ["HTML", "CSS", "JavaScript", "React", "NodeJS", "SQL", "Git"],
        "cyber": ["Network Security", "Linux", "Ethical Hacking", "Risk Management", "Cryptography"]
    }
    
    for key, skills in mapping.items():
        if key in goal:
            return skills
    
    # Universal Fallback if no keyword matches
    return ["Analytical Thinking", "Problem Solving", "Professional Ethics", "Communication", "Time Management", "Leadership"]

def recommend_courses(profile: dict, extracted_skills: list):
    """
    Main recommendation function.
    """
    df = load_courses()
    difficulty_tiers = get_difficulty_tier(profile)
    
    # Filter by difficulty
    filtered_df = df[df['difficulty'].isin(difficulty_tiers)]
    
    # Filter by user interests or extracted skills
    # We look for keyword matches in 'skills_covered' or 'category'
    recommendations = []
    
    for _, row in filtered_df.iterrows():
        course_skills = [s.strip().lower() for s in str(row['skills_covered']).split(",")]
        category = row['category'].lower()
        
        # Check if any extracted skill matches course skills or category
        match_count = 0
        for skill in extracted_skills:
            if skill.lower() in course_skills or skill.lower() in category:
                match_count += 1
                
        if match_count > 0:
            recommendations.append({
                "id": row['id'],
                "title": row['title'],
                "provider": row['provider'],
                "category": row['category'],
                "difficulty": row['difficulty'],
                "skills": row['skills_covered'],
                "duration": row['duration'],
                "match_score": match_count
            })
            
    # Sort by match score
    recommendations = sorted(recommendations, key=lambda x: x['match_score'], reverse=True)
    return recommendations[:10] # Return top 10
