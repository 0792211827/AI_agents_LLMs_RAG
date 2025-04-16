# Gemini Multi-Modal Demo

A simple Streamlit web application demonstrating the capabilities of a multimodal Large Language Model (LLM) using the Google Gemini API. This app allows users to upload an image, provide a text prompt, and receive a response that combines image and text analysis.

## Prerequisites
* Python 3.9 or higher
* A Google Gemini API key (obtain from Google AI Studio)

## Tech Stack

* **Python**

* **Streamlit** (UI Framework)

* **Google Gemini AI** (LLM for response generation)

## Installation
### 1. Clone the Repository
```bash
   git clone https://github.com/0792211827/AI_agents_LLMs_RAG.git
   cd  LLMs/multi-modal-demo
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
   streamlit run multimodal.py 
```


