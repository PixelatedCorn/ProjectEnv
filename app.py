import streamlit as st
import sqlite3

st.set_page_config(page_title="Barangay Tracker", layout="wide")

# Database Setup 'to
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
        cr.execute("""
            CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, sex TEXT, age INTEGER, 
                status TEXT, dob TEXT, birth_place TEXT, address TEXT, other_info TEXT
            )
        """)
        cursor = cr.cursor()
        cursor.execute("SELECT COUNT(*) FROM residents")
        if cursor.fetchone() == 0:
            cr.executemany("INSERT INTO residents (name, sex, age, status, dob, birth_place, address, other_info) VALUES (?,?,?,?,?,?,?,?)", [
                ("Juan Dela Cruz", "Male", 28, "Active", "1998-05-12", "Manila", "123 Rizal St.", "Purok 1"),
                ("Maria Clara", "Female", 24, "Active", "2002-08-20", "Cebu", "456 Mabini St.", "Purok 3")
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
    # Delete mo to makikita sidebar sa login page
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="stSidebarCollapseButton"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
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
    # Sidebar layout rules pag naka login na
    with st.sidebar:
        st.write(f"**Logged in as:** {st.session_state.username} ({st.session_state.access_level})")
        if st.button("Log Out", type="primary", use_container_width=True):
            logout()

    # Dynamic Navigation Routing Setup
    pages = [
        st.Page("pages/home.py", title="Home", icon="🏠"),
        st.Page("pages/profile.py", title="Resident Profiles", icon="👤"),
        st.Page("pages/reports.py", title="Report Part", icon="📊")
    ]
    if st.session_state.access_level == "Admin":
        pages.append(st.Page("pages/accounts.py", title="Account Handling", icon="⚙️"))

    pg = st.navigation(pages)
    pg.run()
