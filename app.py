import sqlite3
import streamlit as st
# Import functions from your separate database file
from db_helper import init_db, add_user, verify_user, fetch_users

# Main app
def main():
    init_db()
    st.title("🔒 Login and Signup App")

    # Injecting Custom CSS for container borders and text adjustments
    st.markdown("""
        <style>
        /* Forces the container borders to be dotted red */
        [data-testid="stVerticalBlockBorderDiv"] {
            border: 3px dotted #FF4B4B !important;
            padding: 25px !important;
            border-radius: 10px !important;
        }
        
        /* Custom styles for the heading background bar */
        .heading-bar {
            background-color: #FF4B4B; /* Red background bar matching the border */
            color: white;              /* White text color */
            padding: 10px 15px;        /* Padding inside the bar */
            border-radius: 5px;        /* Rounded corners for the bar */
            font-size: 1.3rem;         /* Clean header size */
            font-weight: bold;
            margin-bottom: 20px;       /* Gap between heading and input fields */
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Session state for login status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.success(f"👋 Welcome back, {st.session_state.username}!")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    else:
        choice = st.selectbox("Choose Action", ["Login", "Sign Up"])

        if choice == "Login":
            # FIXED: Added [1, 2, 1] weight argument spec. 
            # This makes the middle column take up 50% of the screen width.
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                with st.container(border=True):
                    # Styled HTML heading bar
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

        elif choice == "Sign Up":
            # FIXED: Added [1, 2, 1] weight argument spec here as well.
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.container(border=True):
                    # Styled HTML heading bar for Sign Up
                    st.markdown('<div class="heading-bar">Create New Account</div>', unsafe_allow_html=True)
                    
                    new_user = st.text_input("👤Choose Username")
                    new_password = st.text_input("🔒 Choose Password", type="password")

                    if st.button("Sign Up", use_container_width=True):
                        if new_user.strip() == "" or new_password.strip() == "":
                            st.warning("Please fill in all fields")
                        elif add_user(new_user, new_password):
                            st.success("Account created successfully! Please log in.")
                        else:
                            st.error("Username already exists. Choose another.")

if __name__ == '__main__':
    main()
