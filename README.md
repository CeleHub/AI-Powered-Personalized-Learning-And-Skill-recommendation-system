# AI-Powered Personalized Learning & Skill Recommendation System 🎓

An intelligent, high-fidelity platform designed to bridge the gap between career aspirations and educational pathways. This system uses Large Language Models (LLMs) to map complex career goals into precise learning roadmaps while aligning academic performance with Nigerian university standards.

---

## ✨ Features
- **AI Career Mapping:** Translates unstructured career goals (e.g., "I want to be a Lead AI Researcher") into a structured 10-point skill roadmap using Gemini 1.5 Pro/Flash.
- **Academic Tiering:** Automatically scales course recommendations based on user performance (GPA or O-Level grades) to ensure a personalized learning curve.
- **Nigerian University Pathway:** Checks eligibility for Nigerian degree programs based on NUC-aligned O-Level subject requirements.
- **"Steve Jobs Approved" UI:** A premium, obsidian-themed dashboard featuring glassmorphism, fluid animations, and a responsive Bento-Box layout.
- **Hybrid Intelligence:** Features a local fallback engine to ensure functionality even when AI services are offline or exhausted.

---

## 🏗️ Project Structure

```text
├── backend/            # FastAPI Backend (Python)
│   ├── main.py         # API Gateway & Endpoints
│   ├── engine.py       # Recommendation Logic & Academic Tiering
│   └── gemini_util.py  # AI Integration & Key Rotation
├── frontend/           # Vanilla JS/CSS Frontend
│   ├── index.html      # Glassmorphic UI Structure
│   ├── app.js          # State Management & Results Rendering
│   └── style.css       # Obsidian Dark Theme System
├── data/               # Knowledge Base
│   ├── courses.csv     # 50+ Curated Learning Paths
│   └── uni_requirements.json # Nigerian Academic Mapping
├── docs/               # System Documentation
└── SETUP_GUIDE_WINDOWS.md # Setup instructions for Windows users
```

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.9+
- A Google Gemini API Key

### 1. Backend Setup
1. Navigate to the backend folder.
2. Create a `.env` file and add your key: `GEMINI_API_KEYS=your_key_here`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the server: `python3 -m backend.main`.

### 2. Frontend Setup
Simply open `frontend/index.html` in your browser, or use a "Live Server" extension in VS Code for the best experience.

---

## 🛡️ Hybrid Engine Logic
The system employs a "Dual-Layer Processing" model:
1. **Layer 1 (AI):** Real-time extraction of specific technical and soft skills.
2. **Layer 2 (Local):** Fallback to a hardcoded domain mapping of 15+ professional fields (Law, Medicine, Engineering, etc.) to ensure 100% uptime.

---

## 📜 License
Independent Project for Academic/Professional Portfolio.
Developed with a "Steve Jobs Approved" standard for excellence.
