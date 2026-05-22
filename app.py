import streamlit as st
import sqlite3


st.set_page_config(page_title="Barangay Tracker", layout="wide")

# Initialize Databases
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
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                surname TEXT, first_name TEXT, middle_name TEXT,
                dob TEXT, birth_place TEXT, household_no TEXT,
                sex TEXT, contact_info TEXT, address TEXT, 
                duration_residence TEXT, residency_status TEXT, 
                civil_status TEXT, citizenship TEXT, occupation TEXT,
                age INTEGER,
                purok TEXT,
                last_modified_by TEXT
            )
        """)
        cursor = cr.cursor()
        cursor.execute("SELECT COUNT(*) FROM residents")
        if cursor.fetchone() == 0:
            cr.executemany("""
                INSERT INTO residents (
                    surname, first_name, middle_name, dob, birth_place, household_no,
                    sex, contact_info, address, duration_residence, residency_status, 
                    civil_status, citizenship, occupation, age, purok, last_modified_by
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, [
                ("Dela Cruz", "Juan", "Protacio", "1998-05-12", "Manila", "HH-001", "Male", "09171234567", "123 Rizal St.", "5 Years", "Resident", "Single", "Filipino", "Software Engineer", 28, "Purok 1", "system_seed"),
                ("Clara", "Maria", "Santos", "2002-08-20", "Cebu", "HH-042", "Female", "09187654321", "456 Mabini St.", "2 Years", "Resident", "Married", "Filipino", "Teacher", 24, "Purok 3", "system_seed")
            ])
            cr.commit()

init_dbs()

# State Management Initialization
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

# Router Setup
if not st.session_state.logged_in:

    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
        font-family: sans-serif;
        }

        /* Hide sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="stSidebarCollapseButton"] {
            display: none;
        }

        /* Background */
        .stApp {
            background-color: white;
         }

 

        /* Remove extra spacing */
        .block-container {
            padding-top: 2rem;
        }

        /* Main title */
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            color: #1E3A5F;
            margin-bottom: 5px;
            font-family: 'Poppins', sans-serif;
        }

        /* Subtitle */
        .sub-title {
            text-align: center;
            color: #5c6b7a;
            margin-bottom: 40px;
            font-size: 16px;
        }

        /* Login card */
        .login-card {
            background: #1E3A5F;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0px 5px 20px rgba(0,0,0,0.12);
            border: 1px solid #dce6f2;
        }

        div[data-testid="stForm"] {
            background-color: #1E3A5F;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
        }

        div[data-testid="stForm"] label {
            color: white !important;
        }

        /* Inputs */
        .stTextInput input {
            border-radius: 12px;
            border: 1px solid #cfd9e6;
            padding: 10px;
            background-color: white !important;
            color: black !important;
        }
        
        label, .stTextInput label {
            color: #1E3A5F !important;
            font-family: sans-serif;
            font-weight: 600;
        }

        h3 {
            color: white;
            font-family: 'Poppins', sans-serif;
        }
        
        .stCaption {
            color: #dbe7f5 !important;
        }

        /* Login button */
        .stButton button {
            background-color: #1E3A5F;
            color: white;
            border-radius: 12px;
            border: none;
            padding: 12px;
            font-weight: 600;
            font-size: 15px;
        }

        .stButton button:hover {
            background-color: #27496d;
            color: white;
        }

        /* Footer */
        .footer-text {
            text-align: center;
            color: #5c6b7a;
            margin-top: 30px;
            font-size: 13px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class='main-title'>🏘️ Barangay Residents Tracker</div>
        <div class='sub-title'>
            Resident Information and Community Management System
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1,1.2,1])

    with center:

        st.markdown("### 🔐 Login")
        st.caption("Enter your credentials to continue.")

        with st.form("login"):

            u = st.text_input("Username")
            p = st.text_input("Password", type="password")

            if st.form_submit_button("Login", use_container_width=True):

                with sqlite3.connect("Users.db") as conn:
                    conn.row_factory = sqlite3.Row

                    user = conn.execute(
                        "SELECT * FROM users WHERE username=? AND password=?",
                        (u, p)
                    ).fetchone()

                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.access_level = user["access_level"]
                    st.rerun()

                else:
                    st.error("Invalid credentials")

    st.markdown(
        """
        <div class='footer-text'>
            Barangay Resident Management System • 2026
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.markdown("""
    <style>

    [data-testid="stSidebar"]{
        background-color: #163B65;
    }

    [data-testid="stSidebar"] *{
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)
     
    st.session_state.home_route = st.Page("pages/home.py", title="Home", icon="🏠")
    st.session_state.report_route = st.Page("pages/reports.py", title="Report Part", icon="📊")
    st.session_state.account_route = st.Page("pages/accounts.py", title="Account Handling", icon="⚙️")
    st.session_state.profile_route = st.Page("pages/profile.py", title="Resident Profile", icon="👤")

    

    with st.sidebar:
        if st.session_state.access_level in ["Admin", "Editor"]:
            if st.button("➕ Add New Resident", use_container_width=True):
                st.session_state.sub_page = "Add"
                st.switch_page(st.session_state.profile_route)

        st.write("---")
        st.success(f"Logged in as: {st.session_state.username}")
        st.caption(f"Access Level: {st.session_state.access_level}")
        st.write("---")

        if st.button("Log Out", type="primary", use_container_width=True):
            logout()

    visible_navigation_array = [
        st.session_state.home_route,
        st.session_state.report_route,
        st.session_state.profile_route
    ]

    if st.session_state.access_level == "Admin":
        visible_navigation_array.append(st.session_state.account_route)

    st.markdown(
        """
        <style>
            a[href*="profile"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    pg = st.navigation(visible_navigation_array)
    pg.run()