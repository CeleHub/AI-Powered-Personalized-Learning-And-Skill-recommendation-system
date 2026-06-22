import os
import json
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

def rank_electives_with_ai(level: int, electives: list, career_goal: str, interests: list):
    """
    Ranks electives using Gemini 1.5 Flash based on student's career goals and interests.
    """
    if not API_KEYS:
        return None

    # Format the electives list for the prompt
    electives_str = ""
    for e in electives:
        electives_str += f"- Code: {e['code']}, Title: {e['title']}, Units: {e['units']}, Semester: {e['semester']}, Skills Covered: {', '.join(e['skills_covered'])}\n"

    max_retries = len(API_KEYS)
    attempts = 0

    while attempts < max_retries:
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"""
            You are an expert academic advisor in Computer Science at Mountain Top University.
            A student is in {level} Level. Their career goal is "{career_goal}" and their interests are {interests}.
            We need to rank the following elective courses for this level in order of relevance:
            {electives_str}
            
            Rank all of them. Provide a short justification (max 12 words) for each, explaining its relevance to their specific career goal and interests.
            Return the result ONLY as a JSON list of objects, with no markdown, no ```json formatting, no other text.
            Each object in the JSON list MUST have exactly these keys:
            - "code": the exact course code (e.g., "CSC 417")
            - "justification": the short justification string
            - "rank_score": an integer score from 0 to 100 representing relevance
            
            Example output format:
            [
              {{"code": "CSC 417", "justification": "Directly covers mobile application development which is core to your goal.", "rank_score": 95}}
            ]
            """
            response = model.generate_content(prompt)
            # Try to parse the response as JSON
            cleaned_text = response.text.strip()
            # Strip markdown formatting if Gemini returned it despite instructions
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            ranked_data = json.loads(cleaned_text)
            return ranked_data
        except exceptions.ResourceExhausted:
            print(f"⚠️ Quota exhausted for key {current_key_index + 1}.")
            if not rotate_key(): break
            attempts += 1
        except Exception as e:
            print(f"Error calling Gemini API for ranking: {e}")
            return None
            
    return None
