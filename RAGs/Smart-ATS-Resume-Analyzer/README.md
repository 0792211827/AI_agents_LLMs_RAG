# Smart ATS - Resume Analyzer
A Streamlit web application designed to optimize resumes for tech roles using the Google Gemini API. This app evaluates resumes against job descriptions, providing a match percentage, missing keywords, skill breakdowns, and actionable improvement suggestions to enhance ATS (Application Tracking System) compatibility.
## Prerequisites

* Python 3.9 or higher
* A Google Gemini API key (obtain from Google AI Studio)

## Tech Stack

* **Python**
* **Streamlit** (UI Framework)
* **Google Gemini** AI (LLM for resume analysis)
* **PyPDF2** (PDF text extraction)


## Installation
### 1. Clone the Repository
```bash
   git clone https://github.com/0792211827/AI_agents_LLMs_RAG.git
   cd  RAGs/Smart-ATS-Resume-Analyzer
```

### 2. Create a Virtual Environment
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
```
### 3. Install Dependencies
```bash
   pip install -r requirements.txt
```
### 4. Set Up Environment Variables
Create a .env file in the project root and add the following:
```bash
   GEMINI_API_KEY=your_gemini_api_key
```
### 5. Run the Chatbot
```bash
   streamlit run Smart-ATS.py 
```

