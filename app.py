import streamlit as st
import sqlite3

st.set_page_config(page_title="Barangay Tracker", layout="wide")

# Database (don't)
def init_dbs():
    with sqlite3.connect("Users.db") as cu:
        cu.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT, sex TEXT, username TEXT UNIQUE, password TEXT, access_level TEXT
            )
        """)
        cursor = cu.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone() == 0:
            cu.executemany("INSERT INTO users (fullname, sex, username, password, access_level) VALUES (?,?,?,?,?)", [
                ("Admin User", "Male", "admin", "password", "Admin"),
                ("Editor User", "Female", "editor", "password", "Editor"),
                ("Viewer User", "Male", "viewer", "password", "Viewer")
            ])
            cu.commit()

    with sqlite3.connect("Residents.db") as cr:
        # UPDATED SCHEMA WITH ALL 10 REQUESTED FIELDS
        cr.execute("""
            CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                surname TEXT, first_name TEXT, middle_name TEXT,
                dob TEXT, birth_place TEXT, household_no TEXT,
                sex TEXT, contact_info TEXT, address TEXT, 
                duration_residence TEXT, residency_status TEXT, 
                civil_status TEXT, citizenship TEXT, occupation TEXT
            )
        """)
        cursor = cr.cursor()
        cursor.execute("SELECT COUNT(*) FROM residents")
        if cursor.fetchone() == 0:
            cr.executemany("""
                INSERT INTO residents (
                    surname, first_name, middle_name, dob, birth_place, household_no,
                    sex, contact_info, address, duration_residence, residency_status, 
                    civil_status, citizenship, occupation
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, [
                ("Dela Cruz", "Juan", "Protacio", "1998-05-12", "Manila", "HH-001", "Male", "09171234567", "123 Rizal St., Purok 1", "5 Years", "Resident", "Single", "Filipino", "Software Engineer"),
                ("Clara", "Maria", "Santos", "2002-08-20", "Cebu", "HH-042", "Female", "09187654321", "456 Mabini St., Purok 3", "2 Years", "Resident", "Married", "Filipino", "Teacher")
            ])
            cr.commit()

init_dbs()

# State Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "access_level" not in st.session_state:
    st.session_state.access_level = "Viewer"
if "sub_page" not in st.session_state:
    st.session_state.sub_page = "View"

def logout():
    st.session_state.logged_in = False
    st.rerun()

# Authentication Router
if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] { display: none; }
            [data-testid="stSidebarCollapseButton"] { display: none; }
        </style>
        """, unsafe_allow_html=True
    )
    
    st.markdown("<h1 style='text-align: center;'>Barangay Residents Tracker</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                with sqlite3.connect("Users.db") as conn:
                    conn.row_factory = sqlite3.Row
                    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.access_level = user["access_level"]
                    st.rerun()
                else:
                    st.error("Invalid credentials")
else:
    with st.sidebar:
        st.write(f"**Logged in as:** {st.session_state.username} ({st.session_state.access_level})")
        if st.button("Log Out", type="primary", use_container_width=True):
            logout()

    pages = [
        st.Page("pages/home.py", title="Home", icon="🏠"),
        st.Page("pages/profile.py", title="Resident Profiles", icon="👤"),
        st.Page("pages/reports.py", title="Report Part", icon="📊")
    ]
    if st.session_state.access_level == "Admin":
        pages.append(st.Page("pages/accounts.py", title="Account Handling", icon="⚙️"))

    pg = st.navigation(pages)
    pg.run()
