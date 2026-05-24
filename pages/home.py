import streamlit as st
import pandas as pd
import sqlite3
from frontend import apply_style

apply_style("home")

st.title("Home - Resident Directory")
st.markdown(f"""
<div style="
background: linear-gradient(90deg, #163B65, #245082);
padding: 25px;
border-radius: 22px;
color: white;
margin-bottom: 20px;
">
    <h2 style="margin:0;">Welcome back, {st.session_state.username} 👋</h2>
    <p style="margin-top:5px;">
        Manage resident records and community data efficiently.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
search = c1.text_input("Search Name (First, Middle, or Surname)")
sort = c2.selectbox(
    "Sort / Filter By", 
    ["None", "Alphabetical", "Age", "Sex (Male Only)", "Sex (Female Only)"]
)

show_archived = st.checkbox("Include Archived Records", value=False, help="Check this to include hidden or inactive records in your lookup pool.")

with sqlite3.connect("Residents.db") as conn:
    query = "SELECT *, (surname || ', ' || first_name || ' ' || middle_name) as full_name FROM residents WHERE 1=1"
    params = []
    
    if not show_archived:
        query += " AND residency_status != 'Archived'"
        
    if search:
        query += " AND (surname LIKE ? OR first_name LIKE ? OR middle_name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
    if sort == "Sex (Male Only)":
        query += " AND sex = 'Male'"
    elif sort == "Sex (Female Only)":
        query += " AND sex = 'Female'"
        
    if sort == "Alphabetical":
        query += " ORDER BY surname ASC"
    elif sort == "Age":
        query += " ORDER BY age ASC"
        
    df = pd.read_sql_query(query, conn, params=params)

    total_residents = len(df)
male_count = len(df[df["sex"] == "Male"])
female_count = len(df[df["sex"] == "Female"])
archived_count = len(df[df["residency_status"] == "Archived"])

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <h3> {total_residents}</h3>
        <p>Total Residents</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <h3> {male_count}</h3>
        <p>Male Residents</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <h3> {female_count}</h3>
        <p>Female Residents</p>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <h3> {archived_count}</h3>
        <p>Archived</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

<<<<<<< HEAD
# Header
st.markdown('<div class="header-row">Resident Directory Records</div>', unsafe_allow_html=True)

=======
# Pagination
ROWS_PER_PAGE = 10
total_rows = len(df)
total_pages = max(1, -(-total_rows // ROWS_PER_PAGE))  # Ceiling division

# Reset page if search/filter changes
filter_state = (search, sort, show_archived)
if "last_filter_state" not in st.session_state or st.session_state.last_filter_state != filter_state:
    st.session_state.current_page = 1
    st.session_state.last_filter_state = filter_state

if "current_page" not in st.session_state:
    st.session_state.current_page = 1

current_page = st.session_state.current_page
start_idx = (current_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE
page_df = df.iloc[start_idx:end_idx]

# --- Header ---
>>>>>>> fbfcd85 (Validation)
col_n, col_s, col_a, col_st, col_b = st.columns([3, 1, 1, 2, 1.5])

col_n.markdown("**Full Name**")
col_s.markdown("**Sex**")
col_a.markdown("**Age**")
col_st.markdown("**Residency Status**")
col_b.markdown("**Action**")

for _, row in page_df.iterrows():
    col_n, col_s, col_a, col_st, col_b = st.columns([3, 1, 1, 2, 1.5])

    st.markdown('<div class="resident-row">', unsafe_allow_html=True)
    
    is_rec_archived = (row['residency_status'] == 'Archived')
    display_name = f"{row['surname']}, {row['first_name']} {row['middle_name']}"
    
    if is_rec_archived:
        display_name = f"📁 {display_name} *(Archived)*"
        
    col_n.write(display_name if display_name.strip() not in ["", ",", "📁  *(Archived)*"] else "Unnamed Resident")
    col_s.write(row["sex"] if row["sex"] else "N/A")
    col_a.write(str(row["age"]) if row["age"] is not None else "0")
    col_st.write(row["residency_status"] if row["residency_status"] else "Resident")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if col_b.button("View Profile", key=f"v_{row['id']}", use_container_width=True):
        st.session_state.selected_resident_id = int(row["id"])
        st.session_state.sub_page = "View"
        st.switch_page(st.session_state.profile_route)

# --- Pagination Controls ---
st.markdown("---")
p_left, p_mid, p_right = st.columns([1, 2, 1])

with p_left:
    if st.button("← Previous", disabled=(current_page == 1), use_container_width=True):
        st.session_state.current_page -= 1
        st.rerun()

with p_mid:
    st.markdown(
        f"<div style='text-align:center; padding-top: 6px;'>Page <b>{current_page}</b> of <b>{total_pages}</b> &nbsp;|&nbsp; {total_rows} record(s)</div>",
        unsafe_allow_html=True
    )

with p_right:
    if st.button("Next →", disabled=(current_page == total_pages), use_container_width=True):
        st.session_state.current_page += 1
        st.rerun()