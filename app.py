from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt_text, pdf_content, job_description):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt_text, pdf_content[0], job_description])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        return [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit Page Config
st.set_page_config(page_title="Smart ATS Resume Scanner", page_icon="📄", layout="centered")

# ----- Custom CSS Styling -----
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }

    h1 {
        font-size: 38px !important;
        color: #1a237e !important;
    }

    p, .stTextArea textarea {
        font-size: 18px !important;
    }

    .stButton>button {
        background: linear-gradient(to right, #1e88e5, #42a5f5);
        color: white;
        padding: 10px 22px;
        font-size: 17px;
        font-weight: 500;
        border-radius: 10px;
        border: none;
        margin: 10px 5px;
        transition: background 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background: linear-gradient(to right, #1976d2, #2196f3);
        transform: scale(1.02);
    }

    .analysis-mode .stButton {
        display: flex;
        justify-content: center;
    }

    .small-text {
        font-size: 15px;
        color: gray;
        text-align: center;
        margin-top: 15px;
    }

    .description {
        font-size: 19px;
        color: #333;
        text-align: justify;
        margin-top: 10px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# ----- App Title & Intro -----
st.markdown("<h1 style='text-align: center;'>🤖 Smart ATS Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by Google Gemini Pro Vision · Created with ❤️ by <b>Tanaya Mahalanabis</b></p>", unsafe_allow_html=True)

# Project Description
st.markdown("""
<div class="description">
This AI-powered Resume Application Tracking System leverages Google's Gemini Pro Vision model to analyze resumes against job descriptions. 
It provides insightful feedback, ATS compatibility scores, skill gap analysis, and missing keyword detection – helping job seekers tailor 
their resumes to meet recruiter expectations and improve their chances of getting hired.
</div>
""", unsafe_allow_html=True)

# ----- Inputs -----
input_text = st.text_area("📌 Paste the Job Description Here:", height=180, placeholder="e.g., Looking for a frontend developer with experience in React, TypeScript, and REST APIs...")

uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF format only)", type=["pdf"])
if uploaded_file:
    st.success("✅ Resume uploaded successfully!", icon="📄")

# Prompt Templates
PROMPTS = {
    "tell_resume": """
You are a resume analysis expert. Read the resume and provide a general overview of the candidate's background, technical skills, education, experience, and any notable strengths.
""",
    "evaluate_resume": """
You are an experienced HR manager. Analyze the resume in relation to the job description. Highlight strengths and weaknesses with justification.
""",
    "match_percentage": """
You are an ATS scanner. Compare the resume with the job description and return:
1. Match percentage
2. Missing keywords
3. Final comments
""",
    "improve_skills": """
You are a career coach. Based on the resume and job description, suggest at least 3 specific technical or soft skills the candidate should improve or learn to become a better fit.
""",
    "missing_keywords": """
Compare the resume with the job description and extract important job-specific keywords or technologies missing from the resume.
"""
}

# Output Handler
def handle_request(btn_triggered, prompt_key, title, icon):
    if btn_triggered:
        if uploaded_file and input_text:
            with st.spinner("⏳ Analyzing your resume..."):
                pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(PROMPTS[prompt_key], pdf_content, input_text)
            with st.expander(f"{icon} {title}", expanded=True):
                st.markdown(f"<div style='font-size:17px; color:#444;'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please upload a resume and enter the job description.")

# ----- Analysis Mode -----
st.markdown("<h3 style='text-align: center; margin-top: 30px;'>🔍 Choose Analysis Mode</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    btn_summary = st.button("📘 Tell Me About the Resume")
    btn_evaluate = st.button("📌 Resume Evaluation")
    btn_improve = st.button("🚀 Skill Suggestions")
with col2:
    btn_match = st.button("📊 ATS Match %")
    btn_keywords = st.button("🧩 Missing Keywords")

handle_request(btn_summary, "tell_resume", "Resume Summary", "📘")
handle_request(btn_evaluate, "evaluate_resume", "HR Evaluation", "📌")
handle_request(btn_match, "match_percentage", "ATS Match Percentage & Insights", "📊")
handle_request(btn_improve, "improve_skills", "Skill Enhancement Suggestions", "🚀")
handle_request(btn_keywords, "missing_keywords", "Missing Keywords from Resume", "🧩")

# ----- Footer -----
st.markdown("---")
st.markdown("""
<div class="small-text">
    &copy; 2025 <b>Tanaya Mahalanabis</b>. All rights reserved. · Built with Streamlit & Google Gemini Pro Vision
</div>
""", unsafe_allow_html=True)
