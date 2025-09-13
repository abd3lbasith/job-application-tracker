# Job Application Tracker
A simple web app to keep track of job applications.

## Features
- Add, edit, and delete applications
- Search and filter by company, role, or status
- Dashboard with application counts and upcoming deadlines
- Import and export data as CSV
- Built with Python, Streamlit, and SQLite

## Getting Started
### Run locally
1. Install Python 3.10+
2. Clone this repository and open a terminal in the project folder
3. Create and activate a virtual environment (optional but recommended)
4. Install dependencies:
pip install -r requirements.txt
5. Start the app:
6. Open your browser at `http://localhost:8501`

### Deploy
1. Push this project to a GitHub repository
2. Go to [Streamlit Community Cloud](https://share.streamlit.io)
3. Create a new app, connect your GitHub repo, select `app.py`, and deploy

## Project Structure
job-application-tracker/
├─ app.py # Streamlit app
├─ db.py # SQLite helper
├─ requirements.txt # Dependencies
└─ job_tracker.db # Created automatically when running

## About
This project was created to practice building a small full-stack application.  
It demonstrates working with a database, creating a Streamlit interface, and deploying a live app.
