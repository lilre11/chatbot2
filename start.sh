#!/bin/bash
echo "Starting AI Chatbot Application..."
echo

# Activate virtual environment
source .venv/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your settings."
    echo
    exit 1
fi

# Start the Flask application
echo "Starting Flask development server..."
python app.py
