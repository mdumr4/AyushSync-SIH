import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Edge-Native Terminology Service",
    page_icon="⚕️",
    layout="wide" # Use wide layout for the dashboard
)

# --- App State Management ---
if 'page' not in st.session_state:
    st.session_state.page = "Live Demo"

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
if st.sidebar.button("Live Demo", use_container_width=True):
    st.session_state.page = "Live Demo"
if st.sidebar.button("Analytics Dashboard", use_container_width=True):
    st.session_state.page = "Analytics Dashboard"

# --- API Configuration ---
FASTAPI_URL = "http://127.0.0.1:8000"

# ==============================================================================
# --- Page 1: Live Demo ---
# ==============================================================================
if st.session_state.page == "Live Demo":
    st.title("⚕️ Live Demo: Voice-to-Code")
    st.write("Use the recorder to capture a diagnosis or the text box to search.")

    # --- Voice Input ---
    st.subheader("Record Diagnosis with Voice")
    audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key='recorder')

    if audio:
        st.write("**Audio captured!** Processing...")
        files = {'audio_file': ('audio.wav', audio['bytes'], 'audio/wav')}
        try:
            with st.spinner("Sending audio for AI analysis..."):
                response = requests.post(f"{FASTAPI_URL}/transcribe", files=files)
                response.raise_for_status()
                ai_results = response.json()

            st.success("**AI Analysis Complete:**")
            st.info(f"**Transcribed Text:** *{ai_results.get('transcribed_text')}*")
            st.write("**Found Clinical Terms:**")
            st.table(ai_results.get('found_terms', []))

        except requests.exceptions.RequestException as e:
            st.error(f"Error during AI processing: {e}")

    # --- Text Search ---
    st.subheader("Or, Search by Text")
    search_query = st.text_input("Enter a term to search", "")

    if search_query:
        try:
            response = requests.get(f"{FASTAPI_URL}/lookup", params={"filter": search_query})
            response.raise_for_status()
            results = response.json()
            st.write("**Search Results:**")
            if isinstance(results, list):
                st.table(results)
            elif isinstance(results, dict) and 'message' in results:
                st.info(results['message'])
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the backend API: {e}")

# ==============================================================================
# --- Page 2: Analytics Dashboard ---
# ==============================================================================
elif st.session_state.page == "Analytics Dashboard":
    st.title("📊 Visionary Analytics Dashboard")
    st.write("This is a mock dashboard showcasing the potential national-level insights.")
    st.info("This data is for demonstration purposes only.")

    # Create mock data for the chart
    mock_data = {
        'Condition': ['Jvara (Fever)', 'Kasa (Cough)', 'Atisara (Diarrhoea)', 'Sudah (Headache)', 'Svasa (Dyspnoea)'],
        'Reported Cases': [1200, 850, 600, 1500, 400],
        'Region': ['North', 'South', 'East', 'West', 'Central']
    }
    df = pd.DataFrame(mock_data)

    st.subheader("Top 5 Reported Conditions (Mock Data)")
    st.bar_chart(df.set_index('Condition')['Reported Cases'])

    st.subheader("Geographic Distribution (Mock Data)")
    st.map(pd.DataFrame({
        'lat': [28.6139, 19.0760, 22.5726, 12.9716, 26.8467],
        'lon': [77.2090, 72.8777, 88.3639, 77.5946, 80.9462],
        'size': [150, 100, 70, 50, 80] # Size represents case volume
    }), size='size', zoom=4)

    st.write("--- End of Prototype ---")