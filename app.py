import pandas as pd  # Structure data for the grid view
import streamlit as st
from datetime import datetime  # Imported datetime to track login timestamps
# Import functions from your separate database file
from db_helper import init_db, add_user, verify_user, fetch_users, change_password

# Main app
def main():
    init_db()
    
    # 🎨 POLISHED CSS: Added custom styling for headers and container block overrides
    st.markdown("""
        <style>
        /* Custom styles for the centered main app header bar */
        .main-app-title {
            background: linear-gradient(135deg, #124d0b, #1dfa02);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            font-size: 2.2rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 35px;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2);
            letter-spacing: 1px;
        }

        /* Target standard container border wrapper explicitly */
        div[data-testid="stVerticalBlockBorderDiv"] {
            border: 3px dotted #FF4B4B !important;
            padding: 30px !important;
            border-radius: 12px !important;
            background-color: #ffffff !important;
            box-shadow: none !important;
        }
        
        /* Custom styles for the heading background bar */
        .heading-bar {
            background-color: #124d0b;
            color: white;
            padding: 12px 15px;
            border-radius: 6px;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 25px;
            text-align: center;
        }
        
        /* Sidebar spacing tweaks */
        section[data-testid="stSidebar"] .stButton button {
            margin-bottom: 8px;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🎓 Centered Main Title with its custom nice background bar
    st.markdown('<div class="main-app-title">🎓 STUDENT App</div>', unsafe_allow_html=True)

        # Initialize Session States
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "login_time" not in st.session_state:
        st.session_state.login_time = ""  # New key for tracking timestamp
    if "auth_action" not in st.session_state:
        st.session_state.auth_action = "Login"  
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard" 

    # --- AFTER LOGIN VIEW ---
    if st.session_state.logged_in:
        # 🛠️ SIDEBAR CREATION
        with st.sidebar:
            st.title(f"👋 Hello, {st.session_state.username}!")
            #st.write("📁 **Navigation Menu**")
            
            # --- STACKED VERTICAL MENU BAR WITH ICONS ---
            # Dashboard Menu Item
            db_type = "primary" if st.session_state.current_page == "Dashboard" else "secondary"
            if st.button("📊 Dashboard", type=db_type, use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()

            # Change Password Menu Item
            cp_type = "primary" if st.session_state.current_page == "Change Password" else "secondary"
            if st.button("🔑 Change Password", type=cp_type, use_container_width=True):
                st.session_state.current_page = "Change Password"
                st.rerun()

            # Analytics Menu Item
            an_type = "primary" if st.session_state.current_page == "Analytics" else "secondary"
            if st.button("📈 Analytics", type=an_type, use_container_width=True):
                st.session_state.current_page = "Analytics"
                st.rerun()
            
            st.markdown("---")
            # 🚪 Log Out button label
            if st.button("🚪 Log Out", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.login_time = "" # Reset timestamp on logout
                st.session_state.current_page = "Dashboard"  # Reset page route
                st.rerun()

        # Main Page Content based on current_page selection state
        st.success(f"Welcome back, {st.session_state.username}!")
        st.caption(f"🕒 **Logged in since:** {st.session_state.login_time}")
        
        # 👥 DASHBOARD VIEW 
        if st.session_state.current_page == "Dashboard":
            st.subheader("👥 Dashboard")
            
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
                
        # ⚙️ CHANGE PASSWORD VIEW 
        elif st.session_state.current_page == "Change Password":
            #st.subheader("⚙️ Change Password")
            
            col1, col2, col3 = st.columns([1, 1.8, 1])
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
                            if verify_user(st.session_state.username, current_password):
                                try:
                                    change_password(st.session_state.username, new_password)
                                    st.success("Password updated successfully!")
                                except Exception as e:
                                    st.error(f"Database error: {e}")
                            else:
                                st.error("Incorrect current password.")

        # 📊 ANALYTICS VIEW
        else:
            st.write(f"This is your personalized {st.session_state.current_page.lower()} view.")
        
    # --- BEFORE LOGIN VIEW (LOGIN / SIGNUP ONLY) ---
    else:
        # Fixed layout structure using proportional columns
        col1, col2, col3 = st.columns([1, 1.8, 1])
        
        with col2:
            # One continuous box grouping buttons and fields cleanly together
            with st.container(border=True):
                
                # 🔘 ACTION TOGGLE BUTTONS
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

                st.markdown("<hr style='margin: 15px 0; border: 0; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

                # Render selected form fields
                if st.session_state.auth_action == "Login":
                    st.markdown('<div class="heading-bar">Login Section</div>', unsafe_allow_html=True)
                    username = st.text_input("👤 Username")
                    password = st.text_input("👁️ Password", type="password")
                    
                    if st.button("Login", use_container_width=True):
                        if verify_user(username, password):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            # ⏰ UPDATED: Captures the timestamp right upon successful auth verification
                            st.session_state.login_time = datetime.now().strftime("%d-%b-%Y %I:%M %p")
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")

                elif st.session_state.auth_action == "Sign Up":
                    st.markdown('<div class="heading-bar">Create New Account</div>', unsafe_allow_html=True)
                    new_user = st.text_input("👤 Choose Username")
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

if __name__ == "__main__":
    main()