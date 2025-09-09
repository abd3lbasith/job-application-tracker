# db.py - super simple database helpers for the Job Application Tracker
import sqlite3
from contextlib import closing

DB_PATH = "job_tracker.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role_title TEXT NOT NULL,
    location TEXT,
    job_link TEXT,
    source TEXT,
    status TEXT,
    deadline TEXT,
    date_applied TEXT,
    follow_up_date TEXT,
    priority TEXT,
    recruiter_name TEXT,
    recruiter_email TEXT,
    notes TEXT,
    last_updated TEXT
);
"""

def get_conn():
    # You can change DB_PATH to another folder if needed
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with closing(get_conn()) as conn, conn:
        conn.executescript(SCHEMA)

def add_application(app):
    # app is a dict with keys matching column names (except id)
    keys = [k for k in app.keys() if k != "id"]
    cols = ",".join(keys)
    placeholders = ",".join([":" + k for k in keys])
    with closing(get_conn()) as conn, conn:
        conn.execute(f"INSERT INTO applications ({cols}) VALUES ({placeholders})", app)

def update_application(app_id, fields):
    # fields is a dict of columns to update
    set_clause = ",".join([f"{k} = :{k}" for k in fields.keys()])
    fields["id"] = app_id
    with closing(get_conn()) as conn, conn:
        conn.execute(f"UPDATE applications SET {set_clause} WHERE id = :id", fields)

def delete_application(app_id):
    with closing(get_conn()) as conn, conn:
        conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))

def list_applications(filters=None):
    # filters: dict with optional keys: status, search, source
    query = "SELECT * FROM applications"
    clauses = []
    params = []
    if filters:
        if filters.get("status"):
            clauses.append("status = ?")
            params.append(filters["status"])
        if filters.get("source"):
            clauses.append("source = ?")
            params.append(filters["source"])
        if filters.get("search"):
            # search in company or role_title
            clauses.append("(company LIKE ? OR role_title LIKE ?)")
            params.extend([f"%{filters['search']}%", f"%{filters['search']}%"])
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY last_updated DESC NULLS LAST, id DESC"
    with closing(get_conn()) as conn:
        cur = conn.execute(query, params)
        cols = [c[0] for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    return rows

def to_dataframe(filters=None):
    import pandas as pd
    rows = list_applications(filters)
    if not rows:
        return pd.DataFrame(columns=[
            "id","company","role_title","location","job_link","source","status",
            "deadline","date_applied","follow_up_date","priority","recruiter_name",
            "recruiter_email","notes","last_updated"
        ])
    return pd.DataFrame(rows)

def bulk_insert_from_dataframe(df):
    # expects columns similar to the table; missing columns will be filled with None
    expected = ["company","role_title","location","job_link","source","status","deadline",
                "date_applied","follow_up_date","priority","recruiter_name","recruiter_email",
                "notes","last_updated"]
    cleaned = []
    for _, row in df.iterrows():
        item = {k: (None if pd.isna(row.get(k)) else row.get(k)) for k in expected}
        cleaned.append(item)
    with closing(get_conn()) as conn, conn:
        conn.executemany(
            f"INSERT INTO applications ({','.join(expected)}) VALUES ({','.join(['?']*len(expected))})",
            [[item[k] for k in expected] for item in cleaned]
        )
