import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY not found in .env file. AI features will be disabled.")
else:
    genai.configure(api_key=API_KEY)

def extract_required_skills(career_goal: str):
    """
    Uses Gemini AI to extract a list of standardized industry skills 
    required for a given career goal.
    """
    if not API_KEY:
        return ["Problem Solving", "Communication", "Time Management"] # Default fallback

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Given the career goal: "{career_goal}", 
        provide a comma-separated list of the top 10 specialized technical, domain-specific, and soft skills required to succeed in this role.
        Format the output ONLY as a comma-separated string, no extra text.
        Example for a Nurse: "Patient Assessment, Medication Administration, Wound Care, Anatomy, Ethics, Communication"
        Example for a Data Scientist: "Python, SQL, Statistics, Machine Learning, Data Visualization"
        """
        response = model.generate_content(prompt)
        skills = [s.strip() for s in response.text.split(",")]
        return skills
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return ["Analytical Thinking", "Problem Solving", "Professional Ethics", "Communication", "Time Management", "Leadership"]

def suggest_university_course(career_goal: str, academic_performance: dict):
    """
    Suggests a university degree based on career goal and academic background.
    """
    if not API_KEY:
        return "Computer Science" # Default fallback

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        A user wants to become a "{career_goal}". 
        Their academic performance is: {academic_performance}.
        Based on the Nigerian university system (NUC guidelines), what is the single most relevant undergraduate degree they should study?
        Provide ONLY the degree name. If it's a professional path (like Law or Medicine), state the degree (e.g., 'Law', 'Medicine and Surgery', 'Nursing Science').
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "General Studies academic path"
