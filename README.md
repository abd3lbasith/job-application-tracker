# 🗂️ Job Application Tracker (Streamlit)

A super simple web app to track your job search.

## ⭐ What you’ll learn / show on your resume
- Build a small **web app** using **Python** + **Streamlit**
- **CRUD**: Create, Read, Update, Delete records
- Store data in **SQLite**
- Make a simple **dashboard** and **download CSV**
- Deploy to the web (free) with **Streamlit Community Cloud**

## 🧱 Project structure
```
job-application-tracker/
  ├─ app.py                # Streamlit UI
  ├─ db.py                 # simple SQLite helpers
  ├─ job_tracker.db        # created automatically on first run
  ├─ requirements.txt      # libraries
  └─ .streamlit/config.toml# theme (optional)
```

## ▶️ Run locally (no experience needed)
1) Install Python 3.10+
2) Open a terminal in this folder and run:
```
pip install -r requirements.txt
streamlit run app.py
```
3) Your browser will open at `http://localhost:8501`

## 🚀 Deploy (so others can see it)
1) Create a **GitHub repo** and upload these files
2) Go to **share.streamlit.io** and click **New app**
3) Connect your GitHub repo and pick `app.py`
4) Click **Deploy** — done!

## 📝 Features
- Add applications (company, role, status, links, dates, notes)
- View, filter, search, **edit** and **delete**
- Dashboard with status counts, upcoming deadlines, follow-ups due today
- Follow-up email **template generator**
- Import from CSV and export your data

## 💡 Suggested README snippet for your resume/portfolio
> Built a full-stack job application tracker with Python/Streamlit and SQLite. Implemented CRUD, status filters, deadline reminders, CSV import/export, and a dashboard. Deployed to Streamlit Cloud for public access.

## 🧪 Optional seed data
In the app, use the **Add** tab to create your first entries. You can also prepare a CSV and import it from the **Import/Export** tab.
