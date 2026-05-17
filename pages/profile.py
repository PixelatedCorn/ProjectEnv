import streamlit as st
import sqlite3

if "selected_resident_id" not in st.session_state:
    st.session_state.selected_resident_id = None

mode = st.session_state.sub_page

# Options list constants
SEX_OPTS = ["Male", "Female"]
CIVIL_OPTS = ["Single", "Married", "Widowed", "Separated"]
STATUS_OPTS = ["Resident", "Non-Resident", "Transient"]

# --- ADD PROFILE SCREEN ---
if mode == "Add":
    st.title("Add New Resident Profile")
    with st.form("add_form"):
        st.subheader("Personal Information")
        n1, n2, n3 = st.columns(3)
        ln = n1.text_input("Surname")
        fn = n2.text_input("First Name")
        mn = n3.text_input("Middle Name")
        
        c1, c2, c3 = st.columns(3)
        sex = c1.selectbox("Sex", SEX_OPTS)
        civ = c2.selectbox("Civil Status", CIVIL_OPTS)
        cit = c3.text_input("Citizenship", value="Filipino")

        st.subheader("Birth & Family Structure")
        b1, b2, b3 = st.columns(3)
        dob = b1.text_input("Date of Birth (YYYY-MM-DD)")
        bp = b2.text_input("Place of Birth")
        hh = b3.text_input("Household Number / ID")

        st.subheader("Address & Community Ties")
        addr = st.text_area("Complete Address")
        a1, a2, a3 = st.columns(3)
        dur = a1.text_input("Duration of Residence (e.g. 5 Years)")
        res_st = a2.selectbox("Residency Status", STATUS_OPTS)
        occ = a3.text_input("Occupation")
        
        st.write("---")
        if st.form_submit_button("Save New Resident Record", use_container_width=True):
            with sqlite3.connect("Residents.db") as conn:
                conn.execute("""
                    INSERT INTO residents (
                        surname, first_name, middle_name, dob, birth_place, household_no,
                        sex, contact_info, address, duration_residence, residency_status, 
                        civil_status, citizenship, occupation
                    ) VALUES (?,?,?,?,?,?,?,?,'',?,?,?,?,?)
                """, (ln, fn, mn, dob, bp, hh, sex, addr, dur, res_st, civ, cit, occ))
            st.success("New data profile added successfully!")
            st.switch_page("pages/home.py")

# --- VIEW & EDIT SCREENS ---
else:
    rid = st.session_state.selected_resident_id
    if not rid:
        st.warning("Please select a resident from the Home directory first.")
        st.stop()
        
    with sqlite3.connect("Residents.db") as conn:
        conn.row_factory = sqlite3.Row
        res = conn.execute("SELECT * FROM residents WHERE id=?", (rid,)).fetchone()

    if mode == "View":
        st.title(f"Resident Profile: {res['surname']}, {res['first_name']}")
        
        st.subheader("Personal Information")
        n1, n2, n3 = st.columns(3)
        n1.text_input("Surname", res["surname"], disabled=True)
        n2.text_input("First Name", res["first_name"], disabled=True)
        n3.text_input("Middle Name", res["middle_name"], disabled=True)
        
        c1, c2, c3 = st.columns(3)
        c1.text_input("Sex", res["sex"], disabled=True)
        c2.text_input("Civil Status", res["civil_status"], disabled=True)
        c3.text_input("Citizenship", res["citizenship"], disabled=True)

        st.subheader("Birth & Family Structure")
        b1, b2, b3 = st.columns(3)
        b1.text_input("Date of Birth", res["dob"], disabled=True)
        b2.text_input("Place of Birth", res["birth_place"], disabled=True)
        b3.text_input("Household Number / ID", res["household_no"], disabled=True)

        st.subheader("Address & Community Ties")
        st.text_area("Complete Address", res["address"], disabled=True)
        a1, a2, a3 = st.columns(3)
        a1.text_input("Duration of Residence", res["duration_residence"], disabled=True)
        a2.text_input("Residency Status", res["residency_status"], disabled=True)
        a3.text_input("Occupation", res["occupation"], disabled=True)
        
        st.write("---")
        col_back, col_edit = st.columns(2)
        if col_back.button("Back to Home Directory", use_container_width=True):
            st.switch_page("pages/home.py")
        if st.session_state.access_level in ["Admin", "Editor"]:
            if col_edit.button("Modify Profile Data", use_container_width=True, type="primary"):
                st.session_state.sub_page = "Edit"
                st.rerun()

    elif mode == "Edit":
        st.title(f"Edit Profile: {res['surname']}, {res['first_name']}")
        with st.form("edit_form"):
            st.subheader("Personal Information")
            n1, n2, n3 = st.columns(3)
            eln = n1.text_input("Surname", res["surname"])
            efn = n2.text_input("First Name", res["first_name"])
            emn = n3.text_input("Middle Name", res["middle_name"])
            
            c1, c2, c3 = st.columns(3)
            esex = c1.selectbox("Sex", SEX_OPTS, index=SEX_OPTS.index(res["sex"]) if res["sex"] in SEX_OPTS else 0)
            eciv = c2.selectbox("Civil Status", CIVIL_OPTS, index=CIVIL_OPTS.index(res["civil_status"]) if res["civil_status"] in CIVIL_OPTS else 0)
            ecit = c3.text_input("Citizenship", res["citizenship"])

            st.subheader("Birth & Family Structure")
            b1, b2, b3 = st.columns(3)
            edob = b1.text_input("Date of Birth (YYYY-MM-DD)", res["dob"])
            ebp = b2.text_input("Place of Birth", res["birth_place"])
            ehh = b3.text_input("Household Number / ID", res["household_no"])

            st.subheader("Address & Community Ties")
            eaddr = st.text_area("Complete Address", res["address"])
            a1, a2, a3 = st.columns(3)
            edur = a1.text_input("Duration of Residence", res["duration_residence"])
            eres_st = a2.selectbox("Residency Status", STATUS_OPTS, index=STATUS_OPTS.index(res["residency_status"]) if res["residency_status"] in STATUS_OPTS else 0)
            eocc = a3.text_input("Occupation", res["occupation"])
            
            st.write("---")
            btn1, btn2 = st.columns(2)
            if btn1.form_submit_button("Save Structural Changes", use_container_width=True):
                with sqlite3.connect("Residents.db") as conn:
                    conn.execute("""
                        UPDATE residents SET 
                            surname=?, first_name=?, middle_name=?, dob=?, birth_place=?, household_no=?,
                            sex=?, address=?, duration_residence=?, residency_status=?, civil_status=?, 
                            citizenship=?, occupation=?
                        WHERE id=?
                    """, (eln, efn, emn, edob, ebp, ehh, esex, eaddr, edur, eres_st, eciv, ecit, eocc, rid))
                st.success("Changes saved successfully!")
                st.session_state.sub_page = "View"
                st.switch_page("pages/home.py")
            if btn2.form_submit_button("Cancel Changes Process", use_container_width=True):
                st.session_state.sub_page = "View"
                st.rerun()
