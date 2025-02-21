import os
import google.generativeai as genai
import streamlit as st

# Load Gemini API Key securely
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ Gemini API key is missing! Set it using environment variables.")
    st.stop()

# Configure Gemini AI
genai.configure(api_key=api_key)

# Streamlit UI - Custom Styling
st.set_page_config(page_title="Gemini Resume Generator", page_icon="📄", layout="wide")

st.markdown(
    """
    <style>
        .main { background-color: #f4f4f4; }
        .title { text-align: center; font-size: 32px; font-weight: bold; color: #2E3B4E; }
        .subtitle { text-align: center; font-size: 18px; color: #555; }
        .stButton>button { background-color: #2E86C1; color: white; font-size: 18px; padding: 10px; width: 100%; border-radius: 5px; }
        .stTextInput>div>div>input, .stTextArea>div>textarea { font-size: 16px; padding: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="title">🤖 Gemini AI-Powered Resume Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Create a professional resume instantly!</p>', unsafe_allow_html=True)

# Layout with columns
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.subheader("Enter Resume Details")
    name = st.text_input("Full Name", placeholder="E.g., John Doe")
    job_title = st.text_input("Target Job Title", placeholder="E.g., Data Scientist")
    experience = st.text_area("Work Experience", placeholder="Describe your past experience...")
    skills = st.text_area("Key Skills", placeholder="E.g., Python, Machine Learning, SQL...")

    # Function to generate the resume using Gemini AI
    def generate_resume(name, experience, skills, job_title):
        prompt = f"""
        Generate a professional resume with the following details:
        - Name: {name}
        - Target Job Title: {job_title}
        - Work Experience: {experience}
        - Key Skills: {skills}
        
        Format it properly with sections like Summary, Experience, Skills, and Education.
        """

        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text if response else "⚠ No response from Gemini AI."
        except Exception as e:
            return f"⚠ Error: {str(e)}"

    # Generate Resume Button
    if st.button("🚀 Generate Resume"):
        if name and job_title:
            resume_text = generate_resume(name, experience, skills, job_title)
            st.subheader("📄 Your AI-Generated Resume")
            st.text_area("Generated Resume", resume_text, height=300)

            # Downloadable resume
            st.download_button(
                label="📥 Download Resume",
                data=resume_text,
                file_name=f"{name}_resume.txt",
                mime="text/plain",
            )
        else:
            st.warning("⚠ Please enter at least your name and job title!")

# Instructions for API Key Setup
st.sidebar.subheader("🔑 API Key Setup")
st.sidebar.code('set GEMINI_API_KEY="your-gemini-api-key"', language="bash")