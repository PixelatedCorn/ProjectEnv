import streamlit as st
import sqlite3

# Default fallback assignment safety validation
if "selected_resident_id" not in st.session_state:
    st.session_state.selected_resident_id = None

mode = st.session_state.sub_page

# ADD PROFILE SCREEN 
if mode == "Add":
    st.title("Add Resident Profile")
    with st.form("add_form"):
        name = st.text_input("Name")
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age", min_value=0, value=25)
        sex = c2.selectbox("Sex", ["Male", "Female"])
        status = c3.selectbox("Status", ["Active", "Archived"])
        dob = st.text_input("Date of Birth (YYYY-MM-DD)")
        bp = st.text_input("Birth Place")
        addr = st.text_area("Address")
        info = st.text_area("Other Info")
        
        if st.form_submit_button("Save Record"):
            with sqlite3.connect("Residents.db") as conn:
                conn.execute("INSERT INTO residents (name,sex,age,status,dob,birth_place,address,other_info) VALUES (?,?,?,?,?,?,?,?)",
                             (name, sex, age, status, dob, bp, addr, info))
            st.success("Saved successfully!")
            st.switch_page("pages/home.py")

# VIEW/EDIT SCREENS 
else:
    rid = st.session_state.selected_resident_id
    if not rid:
        st.warning("Please select a resident from the Home view directory first.")
        st.stop()
        
    with sqlite3.connect("Residents.db") as conn:
        conn.row_factory = sqlite3.Row
        res = conn.execute("SELECT * FROM residents WHERE id=?", (rid,)).fetchone()

    if mode == "View":
        st.title(f"Resident Profile: {res['name']}")
        st.text_input("Name", res["name"], disabled=True)
        st.text_input("Sex", res["sex"], disabled=True)
        st.text_input("Age", str(res["age"]), disabled=True)
        st.text_area("Address", res["address"], disabled=True)
        
        if st.session_state.access_level in ["Admin", "Editor"]:
            if st.button("Edit Profile Data Screen"):
                st.session_state.sub_page = "Edit"
                st.rerun()

    elif mode == "Edit":
        st.title("Edit Resident Profile")
        with st.form("edit_form"):
            en = st.text_input("Name", res["name"])
            es = st.selectbox("Sex", ["Male", "Female"], index=0 if res["sex"]=="Male" else 1)
            ea = st.number_input("Age", value=res["age"])
            est = st.selectbox("Status", ["Active", "Archived"], index=0 if res["status"]=="Active" else 1)
            ed = st.text_input("Date of Birth", res["dob"])
            eb = st.text_input("Birth Place", res["birth_place"])
            ead = st.text_area("Address", res["address"])
            ei = st.text_area("Other Info", res["other_info"])
            
            c1, c2 = st.columns(2)
            if c1.form_submit_button("Save System Changes"):
                with sqlite3.connect("Residents.db") as conn:
                    conn.execute("UPDATE residents SET name=?, sex=?, age=?, status=?, dob=?, birth_place=?, address=?, other_info=? WHERE id=?",
                                 (en, es, ea, est, ed, eb, ead, ei, rid))
                st.success("Record modified layout values successfully saved.")
                st.session_state.sub_page = "View"
                st.switch_page("pages/home.py")
            if c2.form_submit_button("Cancel Changes Process"):
                st.session_state.sub_page = "View"
                st.rerun()
