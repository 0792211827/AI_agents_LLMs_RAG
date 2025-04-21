                        
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re

# Load environment variables from .env file
load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Cache the model to improve performance
@st.cache_resource
def load_gemini_model():
    return genai.GenerativeModel('gemini-1.5-pro')

def get_gemini_response(input_prompt):
    try:
        model = load_gemini_model()
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        st.error(f"Failed to connect to AI model: {str(e)}. Please check your API key or internet connection.")
        return None

def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text
        if not text:
            st.error("No text could be extracted from the PDF. Ensure the file is not scanned or image-based.")
            return None
        # Truncate text to avoid token limits (approx. 10,000 characters)
        return text[:10000]
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}. Ensure the file is a valid PDF.")
        return None

# Enhanced Prompt Template
input_prompt = """
You are an expert ATS (Application Tracking System) with deep expertise in tech fields, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume against the provided job description (JD) in a highly competitive job market. Provide a detailed analysis with the following:

1. **JD Match**: Assign a percentage (0-100%) indicating how well the resume matches the JD, considering skills, experience, and qualifications.
2. **Missing Keywords**: List specific keywords, skills, or tools from the JD that are missing in the resume.
3. **Profile Summary**: Summarize the candidate's strengths and weaknesses relative to the JD.
4. **Improvement Suggestions**: Provide 3-5 actionable recommendations to improve the resume's ATS score, focusing on technical skills, certifications, or project descriptions.
5. **Skill Breakdown**: Categorize matched skills into Technical Skills and Soft Skills.

Resume: {text}
Job Description: {jd}

Return *only* a valid JSON string with the structure below, without any additional text, markdown, or backticks:
{{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": "",
  "Improvement Suggestions": [],
  "Technical Skills Matched": [],
  "Soft Skills Matched": []
}}
"""

# Streamlit App
st.title("Smart ATS - Resume Analyzer")
st.markdown("Optimize your resume for tech roles with AI-powered insights.")

# Input fields
jd = st.text_area("Paste the Job Description", height=200)
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

# Submit button
if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.warning("Please upload a resume.")
    elif not jd or len(jd.strip()) < 50:
        st.warning("Please provide a job description with at least 50 characters.")
    else:
        with st.spinner("Analyzing your resume..."):
            # Extract text from PDF
            resume_text = input_pdf_text(uploaded_file)
            if resume_text:
                # Format prompt with resume and JD
                formatted_prompt = input_prompt.format(text=resume_text, jd=jd)
                
                # Get response from Gemini
                response = get_gemini_response(formatted_prompt)
                
                if response:
                    try:
                        # Clean response (handle various formats)
                        cleaned_response = re.sub(r'```(?:json)?\n?|\n?```', '', response).strip()
                        
                        # Attempt to parse JSON
                        try:
                            result = json.loads(cleaned_response)
                        except json.JSONDecodeError:
                            # Fallback: Try to extract JSON-like content
                            json_match = re.search(r'\{.*\}', cleaned_response, re.DOTALL)
                            if json_match:
                                cleaned_response = json_match.group(0)
                                result = json.loads(cleaned_response)
                            else:
                                raise json.JSONDecodeError("No JSON found in response", cleaned_response, 0)
                        
                        # Store result in session state for download
                        st.session_state['analysis_result'] = result
                        
                        # Display results
                        st.subheader("Analysis Results")
                        
                        # JD Match
                        st.metric("JD Match", f"{result['JD Match']}%")
                        
                        # Expandable sections for detailed results
                        with st.expander("Missing Keywords"):
                            if result['Missing Keywords']:
                                st.write(", ".join(result['Missing Keywords']))
                            else:
                                st.write("All key keywords from JD are present!")
                        
                        with st.expander("Profile Summary"):
                            st.write(result['Profile Summary'])
                        
                        with st.expander("Matched Skills"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Technical Skills**")
                                st.write("- " + "\n- ".join(result['Technical Skills Matched']) if result['Technical Skills Matched'] else "None")
                            with col2:
                                st.write("**Soft Skills**")
                                st.write("- " + "\n- ".join(result['Soft Skills Matched']) if result['Soft Skills Matched'] else "None")
                        
                        with st.expander("Improvement Suggestions"):
                            for idx, suggestion in enumerate(result['Improvement Suggestions'], 1):
                                st.write(f"{idx}. {suggestion}")
                        
                    except json.JSONDecodeError as e:
                        st.error(f"Error parsing response from AI model: {str(e)}")
                        with st.expander("Debug: Raw Response"):
                            st.write(response)
                        with st.expander("Debug: Cleaned Response"):
                            st.write(cleaned_response)
                    except KeyError as e:
                        st.error(f"Missing expected field in response: {str(e)}. Please try again.")

# Download button for analysis results
if 'analysis_result' in st.session_state:
    st.download_button(
        label="Download Analysis (JSON)",
        data=json.dumps(st.session_state['analysis_result'], indent=2),
        file_name="resume_analysis.json",
        mime="application/json"
    )