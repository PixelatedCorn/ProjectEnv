import streamlit as st
import sqlite3
from datetime import datetime, date
from frontend import apply_style

apply_style("profile")

if "selected_resident_id" not in st.session_state:
    st.session_state.selected_resident_id = None

mode = st.session_state.sub_page

SEX_OPTS = ["Male", "Female"]
CIVIL_OPTS = ["Single", "Married", "Widowed", "Separated"]
STATUS_OPTS = ["Resident", "Non-Resident", "Transient", "Archived"]
PUROK_OPTS = ["Purok 1", "Purok 2", "Purok 3", "Purok 4", "Purok 5", "Sitio Central", "Sitio Ilaya"]

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return max(0, age)

# --- ADD RESIDENT ---
if mode == "Add":
    st.title("Add New Resident Profile")
    st.caption("Create and register a new barangay resident profile.")
    with st.form("add_form"):
        st.subheader("Personal Information")
        n1, n2, n3 = st.columns(3)
        ln = n1.text_input("Surname")
        fn = n2.text_input("First Name")
        mn = n3.text_input("Middle Name")
        
        c1, c2 = st.columns(2)
        sex = c1.selectbox("Sex", SEX_OPTS)
        civ = c2.selectbox("Civil Status", CIVIL_OPTS)

        st.subheader("Birth & Family Structure")
        b1, b2, b3 = st.columns(3)
        dob_date = b1.date_input("Date of Birth", value=date(2000, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())
        bp = b2.text_input("Place of Birth")
        hh = b3.text_input("Household Number / ID")

        st.subheader("Address & Community Ties")
        cit = st.text_input("Citizenship", value="Filipino")
        addr = st.text_area("Complete Address")
        
        a1, a2, a3 = st.columns(3)
        dur = a1.text_input("Duration of Residence (e.g., 5 Years)")
        purok = a2.selectbox("Purok / Sitio Zone", PUROK_OPTS)
        res_st = a3.selectbox("Residency Status", [s for s in STATUS_OPTS if s != "Archived"])
        occ = st.text_input("Occupation")
        
        st.write("---")
        if st.form_submit_button("Cancel", use_container_width=True):
            st.switch_page(st.session_state.home_route)
        if st.form_submit_button("Save New Resident Record", use_container_width=True):
            computed_age = calculate_age(dob_date)
            dob_str = dob_date.strftime("%Y-%m-%d")
            # Pull currently logged-in account name for accountability tracking
            active_editor = st.session_state.username
            
            with sqlite3.connect("Residents.db") as conn:
                conn.execute("""
                    INSERT INTO residents (
                        surname, first_name, middle_name, dob, birth_place, household_no,
                        sex, contact_info, address, duration_residence, residency_status, 
                        civil_status, citizenship, occupation, age, purok, last_modified_by
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (ln, fn, mn, dob_str, bp, hh, sex, '', addr, dur, res_st, civ, cit, occ, computed_age, purok, active_editor))
                conn.commit()
            st.success("Profile saved successfully!")
            st.switch_page(st.session_state.home_route)

# --- VIEW & EDIT MODES ---
else:
    rid = st.session_state.selected_resident_id
    if not rid:
        st.warning("Please select a resident from the Home directory first.")
        st.stop()
        
    with sqlite3.connect("Residents.db") as conn:
        conn.row_factory = sqlite3.Row
        res = conn.execute("SELECT * FROM residents WHERE id=?", (rid,)).fetchone()

    if mode == "View":
        st.markdown("""
    <style>

    .profile-card{
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #dbe7f3;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }

    .section-title{
        color: #163B65;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    </style>
    """, unsafe_allow_html=True)
        
        st.title(f"Resident Profile: {res['surname']}, {res['first_name']}")
        
        # --- TRACKER LOG VISIBLE DISPLAY ---
        modifier = res["last_modified_by"] if res["last_modified_by"] else "Unknown User"
        st.caption(f"✍🏽 **System Audit Trail:** This record was last modified or registered by user account: `{modifier}`")
        
        resident_age = res["age"] if res["age"] is not None else 0
        if resident_age >= 60:
            st.warning(f"👵🏽👴🏽 **Demographic Alert:** This resident is a Senior Citizen ({resident_age}yo)")
        elif resident_age < 18:
            st.info(f"👶🏽 **Demographic Alert:** This resident is a Minor ({resident_age}yo)")
            
        if res["residency_status"] == "Archived":
            st.error("📂 **Status Alert:** This record is currently Archived.")

        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title"> Personal Information</div>', unsafe_allow_html=True)
        n1, n2, n3 = st.columns(3)
        n1.text_input("Surname", res["surname"], disabled=True)
        n2.text_input("First Name", res["first_name"], disabled=True)
        n3.text_input("Middle Name", res["middle_name"], disabled=True)
        
        c1, c2, c3 = st.columns(3)
        c1.text_input("Sex", res["sex"], disabled=True)
        c2.text_input("Age (Auto-Calculated)", str(resident_age), disabled=True)
        c3.text_input("Civil Status", res["civil_status"], disabled=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-title"> Birth & Family Structure</div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        display_dob = res["dob"]
        try:
            display_dob = datetime.strptime(res["dob"], "%Y-%m-%d").strftime("%B %d, %Y")
        except:
            pass
        b1.text_input("Date of Birth", display_dob, disabled=True)
        b2.text_input("Place of Birth", res["birth_place"], disabled=True)
        b3.text_input("Household Number / ID", res["household_no"], disabled=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-title"> Birth & Address & Community Ties</div>', unsafe_allow_html=True)
        st.text_input("Purok / Sitio Zone", res["purok"] if res["purok"] else "Unassigned", disabled=True)
        st.text_area("Complete Address", res["address"], disabled=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        a1, a2, a3 = st.columns(3)
        a1.text_input("Duration of Residence", res["duration_residence"], disabled=True)
        a2.text_input("Residency Status", res["residency_status"], disabled=True)
        a3.text_input("Occupation", res["occupation"], disabled=True)
        
        st.write("---")
        cb, ce = st.columns(2)
        if cb.button("Back to Home Directory", use_container_width=True):
            st.switch_page(st.session_state.home_route)
        if st.session_state.access_level in ["Admin", "Editor"]:
            if ce.button("Modify Profile Data", use_container_width=True, type="primary"):
                st.session_state.sub_page = "Edit"
                st.rerun()

        if st.session_state.access_level in ["Admin", "Editor"]:
            st.write("---")
            with st.expander("📂 Records Management (Archive Switch)", expanded=False):
                active_editor = st.session_state.username
                if res["residency_status"] == "Archived":
                    if st.button("Restore Profile to Active Status", use_container_width=True):
                        with sqlite3.connect("Residents.db") as conn:
                            conn.execute("UPDATE residents SET residency_status = 'Resident', last_modified_by = ? WHERE id = ?", (active_editor, rid))
                            conn.commit()
                        st.success("Resident restored.")
                        st.rerun()
                else:
                    if st.button("Archive Resident Record", type="primary", use_container_width=True):
                        with sqlite3.connect("Residents.db") as conn:
                            conn.execute("UPDATE residents SET residency_status = 'Archived', last_modified_by = ? WHERE id = ?", (active_editor, rid))
                            conn.commit()
                        st.warning("Resident archived.")
                        st.rerun()

    elif mode == "Edit":
        st.title(f"Edit Profile: {res['surname']}, {res['first_name']}")
        try:
            default_date = datetime.strptime(res["dob"], "%Y-%m-%d").date()
        except:
            default_date = date(2000, 1, 1)

        with st.form("edit_form"):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            st.subheader("Personal Information")
            n1, n2, n3 = st.columns(3)
            eln = n1.text_input("Surname", res["surname"])
            efn = n2.text_input("First Name", res["first_name"])
            emn = n3.text_input("Middle Name", res["middle_name"])
            
            c1, c2 = st.columns(2)
            esex = c1.selectbox("Sex", SEX_OPTS, index=SEX_OPTS.index(res["sex"]) if res["sex"] in SEX_OPTS else 0)
            eciv = c2.selectbox("Civil Status", CIVIL_OPTS, index=CIVIL_OPTS.index(res["civil_status"]) if res["civil_status"] in CIVIL_OPTS else 0)

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            st.subheader("Birth & Family Structure")
            b1, b2, b3 = st.columns(3)
            edob_date = b1.date_input("Date of Birth", value=default_date, min_value=date(1900, 1, 1), max_value=date.today())
            ebp = b2.text_input("Place of Birth", res["birth_place"])
            ehh = b3.text_input("Household Number / ID", res["household_no"])

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            st.subheader("Address & Community Ties")
            ecit = st.text_input("Citizenship", res["citizenship"])
            eaddr = st.text_area("Complete Address", res["address"])
            
            a1, a2, a3 = st.columns(3)
            edur = a1.text_input("Duration of Residence", res["duration_residence"])
            
            default_purok_idx = PUROK_OPTS.index(res["purok"]) if res["purok"] in PUROK_OPTS else 0
            epurok = a2.selectbox("Purok / Sitio Zone", PUROK_OPTS, index=default_purok_idx)
            
            eres_st = a3.selectbox("Residency Status", STATUS_OPTS, index=STATUS_OPTS.index(res["residency_status"]) if res["residency_status"] in STATUS_OPTS else 0)
            eocc = st.text_input("Occupation", res["occupation"])
            
            st.markdown('</div>', unsafe_allow_html=True)

            
            st.write("---")
            btn1, btn2 = st.columns(2)
            if btn1.form_submit_button("Cancel", use_container_width=True):
                st.session_state.sub_page = "View"
                st.rerun()
            if btn2.form_submit_button("Save Structural Changes", use_container_width=True):
                updated_age = calculate_age(edob_date)
                edob_str = edob_date.strftime("%Y-%m-%d")
                active_editor = st.session_state.username
                
                with sqlite3.connect("Residents.db") as conn:
                    conn.execute("""
                        UPDATE residents SET 
                            surname=?, first_name=?, middle_name=?, dob=?, birth_place=?, household_no=?,
                            sex=?, address=?, duration_residence=?, residency_status=?, civil_status=?, 
                            citizenship=?, occupation=?, age=?, purok=?, last_modified_by=?
                        WHERE id=?
                    """, (eln, efn, emn, edob_str, ebp, ehh, esex, eaddr, edur, eres_st, eciv, ecit, eocc, updated_age, epurok, active_editor, rid))
                    conn.commit()
                st.success("Changes saved successfully!")
                st.session_state.sub_page = "View"
                st.switch_page(st.session_state.home_route)
