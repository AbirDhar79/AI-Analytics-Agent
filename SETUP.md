# Setup instructions (run app with .env + Streamlit permission)

Follow these steps so the app runs without entering the API key in the sidebar and without Streamlit permission errors.

---

## 0. Use the right dependencies (avoids "cannot import create_sql_agent" / 401)

This app was written for **LangChain 0.1.x**. If you install the full `requirements.txt` or upgrade packages, you can get **LangChain 1.x**, which moved APIs and breaks the original app code.

**Use the app-only pinned deps in a clean venv:**

```powershell
cd "D:\AI repo summerizer\Ai-sql-analytics-assistant-main"
python -m venv venv
.\venv\Scripts\pip install -r requirements-app.txt
```

Then add your Groq API key (step 2) and run the app (step 3). No app code changes are needed.

---

## 1. Give Streamlit permission (fix machine_id_v4 error)

Streamlit needs to write to a folder in your user profile. Create it and ensure it’s writable.

**In PowerShell (run as yourself, no admin needed):**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.streamlit"
```

If you still get “Permission denied”:

- Right-click the folder `C:\Users\Abir Dhar\.streamlit` (or your username) → **Properties** → **Security**
- Ensure your user has **Modify** or **Full control**. Use **Edit** to add it if needed.

---

## 2. Add your Groq API key in a `.env` file

The app reads `GROQ_API_KEY` from a `.env` file so you don’t have to type it in the sidebar.

**Steps:**

1. Get a Groq API key from **[console.groq.com](https://console.groq.com)** (free tier is fine).
2. In the project folder, copy the example env file:
   ```powershell
   cd "D:\AI repo summerizer\Ai-sql-analytics-assistant-main"
   Copy-Item .env.example .env
   ```
3. Open `.env` in Notepad or VS Code and replace the placeholder with your real key:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
   ```
   (No quotes, no spaces around `=`.)
4. Save the file.  
   **Important:** `.env` is in `.gitignore` so it won’t be committed to git.

---

## 3. Run the app

From the project folder:

```powershell
python -m streamlit run app.py
```

Or use the script:

```powershell
.\run-app.ps1
```

Open **http://localhost:8501** in your browser. The app will use the key from `.env`; you don’t need to type it in the sidebar. Select the SQLite option and start asking questions.

---

## Summary

| Step | What to do |
|------|------------|
| 1 | Create `%USERPROFILE%\.streamlit` (and fix permissions if needed). |
| 2 | Copy `.env.example` to `.env`, add your `GROQ_API_KEY`. |
| 3 | Run `python -m streamlit run app.py` (or `.\run-app.ps1`). |

No need to change any app code; the app already supports `GROQ_API_KEY` from `.env` and the sidebar is only used if the env var is not set.
