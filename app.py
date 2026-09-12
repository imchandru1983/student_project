import sqlite3
import pandas as pd  # Structure data for the grid view
import streamlit as st
# Import functions from your separate database file
# TIP: Add your password update function to this import statement if it exists (e.g., update_password)
from db_helper import init_db, add_user, verify_user, fetch_users, change_password

# Main app
def main():
    init_db()
    
    st.title("🔒 Login and Signup App")

    # Injecting Custom CSS for container borders and text adjustments
    st.markdown("""
        <style>
        [data-testid="stVerticalBlockBorderDiv"] {
            border: 3px dotted #FF4B4B !important;
            padding: 25px !important;
            border-radius: 10px !important;
        }
        .heading-bar {
            background-color: #FF4B4B;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize Session States
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "auth_action" not in st.session_state:
        st.session_state.auth_action = "Login"  # Default view

    # --- AFTER LOGIN VIEW ---
    if st.session_state.logged_in:
        # 🛠️ SIDEBAR CREATION
        with st.sidebar:
            st.title(f"👋 Hello, {st.session_state.username}!")
            st.write("Navigate through the app using the menu below:")
            
            page = st.radio("Go to Page", ["Dashboard", "Change Password", "Analytics"])
            
            st.markdown("---")
            if st.button("Log Out", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.rerun()

        # Main Page Content based on Sidebar Selection
        st.success(f"Welcome back, {st.session_state.username}!")
        #st.header(f"📌 {page} Section")
        
        # 👥 DASHBOARD VIEW 
        if page == "Dashboard":
            st.subheader("👥 Registered Users Directory")
            
            try:
                raw_users = fetch_users()
                if raw_users:
                    df = pd.DataFrame(raw_users, columns=["Username", "Password Hash"])
                    df_display = df[["Username"]]  # Keep hash hidden
                    
                    st.dataframe(
                        df_display, 
                        use_container_width=True, 
                        hide_index=True
                    )
                    st.metric(label="Total Registered Users", value=len(df_display))
                else:
                    st.info("No registered users found in the database.")
            except Exception as e:
                st.error(f"Error loading dashboard directory: {e}")
                
        # ⚙️ PROFILE SETTINGS VIEW (WITH CHANGE PASSWORD SECTION)
        elif page == "Change Password":
            st.subheader("⚙️ Change Password")
            
            # Using columns to center the profile card layout nicely
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.container(border=True):
                    st.markdown('<div class="heading-bar">Change Password</div>', unsafe_allow_html=True)
                    
                    current_password = st.text_input("🔑 Current Password", type="password")
                    new_password = st.text_input("🆕 New Password", type="password")
                    confirm_password = st.text_input("🔁 Confirm New Password", type="password")
                    
                    if st.button("Update Password", use_container_width=True):
                        if current_password.strip() == "" or new_password.strip() == "" or confirm_password.strip() == "":
                            st.warning("Please fill in all fields.")
                        elif new_password != confirm_password:
                            st.error("New passwords do not match!")
                        elif new_password == current_password:
                            st.warning("New password cannot be the same as your old password.")
                        else:
                            # 1. First verify if the old password is correct
                            if verify_user(st.session_state.username, current_password):
                                
                                # 2. Update the password in SQLite
                                try:
                                    change_password(st.session_state.username, new_password)
                                    st.success("Password updated successfully!")
                                except Exception as e:
                                    st.error(f"Database error: {e}")
                            else:
                                st.error("Incorrect current password.")

        # 📊 ANALYTICS VIEW
        else:
            st.write(f"This is your personalized {page.lower()} view.")
        
    # --- BEFORE LOGIN VIEW (LOGIN / SIGNUP ONLY) ---
    else:
        # ACTION TOGGLE BUTTONS
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            login_type = "primary" if st.session_state.auth_action == "Login" else "secondary"
            if st.button("🔑 Go to Login", type=login_type, use_container_width=True):
                st.session_state.auth_action = "Login"
                st.rerun()
                
        with btn_col2:
            signup_type = "primary" if st.session_state.auth_action == "Sign Up" else "secondary"
            if st.button("📝 Go to Sign Up", type=signup_type, use_container_width=True):
                st.session_state.auth_action = "Sign Up"
                st.rerun()

        st.write("") # Spacer

        # Render form based on selection
        if st.session_state.auth_action == "Login":
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.container(border=True):
                    st.markdown('<div class="heading-bar">Login Section</div>', unsafe_allow_html=True)
                    username = st.text_input("👤Username")
                    password = st.text_input("👁️Password", type="password")
                    
                    if st.button("Login", use_container_width=True):
                        if verify_user(username, password):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")

        elif st.session_state.auth_action == "Sign Up":
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.container(border=True):
                    st.markdown('<div class="heading-bar">Create New Account</div>', unsafe_allow_html=True)
                    new_user = st.text_input("👤Choose Username")
                    new_password = st.text_input("🔒 Choose Password", type="password")
                    
                    if st.button("Sign Up", use_container_width=True):
                        if new_user.strip() == "" or new_password.strip() == "":
                            st.warning("Please fill in all fields")
                        elif add_user(new_user, new_password):
                            st.success("Account created successfully! Please log in.")
                            st.session_state.auth_action = "Login"
                            st.rerun()
                        else:
                            st.error("Username already exists. Choose another.")

if __name__ == '__main__':
    main()
