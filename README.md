# smart-ats-resume-analyzer
AI-powered Resume Analyzer that uses Gemini Pro Vision to evaluate, match, and optimize resumes for job descriptions with ATS insights.

**Smart ATS Resume Analyzer**
A smart, AI-powered Resume Application Tracking System that leverages **Google's Gemini Pro Vision API** to evaluate resumes against job descriptions. It helps job seekers optimize their resumes for **ATS (Applicant Tracking Systems)** by offering:
a)Resume summaries: Reads and extracts content from the uploaded PDF resume.
b)Match percentages: Calculates how closely your resume aligns with the job description using AI-driven analysis.
c)Missing keyword detection: Identifies important job-specific keywords that are absent in your resume.
d)Skill gap analysis: Highlights the skills required by the job that are missing or underrepresented in your resume.
e)Detailed HR-style feedback: Provides professional feedback on your resume from an HR perspective, including strengths and weaknesses.

**Tech Stack Used**
a)Python: Backend logic and integration
b)Streamlit: UI/UX for web app 
c)Gemini Pro Vision: Google AI model for resume analysis
d)PDF2Image, PIL: Resume file handling and rendering 

**How to Run Locally??**

1. **Clone the repo**  
git clone https://github.com/Frozenfever4/smart-ats-resume-analyzer.git
cd smart-ats-resume-analyzer

2. **Install dependencies**
pip install -r requirements.txt

3. **Create a .env file**
Add your Google API key to a .env file:
GOOGLE_API_KEY=your_gemini_api_key_here

4. **Run the app**
streamlit run app.py

