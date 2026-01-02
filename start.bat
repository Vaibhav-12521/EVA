@echo off
echo Starting AI Chatbot with UI...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with the following content:
    echo.
    echo Username=YourName
    echo Assistantname=AI Assistant
    echo GroqAPIKey=your_groq_api_key_here
    echo.
    echo Press any key to continue anyway...
    pause
)

REM Start the Flask server
echo Starting the web server...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause