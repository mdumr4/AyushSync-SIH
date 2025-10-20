import sqlite3
from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import shutil
import torch
from transformers import pipeline
import spacy

# --- AI Model Loading ---
@torch.no_grad()
def load_models():
    print("Loading AI models...")
    transcriber = pipeline("automatic-speech-recognition", model="distil-whisper/distil-small.en")
    nlp = spacy.load("en_core_web_sm")
    print("AI models loaded successfully.")
    return transcriber, nlp

transcriber, nlp = load_models()

# --- Project Setup ---
PROTOTYPE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROTOTYPE_DIR, 'terminology.db')

app = FastAPI(
    title="Edge-Native Terminology Service",
    description="An offline-first service to harmonize NAMASTE and ICD-11 terminologies.",
    version="0.1.0",
)

# --- Database Connection ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Internal Helper Functions ---
def find_terms_in_db(terms: list[str]):
    if not terms:
        return []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build a query that searches for any of the terms in the description or term_name
    query_parts = []
    params = []
    for term in terms:
        query_parts.append("TERM_NAME LIKE ? OR DESCRIPTION LIKE ?")
        params.extend([f"%{term}%", f"%{term}%"])
    
    query = f"SELECT * FROM terminology_map WHERE {' OR '.join(query_parts)}"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    # Use a dictionary to store unique results by NAMASTE_CODE
    unique_results = {dict(row)['NAMASTE_CODE']: dict(row) for row in results}
    
    return list(unique_results.values())

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Edge-Native Terminology Service!"}


@app.get("/lookup")
def search_terminology(filter: str):
    if not filter:
        raise HTTPException(status_code=400, detail="A 'filter' query parameter is required.")
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM terminology_map WHERE term_name LIKE ? OR description LIKE ?"
    search_term = f"%{filter}%"
    cursor.execute(query, (search_term, search_term))
    results = cursor.fetchall()
    conn.close()
    if not results:
        return {"message": "No results found."}
    return [dict(row) for row in results]


@app.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    temp_audio_path = os.path.join(PROTOTYPE_DIR, "temp_audio.wav")
    with open(temp_audio_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)

    transcription_result = transcriber(temp_audio_path)
    transcribed_text = transcription_result['text']
    print(f"Transcription: '{transcribed_text}'")

    # IMPROVED LOGIC: Use spaCy to get all nouns, verbs, and adjectives as potential terms
    doc = nlp(transcribed_text.lower()) # process in lowercase
    potential_terms = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ', 'VERB']]
    print(f"Found potential terms: {potential_terms}")

    found_terms_in_db = find_terms_in_db(potential_terms)
    print(f"Found matching codes in DB: {found_terms_in_db}")

    return {
        "transcribed_text": transcribed_text,
        "found_terms": found_terms_in_db
    }