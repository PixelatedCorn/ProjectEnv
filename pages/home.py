import streamlit as st
import pandas as pd
import sqlite3

st.title("Home - Resident Directory")

c1, c2 = st.columns(2)
search = c1.text_input("Search Name (First, Middle, or Surname)")
sort = c2.selectbox("Sort By", ["None", "Surname", "Sex"])

with sqlite3.connect("Residents.db") as conn:
    query = "SELECT *, (surname || ', ' || first_name || ' ' || middle_name) as full_name FROM residents WHERE 1=1"
    params = []
    if search:
        query += " AND (surname LIKE ? OR first_name LIKE ? OR middle_name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if sort == "Surname":
        query += " ORDER BY surname ASC"
    elif sort == "Sex":
        query += " ORDER BY sex ASC"
    df = pd.read_sql_query(query, conn, params=params)

st.markdown("---")

# Organized Header
col_n, col_s, col_h, col_st, col_b = st.columns([3, 1, 1.5, 1.5, 1.5])
col_n.markdown("**Full Name**")
col_s.markdown("**Sex**")
col_h.markdown("**Household No.**")
col_st.markdown("**Residency Status**")
col_b.markdown("**Action**")

for _, row in df.iterrows():
    col_n, col_s, col_h, col_st, col_b = st.columns([3, 1, 1.5, 1.5, 1.5])
    col_n.write(f"{row['surname']}, {row['first_name']} {row['middle_name']}")
    col_s.write(row["sex"])
    col_h.write(row["household_no"])
    col_st.write(row["residency_status"])
    if col_b.button("View Profile", key=f"v_{row['id']}", use_container_width=True):
        st.session_state.selected_resident_id = int(row["id"])
        st.session_state.sub_page = "View"
        st.switch_page("pages/profile.py")

if st.session_state.access_level in ["Admin", "Editor"]:
    st.write("---")
    if st.button("Add New Resident Record"):
        st.session_state.sub_page = "Add"
        st.switch_page("pages/profile.py")
