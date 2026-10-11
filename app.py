import base64
import email
import io
import re
import pandas as pd  # Structure data for the grid view
import streamlit as st
from PIL import Image
from datetime import datetime, date  # Imported datetime to track login timestamps
from db_helper import init_db, add_user, verify_user, fetch_users, change_password, fetch_applications, add_application, delete_applications, update_application_field
import requests

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

            # Contact Us Menu Item
            cu_type = "primary" if st.session_state.current_page == "Contact Us" else "secondary"
            if st.button("� Contact Us", type=cu_type, use_container_width=True):
                contact_form()  # Call the contact form dialog

            # Import Data Menu Item
            import_type = "primary" if st.session_state.current_page == "Import Data" else "secondary"
            if st.button("📥 Import Data", type=import_type, use_container_width=True):
                st.session_state.current_page = "Import Data"
                st.rerun()

            # Open Google Menu Item
            open_google = "primary" if st.session_state.current_page == "Open Google" else "secondary"
            if st.button("🌐 Open Google", type=open_google, use_container_width=True):
                st.session_state.current_page = "Open Google"
                st.rerun()

            # Profile Picture Menu Item
            profile_picture = "primary" if st.session_state.current_page == "Profile Picture" else "secondary"
            if st.button("👤 Profile Picture", type=profile_picture, use_container_width=True):
                st.session_state.current_page = "Profile Picture"
                st.rerun()

            # Run Video Menu Item
            run_video = "primary" if st.session_state.current_page == "Run Video" else "secondary"
            if st.button("🎥 Run Video", type=run_video, use_container_width=True):
                st.session_state.current_page = "Run Video"
                st.rerun()

            # Apply Online Menu Item
            apply_online = "primary" if st.session_state.current_page == "Apply Online" else "secondary"
            if st.button("🎥 Apply Online", type=apply_online, use_container_width=True):
                st.session_state.current_page = "Apply Online"
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
        elif st.session_state.current_page == "Analytics":
            st.write(f"This is your personalized {st.session_state.current_page.lower()} view.")

        # 📥 IMPORT DATA VIEW
        elif st.session_state.current_page == "Import Data":
            import_form()

        # 🌐 OPEN GOOGLE VIEW
        elif st.session_state.current_page == "Open Google":
            # This opens Google in a new tab when clicked
            st.link_button("Go to Google", "https://www.google.com")
            
        # 🌐 PROFILE PICTURE VIEW
        elif st.session_state.current_page == "Profile Picture":
            # This opens Google in a new tab when clicked
            load_picture()

        # 🎥 RUN VIDEO VIEW
        elif st.session_state.current_page == "Run Video":
            load_video()

        # 🎥 APPLY ONLINE VIEW
        elif st.session_state.current_page == "Apply Online":
            load_apply_online()

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

@st.dialog("Contact Us")
def contact_form():
    st.write("Please fill out the form below to get in touch with us.")
    
    # Form input fields
    name = st.text_input("Your Name", placeholder="John Doe")
    email = st.text_input("Your Email", placeholder="john@example.com")
    message = st.text_area("Your Message", placeholder="Type your message here...")
    
    # Target email configuration via FormSubmit
    # Replace with your actual email address
    YOUR_EMAIL = "your_email@example.com" 
    FORM_SUBMIT_URL = f"https://formsubmit.co{YOUR_EMAIL}"

    if st.button("Submit"):
        if not name or not email or not message:
            st.error("Please fill out all fields.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            # Prepare payload for backend email processing
            payload = {
                "name": name,
                "email": email,
                "message": message
            }
            
            try:
                # Send the data asynchronously to the email endpoint
                response = requests.post(FORM_SUBMIT_URL, json=payload)
                if response.status_code == 200:
                    st.success("Thank you! Your message has been sent.")
                    # Optional: Rerun the app to close the dialog automatically after submission
                    st.rerun()
                else:
                    st.error("Failed to send message. Please try again.")
            except Exception as e:
                st.error("An error occurred while sending the message.")

def import_form():
    st.write("Import your data below.")
    
    # File uploader for Excel files
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Read the uploaded Excel file into a DataFrame
            df = pd.read_excel(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(df)  # Display the DataFrame in the app
            
            # Optional: Add functionality to process or save the DataFrame as needed
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")

def load_picture():
    st.write("Upload your profile picture below.")
    
    # File uploader for image files
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # 2. Open the image using PIL
            image = Image.open(uploaded_file)

            # 3. Convert the image to bytes and then to a Base64 string
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # 4. Use HTML and CSS to display the image in a circle
            # Adjust width and height to change the size of your profile picture
            profile_html = f"""
            <div style="display: flex; justify-content: center; margin-top: 20px;">
                <div style="
                    width: 150px; 
                    height: 150px; 
                    border-radius: 50%; 
                    overflow: hidden; 
                    border: 3px solid #4CAF50;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
                ">
                    <img src="data:image/png;base64,{img_str}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
            </div>
            """

            # 5. Render the HTML component
            st.markdown(profile_html, unsafe_allow_html=True)
            # Display the uploaded image
            #st.image(uploaded_file, caption="Uploaded Profile Picture", use_column_width=True)
            #st.success("Profile picture uploaded successfully!")
            
            # Optional: Add functionality to save the image to a database or server
        except Exception as e:
            st.error(f"Error uploading the profile picture: {e}")

def load_video():
    st.write("Watch the video below.")
    
    # Video URL (YouTube or any other source)
    video_url = "https://www.youtube.com/embed/dQw4w9WgXcQ"  # Example YouTube video
    
    # Embed the video using an iframe
    st.markdown(f"""
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
            <iframe src="{video_url}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
                    frameborder="0" 
                    allowfullscreen>
            </iframe>
        </div>
    """, unsafe_allow_html=True)

def load_apply_online():
    st.write("### 📝 Apply Online")

    # Regular expression pattern validation constraints
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    MOBILE_REGEX = r"^(\+?\d{1,3})?[-.\s]?\d{10}$"

    # ==========================================
    # 1. CREATE OPERATION (Input Form)
    # ==========================================
    # Wrapping inputs inside a form prevents premature error alerts while typing
    with st.form("student_apply_form", clear_on_submit=True):
        name = st.text_input("Full Name").strip()
        guardianname = st.text_input("Guardian's Name").strip()
        email_input = st.text_input("Email address", placeholder="example@domain.com").strip()
        
        # Date of birth validation setup
        dob = st.date_input(
            label="Date of birth",
            value=None,                         
            min_value=date(1900, 1, 1),         
            max_value=date.today(),             
            format="DD/MM/YYYY"                 
        )
        
        phone = st.text_input(
            label="Mobile number", 
            placeholder="1234567890",
            max_chars=15 # Increased slightly to accommodate optional country codes
        ).strip()
        
        submit_btn = st.form_submit_button("Submit Application")

    if submit_btn:
        clean_phone = re.sub(r"[-.\s]", "", phone)
        
        if not name or not guardianname or not email_input or not phone:
            st.error("❌ Please fill out all text fields.")
        elif not dob:
            st.error("❌ Please select your Date of Birth.")
        elif not re.match(EMAIL_REGEX, email_input):
            st.error("❌ Please enter a valid email address.")
        elif not re.match(MOBILE_REGEX, clean_phone):
            st.error("❌ Please enter a valid 10-digit mobile number.")
        else:
            # Execute database [CREATE] insertion
            # Storing matching string format as requested: dob.strftime("%d-%b-%Y")
            add_application(st.session_state.username, name, guardianname, dob.strftime("%d-%b-%Y"), clean_phone, email_input)
            st.success("🎉 Your application has been submitted successfully!")
            st.rerun()

    # ==========================================
    # 2. READ, UPDATE, & DELETE OPERATIONS (Data Grid Ledger)
    # ==========================================
    st.write("---")
    st.write("### 📋 Manage Applications Ledger")
    st.caption("💡 Double-click cells to **Update**. Select rows and hit 'Save Changes' below to **Delete** rows permanently.")

    try:
        raw_applications = fetch_applications()  # Fetch student applications from the database
        
        if raw_applications:
            # [READ] Phase: Mount data matrix framework
            df = pd.DataFrame(raw_applications, columns=["Application ID", "Username", "Name", "Guardian's Name", "Date of Birth", "Mobile", "Email", "Submission Date"])
            
            # Inject structural control column checkbox field for tracking deletions
            df.insert(0, "Select to Delete", False)
            
            # Interactive Grid Engine enabling [UPDATE] and selection arrays
            edited_df = st.data_editor(
                df, 
                use_container_width=True, 
                hide_index=True,
                disabled=["Application ID", "Username", "Submission Date"], # Protect operational logs
                column_config={
                    "Select to Delete": st.column_config.CheckboxColumn(required=True)
                }
            )
            
            # Central Execution Pipeline for Saving/Deleting changes
            if st.button("Save Changes to Database", type="primary"):
                
                # A. [DELETE] Operations Engine Processing
                deleted_ids = edited_df[edited_df["Select to Delete"] == True]["Application ID"].tolist()
                if deleted_ids:
                    # Assumes a function like delete_applications(list_of_ids) exists in your backend module
                    delete_applications(deleted_ids) 
                    st.toast(f"Deleted {len(deleted_ids)} application(s)!", icon="🗑️")
                
                # B. [UPDATE] Operations Engine Processing
                for idx, row in edited_df.iterrows():
                    app_id = row["Application ID"]
                    if app_id in deleted_ids:
                        continue # Skip row changes if it was marked for permanent removal
                        
                    old_row = df[df["Application ID"] == app_id].iloc[0]
                    
                    # Track item changes cell-by-cell dynamically
                    for col_name, db_col_field in [
                        ("Name", "name"), 
                        ("Guardian's Name", "guardian_name"), 
                        ("Date of Birth", "dob"), 
                        ("Mobile", "mobile"), 
                        ("Email", "email_address")
                    ]:
                        if str(row[col_name]) != str(old_row[col_name]):
                            # Assumes a flexible column update helper layout: update_application_field(id, col, val)
                            update_application_field(app_id, db_col_field, row[col_name])
                            st.toast(f"Updated {col_name} for ID {app_id}!", icon="✏️")
                
                # Refresh layout completely to display structural storage state modifications
                st.rerun()
                
        else:
            st.info("No applications found in the database.")
            
    except Exception as e:
        st.error(f"Error loading dashboard directory: {e}")

    
if __name__ == "__main__":
    main()