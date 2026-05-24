import streamlit as st
import pandas as pd
import sqlite3
from frontend import apply_style

apply_style("accounts")

st.title("Account Management Workspace")

# Admin access check
if st.session_state.access_level != "Admin":
    st.error("🔒 Access Denied: You do not have permission to view or manage system user accounts.")
    st.stop()

# Initialized view state tabs
tab1, tab2 = st.tabs(["👥 Active User Accounts", "➕ Register New Account"])

ROLE_OPTS = ["Admin", "Editor", "Viewer"]

# Tab1 (Active User Accounts)
with tab1:
    st.subheader("System Account Directory")
    
    # Search account
    search_acc = st.text_input("Search Users by Full Name", placeholder="Type name here...")
    
    with sqlite3.connect("Users.db") as conn:
        query = "SELECT id, fullname, sex, username, access_level FROM users WHERE 1=1"
        params = []
        if search_acc:
            query += " AND fullname LIKE ?"
            params.append(f"%{search_acc}%")
        df = pd.read_sql_query(query, conn, params=params)

    st.markdown("---")
    
    if df.empty:
        st.info("No matching system user accounts found.")
    else:
        for _, row in df.iterrows():
            col_info, col_actions = st.columns(2)
            
            # Prevents the current logged-in user from changing their own role or deleting themselves
            is_self = (row["username"] == st.session_state.username)
            user_id = int(row["id"])
            username_str = row["username"]
            current_role = row["access_level"]
            
            with col_info:
                self_badge = " *(You)*" if is_self else ""
                st.markdown(f"### {row['fullname']}{self_badge}")
                st.markdown(f"**Username:** `{username_str}` | **Sex:** {row['sex']} | **Role:** `{current_role}`")
            
            with col_actions:
                # Role Change Toolblock
                with st.expander("🛠️ Change Role", expanded=False):
                    if is_self:
                        st.warning("You cannot change your own permission level role to preserve session stability.")
                    else:
                        st.write(f"Assign a new access level role to `{username_str}`:")
                        # Find the index of the user's current role to set as default selectbox option
                        default_role_idx = ROLE_OPTS.index(current_role) if current_role in ROLE_OPTS else 2
                        
                        with st.form(key=f"role_form_{user_id}"):
                            new_role = st.selectbox(
                                "Select Access Level", 
                                ROLE_OPTS, 
                                index=default_role_idx, 
                                key=f"role_val_{user_id}"
                            )
                            
                            if st.form_submit_button("Update Role", use_container_width=True):
                                with sqlite3.connect("Users.db") as conn:
                                    conn.execute("UPDATE users SET access_level = ? WHERE id = ?", (new_role, user_id))
                                    conn.commit()
                                st.success(f"Role updated to `{new_role}` for user `{username_str}`!")
                                st.rerun()

                # Password Reset Toolblock
                with st.expander("🔄 Reset Password", expanded=False):
                    st.write(f"Change password for `{username_str}`:")
                    with st.form(key=f"pw_form_{user_id}"):
                        new_pw = st.text_input("New Password", type="password", key=f"new_pw_val_{user_id}")
                        confirm_new_pw = st.text_input("Confirm Password", type="password", key=f"conf_pw_val_{user_id}")
                        
                        if st.form_submit_button("Update Password", use_container_width=True):
                            if not new_pw:
                                st.error("Password cannot be blank.")
                            elif new_pw != confirm_new_pw:
                                st.error("Passwords do not match!")
                            else:
                                with sqlite3.connect("Users.db") as conn:
                                    conn.execute("UPDATE users SET password = ? WHERE id = ?", (new_pw, user_id))
                                    conn.commit()
                                st.success(f"Password updated for `{username_str}`!")
                
                # 3. Permanent Account Deletion Toolblock
                if is_self:
                    st.button("🔒 Locked", key=f"lock_{user_id}", disabled=True, use_container_width=True, help="You cannot delete your own active session account profile.")
                else:
                    with st.expander("⚠️ Delete User Account", expanded=False):
                        confirm_del = st.checkbox("Confirm Deletion", key=f"chk_del_user_{user_id}", help="Check this box to unlock the permanent erase button.")
                        
                        if confirm_del:
                            if st.button("Delete User Account", key=f"btn_del_user_{user_id}", type="primary", use_container_width=True):
                                with sqlite3.connect("Users.db") as conn:
                                    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                                    conn.commit()
                                st.success(f"Security profile for `{username_str}` wiped successfully!")
                                st.rerun()
                        else:
                            st.button("Delete User Account", key=f"btn_del_user_dis_{user_id}", type="primary", disabled=True, use_container_width=True)
            st.markdown("---")

# Tab2 (Create/Register New Account)
with tab2:
    st.subheader("Create / Register New System Profile Account")
    st.markdown("Fill out the following fields to provision new administrative credentials.")
    
    with st.form("new_acc_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        fn = c1.text_input("First Name")
        mn = c2.text_input("Middle Name")
        ln = c3.text_input("Last Name")
        
        sx = st.selectbox("Sex", ["Male", "Female"])
        un = st.text_input("Username Access ID")
        pw = st.text_input("Password String", type="password")
        cpw = st.text_input("Confirm Password", type="password")
        al = st.selectbox("Access Level Permission Group", ROLE_OPTS, index=2)
        
        st.write("---")
        if st.form_submit_button("Register System User Profile", use_container_width=True):
            errors = []

            # Name validations
            if not fn.strip():
                errors.append("First Name is required.")
            elif not fn.strip().replace(" ", "").isalpha():
                errors.append("First Name must contain letters only.")

            if not mn.strip():
                errors.append("Middle Name is required.")
            elif not mn.strip().replace(" ", "").isalpha():
                errors.append("Middle Name must contain letters only.")

            if not ln.strip():
                errors.append("Last Name is required.")
            elif not ln.strip().replace(" ", "").isalpha():
                errors.append("Last Name must contain letters only.")

            # Username validation
            if not un.strip():
                errors.append("Username is required.")
            elif len(un.strip()) < 4:
                errors.append("Username must be at least 4 characters long.")
            elif " " in un:
                errors.append("Username must not contain spaces.")

            # Password validation
            if not pw:
                errors.append("Password is required.")
            elif len(pw) < 6:
                errors.append("Password must be at least 6 characters long.")
            elif pw != cpw:
                errors.append("Passwords do not match.")

            if not cpw:
                errors.append("Please confirm your password.")

            if errors:
                for err in errors:
                    st.error(f"⚠️ {err}")
            else:
                full_name = f"{fn.strip()} {mn.strip()} {ln.strip()}"
                try:
                    with sqlite3.connect("Users.db") as conn:
                        conn.execute(
                            "INSERT INTO users (fullname, sex, username, password, access_level) VALUES (?,?,?,?,?)",
                            (full_name, sx, un.strip(), pw, al)
                        )
                        conn.commit()
                    st.success(f"✅ Profile created for `{un.strip()}` with `{al}` authorization rights.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("⚠️ Username already taken or registered in the database directory.")