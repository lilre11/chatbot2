@echo off
echo Starting AI Chatbot Application...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure your settings.
    echo.
    pause
    exit /b 1
)

REM Start the Flask application
echo Starting Flask development server...
python app.py

pause
