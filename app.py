import streamlit as st

# Inject custom CSS to change the background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 My Free Streamlit Website")
st.write("Hello world! This website is running on Python.")
