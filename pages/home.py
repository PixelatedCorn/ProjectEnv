import streamlit as st
import pandas as pd
import sqlite3

st.title("Home - Resident Directory")

c1, c2 = st.columns(2)
search = c1.text_input("Search Name (First, Middle, or Surname)")
sort = c2.selectbox(
    "Sort / Filter By", 
    ["None", "Alphabetical", "Age", "Sex (Male Only)", "Sex (Female Only)"]
)

# Default filter state for archived records (default)
show_archived = st.checkbox("Include Archived Records", value=False, help="Check this to include hidden or inactive records in your lookup pool.")

with sqlite3.connect("Residents.db") as conn:
    query = "SELECT *, (surname || ', ' || first_name || ' ' || middle_name) as full_name FROM residents WHERE 1=1"
    params = []
    
    # Default filtering behavior for archived individuals
    if not show_archived:
        query += " AND residency_status != 'Archived'"
        
    # Search processing
    if search:
        query += " AND (surname LIKE ? OR first_name LIKE ? OR middle_name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
    # Sorting
    if sort == "Sex (Male Only)":
        query += " AND sex = 'Male'"
    elif sort == "Sex (Female Only)":
        query += " AND sex = 'Female'"
        
    if sort == "Alphabetical":
        query += " ORDER BY surname ASC"
    elif sort == "Age":
        query += " ORDER BY age ASC"
        
    df = pd.read_sql_query(query, conn, params=params)

st.markdown("---")

# Header
col_n, col_s, col_a, col_st, col_b = st.columns([3, 1, 1, 2, 1.5])
col_n.markdown("**Full Name**")
col_s.markdown("**Sex**")
col_a.markdown("**Age**")
col_st.markdown("**Residency Status**")
col_b.markdown("**Action**")

for _, row in df.iterrows():
    col_n, col_s, col_a, col_st, col_b = st.columns([3, 1, 1, 2, 1.5])
    
    # Visual cues for archived entries (Display)
    is_rec_archived = (row['residency_status'] == 'Archived')
    display_name = f"{row['surname']}, {row['first_name']} {row['middle_name']}"
    
    if is_rec_archived:
        display_name = f"📁 {display_name} *(Archived)*"
        
    col_n.write(display_name if display_name.strip() not in ["", ",", "📁  *(Archived)*"] else "Unnamed Resident")
    col_s.write(row["sex"] if row["sex"] else "N/A")
    col_a.write(str(row["age"]) if row["age"] is not None else "0")
    col_st.write(row["residency_status"] if row["residency_status"] else "Resident")
    
    if col_b.button("View Profile", key=f"v_{row['id']}", use_container_width=True):
        st.session_state.selected_resident_id = int(row["id"])
        st.session_state.sub_page = "View"
        st.switch_page(st.session_state.profile_route)
