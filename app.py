# app.py - Job Application Tracker (beginner friendly)
# Run locally:   streamlit run app.py
# Deps: see requirements.txt

import datetime as dt
import pandas as pd
import streamlit as st
from db import init_db, add_application, list_applications, to_dataframe, update_application, delete_application

st.set_page_config(page_title="Job Application Tracker", page_icon="🗂️", layout="wide")

# ---------- Constants (dropdown choices) ----------
STATUS_OPTIONS = [
    "Wishlist",
    "Draft",
    "Applied",
    "Online Assessment",
    "Phone Screen",
    "Interview",
    "Onsite/Final",
    "Offer",
    "Rejected",
    "Ghosted",
    "Paused",
]

SOURCE_OPTIONS = [
    "Company Site",
    "LinkedIn",
    "Indeed",
    "Internal Portal",
    "Referral",
    "Career Fair",
    "Other",
]

PRIORITY_OPTIONS = ["High", "Medium", "Low"]

# ---------- Setup ----------
init_db()

st.title("🗂️ Job Application Tracker")
st.write("A simple, no-stress tracker you can **run** and **deploy**. ")

tabs = st.tabs(["➕ Add", "📋 View & Edit", "📊 Dashboard", "✉️ Templates", "⬇️ Import/Export"])

# ---------- Tab: Add ----------
with tabs[0]:
    st.subheader("Add a new application")
    with st.form("add_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        company     = col1.text_input("Company*", placeholder="Google")
        role_title  = col2.text_input("Role Title*", placeholder="Software Intern")
        location    = col3.text_input("Location", placeholder="Toronto, ON")

        job_link    = st.text_input("Job Link", placeholder="https://...")
        source      = st.selectbox("Source", SOURCE_OPTIONS, index=0)
        status      = st.selectbox("Status", STATUS_OPTIONS, index=2)  # default to Applied
        col4, col5, col6 = st.columns(3)
        deadline        = col4.date_input("Deadline", value=None, format="YYYY-MM-DD")
        date_applied    = col5.date_input("Date Applied", value=dt.date.today(), format="YYYY-MM-DD")
        follow_up_date  = col6.date_input("Follow-Up Date", value=None, format="YYYY-MM-DD")

        priority    = st.selectbox("Priority", PRIORITY_OPTIONS, index=1)
        recruiter_name  = st.text_input("Recruiter Name", placeholder="Jane Doe")
        recruiter_email = st.text_input("Recruiter Email", placeholder="jane@company.com")
        notes       = st.text_area("Notes", placeholder="Tailored resume; follow up next week")

        submitted = st.form_submit_button("Add application")
        if submitted:
            if not company or not role_title:
                st.error("Please fill in the required fields (Company and Role Title).")
            else:
                app = {
                    "company": company.strip(),
                    "role_title": role_title.strip(),
                    "location": location.strip() if location else None,
                    "job_link": job_link.strip() if job_link else None,
                    "source": source,
                    "status": status,
                    "deadline": str(deadline) if deadline else None,
                    "date_applied": str(date_applied) if date_applied else None,
                    "follow_up_date": str(follow_up_date) if follow_up_date else None,
                    "priority": priority,
                    "recruiter_name": recruiter_name.strip() if recruiter_name else None,
                    "recruiter_email": recruiter_email.strip() if recruiter_email else None,
                    "notes": notes.strip() if notes else None,
                    "last_updated": str(dt.datetime.now()),
                }
                add_application(app)
                st.success("Application added! Go to **View & Edit** to see it.")

# ---------- Tab: View & Edit ----------
with tabs[1]:
    st.subheader("Your applications")
    # Filters
    filt_cols = st.columns([2,2,2,3,1])
    status_f = filt_cols[0].selectbox("Filter by status", ["(All)"] + STATUS_OPTIONS, index=0)
    source_f = filt_cols[1].selectbox("Filter by source", ["(All)"] + SOURCE_OPTIONS, index=0)
    search_f = filt_cols[2].text_input("Search company/role", placeholder="type to filter")
    refresh  = filt_cols[3].button("Refresh")
    _ = refresh  # No-op; Streamlit reruns on button click

    filters = {}
    if status_f != "(All)":
        filters["status"] = status_f
    if source_f != "(All)":
        filters["source"] = source_f
    if search_f.strip():
        filters["search"] = search_f.strip()

    df = to_dataframe(filters)
    st.caption(f"{len(df)} rows")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("#### Edit / Delete")
    if len(df) > 0:
        # pick by ID
        ids = df["id"].tolist()
        id_to_edit = st.selectbox("Pick an Application ID", ids)
        row = df[df["id"] == id_to_edit].iloc[0].to_dict()

        with st.form("edit_form"):
            e1, e2, e3 = st.columns(3)
            company_e    = e1.text_input("Company*", value=row.get("company",""))
            role_e       = e2.text_input("Role Title*", value=row.get("role_title",""))
            location_e   = e3.text_input("Location", value=row.get("location") or "")

            link_e   = st.text_input("Job Link", value=row.get("job_link") or "")
            source_e = st.selectbox("Source", SOURCE_OPTIONS, index=max(0, SOURCE_OPTIONS.index(row.get("source") or SOURCE_OPTIONS[0])))
            status_e = st.selectbox("Status", STATUS_OPTIONS, index=max(0, STATUS_OPTIONS.index(row.get("status") or STATUS_OPTIONS[0])))

            f1, f2, f3 = st.columns(3)
            deadline_e   = f1.date_input("Deadline", value=pd.to_datetime(row.get("deadline")).date() if row.get("deadline") else None, format="YYYY-MM-DD")
            applied_e    = f2.date_input("Date Applied", value=pd.to_datetime(row.get("date_applied")).date() if row.get("date_applied") else None, format="YYYY-MM-DD")
            follow_e     = f3.date_input("Follow-Up Date", value=pd.to_datetime(row.get("follow_up_date")).date() if row.get("follow_up_date") else None, format="YYYY-MM-DD")

            priority_e = st.selectbox("Priority", ["High","Medium","Low"], index=max(0, ["High","Medium","Low"].index(row.get("priority") or "Medium")))
            rec_name_e  = st.text_input("Recruiter Name", value=row.get("recruiter_name") or "")
            rec_mail_e  = st.text_input("Recruiter Email", value=row.get("recruiter_email") or "")
            notes_e     = st.text_area("Notes", value=row.get("notes") or "", height=100)

            c1, c2 = st.columns(2)
            do_update = c1.form_submit_button("Save changes")
            do_delete = c2.form_submit_button("Delete", type="secondary")

        if do_update:
            if not company_e.strip() or not role_e.strip():
                st.error("Company and Role Title are required.")
            else:
                update_application(id_to_edit, {
                    "company": company_e.strip(),
                    "role_title": role_e.strip(),
                    "location": location_e.strip() or None,
                    "job_link": link_e.strip() or None,
                    "source": source_e,
                    "status": status_e,
                    "deadline": str(deadline_e) if deadline_e else None,
                    "date_applied": str(applied_e) if applied_e else None,
                    "follow_up_date": str(follow_e) if follow_e else None,
                    "priority": priority_e,
                    "recruiter_name": rec_name_e.strip() or None,
                    "recruiter_email": rec_mail_e.strip() or None,
                    "notes": notes_e.strip() or None,
                    "last_updated": str(pd.Timestamp.now())
                })
                st.success("Saved! Click Refresh above to see updates.")

        if do_delete:
            delete_application(id_to_edit)
            st.success("Deleted. Click Refresh above.")

    else:
        st.info("No rows yet. Add your first application in the **Add** tab.")

# ---------- Tab: Dashboard ----------
with tabs[2]:
    st.subheader("Progress overview")
    data = to_dataframe({})
    if len(data) == 0:
        st.info("Add some applications to see charts and counts.")
    else:
        # summary counts
        colA, colB, colC, colD = st.columns(4)
        colA.metric("Total", len(data))
        colB.metric("Applied", int((data["status"] == "Applied").sum()))
        colC.metric("Interviews", int((data["status"] == "Interview").sum() + (data["status"] == "Onsite/Final").sum()))
        colD.metric("Offers", int((data["status"] == "Offer").sum()))

        st.markdown("**By Status**")
        by_status = data["status"].value_counts().reset_index()
        by_status.columns = ["status","count"]
        st.bar_chart(by_status.set_index("status"))

        st.markdown("**Upcoming deadlines (next 7 days)**")
        if "deadline" in data.columns:
            data["deadline_dt"] = pd.to_datetime(data["deadline"], errors="coerce")
            upcoming = data[(pd.Timestamp.now().normalize() <= data["deadline_dt"]) & (data["deadline_dt"] <= (pd.Timestamp.now().normalize() + pd.Timedelta(days=7)))]
            if len(upcoming) == 0:
                st.write("No deadlines in the next 7 days.")
            else:
                st.dataframe(upcoming[["id","company","role_title","deadline"]], use_container_width=True, hide_index=True)

        st.markdown("**Follow-ups due today**")
        if "follow_up_date" in data.columns:
            data["follow_dt"] = pd.to_datetime(data["follow_up_date"], errors="coerce")
            today = pd.Timestamp.now().normalize()
            due = data[data["follow_dt"] == today]
            if len(due) == 0:
                st.write("No follow-ups due today.")
            else:
                st.dataframe(due[["id","company","role_title","follow_up_date"]], use_container_width=True, hide_index=True)

# ---------- Tab: Templates ----------
with tabs[3]:
    st.subheader("Follow-up email (auto-fill)")
    data = to_dataframe({})
    if len(data) == 0:
        st.info("Add at least one application to generate a follow-up email.")
    else:
        ids = data["id"].tolist()
        pick = st.selectbox("Pick Application ID", ids)
        row = data[data["id"] == pick].iloc[0].to_dict()

        recipient = st.text_input("Recipient name", value=row.get("recruiter_name") or "Hiring Team")
        company = row.get("company") or "your company"
        role = row.get("role_title") or "the role"
        applied_on = row.get("date_applied") or "recently"

        email = f"""Hi {recipient},

I hope you're well. I applied for **{role}** at **{company}** on {applied_on} and wanted to kindly follow up on my application. I'm very excited about the role and how my skills align with your team.

If there are any updates or next steps I can prepare for, please let me know. Thanks for your time!

Best regards,
[Your Name]
[Phone] | [LinkedIn]
"""
        st.code(email, language="markdown")

# ---------- Tab: Import / Export ----------
with tabs[4]:
    st.subheader("Export your data")
    df = to_dataframe({})
    if len(df) == 0:
        st.write("No data yet to export.")
    else:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="applications_export.csv", mime="text/csv")

    st.subheader("Import from CSV")
    st.caption("Your CSV should have columns like: company, role_title, location, job_link, source, status, deadline, date_applied, follow_up_date, priority, recruiter_name, recruiter_email, notes")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        try:
            up = pd.read_csv(file)
            # simple normalization
            up.columns = [c.strip().lower() for c in up.columns]
            required = ["company","role_title"]
            if not set(required).issubset(set(up.columns)):
                st.error("CSV must include at least company and role_title columns.")
            else:
                from db import bulk_insert_from_dataframe
                bulk_insert_from_dataframe(up)
                st.success("Import complete! Go to View & Edit to see your data.")
        except Exception as e:
            st.error(f"Import failed: {e}")
