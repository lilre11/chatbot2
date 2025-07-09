@echo off
echo Starting AI Chatbot Full-Stack Application...
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure your settings.
    echo.
    pause
    exit /b 1
)

echo Starting Flask Backend Server...
start "Flask Backend" cmd /c "call .venv\Scripts\activate.bat && python app.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting React Frontend Server...
start "React Frontend" cmd /c "cd frontend && npm start"

echo.
echo ================================
echo AI Chatbot Application Starting
echo ================================
echo Backend (Flask API): http://localhost:5000
echo Frontend (React SPA): http://localhost:3000
echo.
echo Both servers are starting in separate windows.
echo Close those windows to stop the servers.
echo.
pause
