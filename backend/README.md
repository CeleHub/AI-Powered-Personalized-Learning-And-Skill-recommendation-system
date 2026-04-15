# AI Recommendation Engine | Backend 🧠

A high-performance FastAPI service that acts as the "intelligence layer" for the Personalized Learning System.

---

## 🛠️ Core Stack
- **Framework:** FastAPI (Python)
- **AI Platform:** Google Gemini (Generative AI SDK)
- **Data Engine:** Pandas (Optimized CSV processing)
- **Security:** Python Dotenv

---

## 🚀 Key Modules
1. **`main.py`**: Handles incoming HTTP requests and coordinates between the AI and the Local Engine.
2. **`gemini_util.py`**:
    - **Skill Extraction:** Converts career goals into structured skill sets.
    - **Key Rotation:** Automatically cycles through multiple API keys if quota limits (429 errors) are reached.
3. **`engine.py`**:
    - **Academic Logic:** Maps Nigerian O-level grades and GPAs to performance tiers.
    - **Recommendation Logic:** Weights and ranks courses based on skill matches.
    - **Eligibility Engine:** Checks if a user can apply for a specific Nigerian degree program.

---

## 🔧 Installation & Usage

### 1. Requirements
Ensure you have Python 3.9+ installed.

### 2. Environment Variables
Create a `.env` file in this directory:
```env
GEMINI_API_KEYS=key1,key2,key3
```

### 3. Run Locally
```bash
pip install -r requirements.txt
python3 -m backend.main
```

### 4. API Endpoints
- `GET /`: Root check.
- `GET /health`: Health check (returns 200).
- `POST /recommend`: Main endpoint for generating roadmaps.

---

## 🛡️ Fallback System
The backend is designed for resilience. If the Gemini API fails, it switches to a local keyword-matching engine that covers 15+ professional domains including:
- Medicine & Healthcare
- Law & Jurisprudence
- Engineering & Construction
- Business & Accounting
- Architecture & Design
- Agriculture & Environment
