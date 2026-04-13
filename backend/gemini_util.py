import os
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load all keys as a list
API_KEYS_RAW = os.getenv("GEMINI_API_KEYS", "")
API_KEYS = [k.strip() for k in API_KEYS_RAW.split(",") if k.strip()]
current_key_index = 0

def configure_genai():
    """Configures the Gemini SDK with the current active key."""
    if not API_KEYS:
        return False
    global current_key_index
    genai.configure(api_key=API_KEYS[current_key_index])
    return True

# Initial configuration
configure_genai()

def rotate_key():
    """Switches to the next API key in the rotation pool."""
    global current_key_index
    if len(API_KEYS) <= 1:
        return False
    
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    print(f"🔄 Rotating to next API key (Index: {current_key_index})")
    return configure_genai()

def extract_required_skills(career_goal: str):
    """
    Extracts skills with automatic key rotation on quota limits.
    """
    if not API_KEYS:
        return ["Analytical Thinking", "Problem Solving", "Professional Ethics"]

    max_retries = len(API_KEYS)
    attempts = 0

    while attempts < max_retries:
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
        except exceptions.ResourceExhausted:
            print(f"⚠️ Quota exhausted for key {current_key_index + 1}.")
            if not rotate_key(): break
            attempts += 1
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return ["Analytical Thinking", "Problem Solving", "Professional Ethics", "Communication", "Time Management", "Leadership"]
    
    return ["Analytical Thinking", "Problem Solving", "Professional Ethics", "Communication", "Time Management", "Leadership"]

def suggest_university_course(career_goal: str, academic_performance: dict):
    """
    Suggests a university degree with automatic key rotation.
    """
    if not API_KEYS:
        return "General Studies academic path"

    max_retries = len(API_KEYS)
    attempts = 0

    while attempts < max_retries:
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
        except exceptions.ResourceExhausted:
            print(f"⚠️ Quota exhausted for key {current_key_index + 1}.")
            if not rotate_key(): break
            attempts += 1
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "General Studies academic path"
    
    return "General Studies academic path"
