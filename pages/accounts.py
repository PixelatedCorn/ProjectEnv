import streamlit as st
import pandas as pd
import sqlite3

st.title("Account Management Workspace")

with sqlite3.connect("Users.db") as conn:
    df = pd.read_sql_query("SELECT id, fullname, sex, username, access_level FROM users", conn)

st.dataframe(df, use_container_width=True)

st.write("---")
st.write("### Create / Register New System Profile Account")
with st.form("new_acc_form"):
    fn = st.text_input("Full Name")
    sx = st.selectbox("Sex Orientation", ["Male", "Female"])
    un = st.text_input("Username Code Access ID")
    pw = st.text_input("Password String", type="password")
    al = st.selectbox("Access Level Permission Group", ["Admin", "Editor", "Viewer"])
    
    if st.form_submit_button("Register Security User"):
        try:
            with sqlite3.connect("Users.db") as conn:
                conn.execute("INSERT INTO users (fullname, sex, username, password, access_level) VALUES (?,?,?,?,?)",
                             (fn, sx, un, pw, al))
            st.success("User account saved to database system directory module updates successfully.")
            st.rerun()
        except sqlite3.IntegrityError:
            st.error("Unique entry violation: System user index key reference collision detected.")
