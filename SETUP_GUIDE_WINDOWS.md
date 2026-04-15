# 🪟 Windows Setup Guide

This guide will help you set up and run the **AI Course Recommender** on a fresh Windows PC after downloading it as a ZIP file.

---

## 🛠️ Step 1: Install Python
1.  Go to [python.org](https://www.python.org/downloads/).
2.  Click the **Download Python** button.
3.  **IMPORTANT:** When running the installer, make sure to check the box that says **"Add Python to PATH"** before clicking "Install Now".
4.  Once finished, open **Command Prompt** (cmd) and type:
    ```cmd
    python --version
    ```
    If it shows Python 3.x, you are ready!

---

## 📂 Step 2: Extract the Project
1.  Right-click the downloaded ZIP file.
2.  Select **Extract All...** and choose a folder (e.g., your Desktop).
3.  Open the extracted folder.

---

## 🧠 Step 3: Setup the Backend
1.  Open the project folder.
2.  Hold **Shift** and **Right-Click** in an empty space inside the folder.
3.  Select **Open PowerShell window here** or **Open in Terminal**.
4.  Type the following commands:

    ```powershell
    # 1. Create a virtual environment (keeps your PC clean)
    python -m venv venv

    # 2. Activate the virtual environment
    .\venv\Scripts\activate

    # 3. Install the required libraries
    pip install -r backend/requirements.txt
    ```

5.  Create your API Key file:
    - Right-click in the folder and select **New > Text Document**.
    - Rename it to `.env` (make sure it's not `.env.txt`).
    - Open it with Notepad and add:
      ```text
      GEMINI_API_KEYS=your_actual_key_here
      ```

6.  **Run the Backend:**
    ```powershell
    python -m backend.main
    ```
    You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`.

---

## 🎨 Step 4: Run the Frontend
1.  Keep the Backend window running!
2.  Open another folder window and navigate to the `frontend` directory.
3.  Double-click `index.html`. It will open in your default browser (Chrome/Edge/Firefox).
4.  **Note:** For the best experience (and to avoid CORS issues in some browsers), we recommend opening the folder in **VS Code** and using the **"Live Server"** extension.

---

## 🔌 Troubleshooting (Windows specific)
- **"Execution of scripts is disabled..."**: If you see this error when activating the venv, run this command in PowerShell as Administrator:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Port 8000 Busy**: If the backend says the port is in use, close any other Python windows or restart your PC.
- **Python not found**: If `python` doesn't work, try typing `py` or `python3`.
