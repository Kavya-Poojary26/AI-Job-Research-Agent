import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Load API Key
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- Function to call Tavily API ---
def search_tavily(query):
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": 5
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def summarise_results(results):
    return [res["content"] for res in results.get("results", [])]

# --- Streamlit Page Config ---
st.set_page_config(page_title="AI Job Research Agent", page_icon="🤖", layout="wide")

# --- Custom CSS for Black Theme ---
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3, h4, h5 {
        color: #00FFB0;
    }
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #444;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #00FFB0;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #00d999;
        transform: scale(1.05);
    }
    .result-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.markdown("<h1>🤖 AI Job Research Agent</h1>", unsafe_allow_html=True)
st.write("Enter a **Company Name** and **Job Role** to get AI-researched insights.")

# --- Inputs ---
company = st.text_input("🏢 Company Name", placeholder="e.g. Infosys")
role = st.text_input("💼 Job Role", placeholder="e.g. Data Scientist")

# --- Button & Processing ---
if st.button("🔍 Research Now"):
    if company and role:
        with st.spinner("Researching... Please wait"):
            company_data = search_tavily(f"{company} company overview size domain headquarters website latest news")
            company_summary = summarise_results(company_data)

            role_data = search_tavily(f"{role} job description skills experience salary {company}")
            role_summary = summarise_results(role_data)

        # --- Results Display ---
        st.markdown(f"<h2>🏢 Company Overview: {company}</h2>", unsafe_allow_html=True)
        for point in company_summary:
            st.markdown(f"<div class='result-box'>• {point}</div>", unsafe_allow_html=True)

        st.markdown(f"<h2>💼 Role Requirements: {role}</h2>", unsafe_allow_html=True)
        for point in role_summary:
            st.markdown(f"<div class='result-box'>• {point}</div>", unsafe_allow_html=True)

    else:
        st.warning("Please enter both Company Name and Job Role.")
