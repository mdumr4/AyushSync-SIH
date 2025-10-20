@echo off

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing/Verifying all required packages...
python -m pip install -r prototype\requirements.txt

echo.
echo Downloading required spaCy AI model...
python -m spacy download en_core_web_sm

echo.
echo (Re)Creating the terminology database...
python prototype\scripts\ingest.py

echo.
echo All packages are installed. Starting servers...

echo.
echo Starting Backend API Server (Uvicorn) in a new window...
echo THIS WILL TAKE A MINUTE TO LOAD THE AI MODELS.
start "Backend API" cmd /k python -m uvicorn prototype.main:app --host 0.0.0.0 --port 8000

echo.
echo Starting Frontend UI Server (Streamlit) in a new window...

echo Waiting 30 seconds for backend to initialize...
timeout /t 30 >nul

start "Frontend UI" cmd /k python -m streamlit run prototype/app.py

echo.
echo Two new windows have been opened. Please check the Streamlit window for the URL.