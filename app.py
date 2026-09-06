import sqlite3
import streamlit as st

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a new user
def add_user(username, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Verify user credentials
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Main app
def main():
    init_db()
    st.title("Login and Signup App")

    # Injecting Custom CSS for the dotted border box
    st.markdown("""
        <style>
        .dotted-box {
            border: 3px dotted #FF4B4B; /* Change color here */
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Session state for login status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.username}!")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    else:
        choice = st.selectbox("Choose Action", ["Login", "Sign Up"])

        if choice == "Login":
            st.subheader("Login Section")
            
            # Using st.container with a custom CSS wrapper class
            with st.container(border=False):
                st.markdown('<div class="dotted-box">', unsafe_allow_html=True)
                
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                if st.button("Login"):
                    if verify_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                        
                st.markdown('</div>', unsafe_allow_html=True)

        elif choice == "Sign Up":
            st.subheader("Create New Account")
            new_user = st.text_input("Choose Username")
            new_password = st.text_input("Choose Password", type="password")

            if st.button("Sign Up"):
                if new_user.strip() == "" or new_password.strip() == "":
                    st.warning("Please fill in all fields")
                elif add_user(new_user, new_password):
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("Username already exists. Choose another.")

if __name__ == '__main__':
    main()
