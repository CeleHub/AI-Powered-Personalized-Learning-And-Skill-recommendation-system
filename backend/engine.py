import sqlite3
import os
import json
import datetime
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'database.db')
ELECTIVES_PATH = os.path.join(os.path.dirname(__file__), 'data', 'electives.json')
DATABASE_URL = os.getenv("DATABASE_URL")

# Dynamic SQL placeholders: %s for PostgreSQL, ? for SQLite
PLACEHOLDER = "%s" if DATABASE_URL else "?"

def get_db_connection():
    if DATABASE_URL:
        import psycopg2
        import psycopg2.extras
        # Use DictCursor to align with sqlite3.Row's key-value access style
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.DictCursor)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    if not DATABASE_URL:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            matric_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            career_goal TEXT NOT NULL,
            interests TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def validate_matric_number(matric: str) -> bool:
    """
    Validates that a matric number is exactly 11 digits and adheres to
    Mountain Top University's Computer Science department code layout:
    AA-BB-CC-DD-EEE where BB=01 (College), CC=03 (Department), DD=01 (Programme).
    """
    cleaned = matric.replace("-", "").strip()
    if len(cleaned) != 11 or not cleaned.isdigit():
        return False
    
    college = cleaned[2:4]
    dept = cleaned[4:6]
    prog = cleaned[6:8]
    return college == "01" and dept == "03" and prog == "01"

def calculate_level(matric: str) -> int:
    """
    Calculates current academic level from the year of admission (derived from matric AA...)
    based on the Mountain Top University academic calendar (September - August).
    """
    cleaned = matric.replace("-", "").strip()
    entry_year_suffix = int(cleaned[:2])
    entry_year = 2000 + entry_year_suffix
    
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    
    # Determine the start year of the current academic year
    # Academic calendar runs Sep to Aug, so Sep 2025 starts the 2025/2026 academic year.
    if current_month >= 9:
        current_academic_start = current_year
    else:
        current_academic_start = current_year - 1
        
    years_diff = current_academic_start - entry_year
    level = (years_diff + 1) * 100
    
    # Return level, clamping to normal undergrad range (100L - 400L)
    if level < 100:
        return 100
    return level

def register_student(name, matric_number, password, career_goal, interests):
    init_db()
    matric = matric_number.replace("-", "").strip()
    if not validate_matric_number(matric):
        return False, "Invalid MTU Computer Science Matric Number. Check that it is an 11-digit BSc. Computer Science code."
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    interests_str = ",".join([i.strip() for i in interests if i.strip()])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"INSERT INTO students (matric_number, name, password_hash, career_goal, interests) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
            (matric, name, password_hash, career_goal, interests_str)
        )
        conn.commit()
        return True, "Registration successful!"
    except Exception as e:
        # Check for duplicate key / integrity errors dynamically across databases
        err_msg = str(e).lower()
        if "unique" in err_msg or "duplicate" in err_msg:
            return False, "Matric number is already registered."
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()

def login_student(matric_number, password):
    init_db()
    matric = matric_number.replace("-", "").strip()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM students WHERE matric_number = {PLACEHOLDER} AND password_hash = {PLACEHOLDER}",
        (matric, password_hash)
    )
    student = cursor.fetchone()
    conn.close()
    if student:
        return {
            "matric_number": student["matric_number"],
            "name": student["name"],
            "career_goal": student["career_goal"],
            "interests": [i.strip() for i in student["interests"].split(",") if i.strip()]
        }
    return None

def load_electives():
    if not os.path.exists(ELECTIVES_PATH):
        return []
    with open(ELECTIVES_PATH, 'r') as f:
        return json.load(f)

def get_local_fallback_recommendations(level: int, career_goal: str, interests: list):
    """
    Ranks the level-appropriate electives locally based on overlap between course
    skills and the student's career goals/interests.
    """
    electives = load_electives()
    level_electives = [e for e in electives if e['level'] == level]
    
    keywords = [k.lower().strip() for k in interests if k.strip()]
    keywords.extend([w.lower().strip() for w in career_goal.split() if len(w) > 2])
    
    ranked = []
    for e in level_electives:
        score = 0
        title_lower = e['title'].lower()
        skills = [s.lower() for s in e['skills_covered']]
        
        # Check overlaps
        for kw in keywords:
            if kw in title_lower:
                score += 3
            for skill in skills:
                if kw in skill or skill in kw:
                    score += 2
                    
        # Formulate a custom justification based on the matched areas
        matched_areas = []
        for skill in e['skills_covered']:
            for kw in keywords:
                if kw in skill.lower() and skill not in matched_areas:
                    matched_areas.append(skill)
                    
        if matched_areas:
            justification = f"Directly supports your goal by covering key skills: {', '.join(matched_areas[:3])}."
        else:
            justification = f"Aligns with core Computer Science foundation requirements."
            
        ranked.append({
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
    ranked = sorted(ranked, key=lambda x: (-x['match_score'], x['code']))
    return ranked
