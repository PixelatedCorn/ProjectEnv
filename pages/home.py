import streamlit as st
import pandas as pd
import sqlite3

st.title("Home - Resident Directory")

# Filter controls
c1, c2 = st.columns(2)
search = c1.text_input("Search Name")
sort = c2.selectbox("Sort By", ["None", "Alphabetical", "Sex"])

with sqlite3.connect("Residents.db") as conn:
    query = "SELECT * FROM residents WHERE 1=1"
    params = []
    if search:
        query += " AND name LIKE ?"
        params.append(f"%{search}%")
    if sort == "Alphabetical":
        query += " ORDER BY name ASC"
    elif sort == "Sex":
        query += " ORDER BY sex ASC"
    df = pd.read_sql_query(query, conn, params=params)

# Header Row Layout
st.markdown("---")
cols = st.columns([3, 1, 1, 3, 2])
cols[0].markdown("**Name**")
cols[1].markdown("**Sex**")
cols[2].markdown("**Age**")
cols[3].markdown("**Address**")
cols[4].markdown("**Action**")

# Data Presentation loop
for _, row in df.iterrows():
    cols = st.columns([3, 1, 1, 3, 2])
    cols[0].write(row["name"])
    cols[1].write(row["sex"])
    cols[2].write(str(row["age"]))
    cols[3].write(row["address"])
    if cols[4].button("View Profile", key=f"v_{row['id']}"):
        st.session_state.selected_resident_id = int(row["id"])
        st.session_state.sub_page = "View"
        st.switch_page("pages/profile.py")

if st.session_state.access_level in ["Admin", "Editor"]:
    st.write("---")
    if st.button("Add New Resident Record"):
        st.session_state.sub_page = "Add"
        st.switch_page("pages/profile.py")
