@echo off
echo 🚀 Starting AI Chatbot Backend...
echo.

cd /d "C:\Users\Emre Yılmaz\Documents\cb2"

echo 🔧 Activating virtual environment...
call ".\.venv\Scripts\activate.bat"

echo 🧪 Testing system...
python test_direct.py

echo.
echo 🌐 Starting Flask server...
echo 📍 Backend will be available at: http://localhost:5000
echo 📍 Health check: http://localhost:5000/api/health
echo 📍 Simple chat test: http://localhost:5000/api/chat/send-simple
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
