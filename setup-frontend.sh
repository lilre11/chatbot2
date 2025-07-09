#!/bin/bash
echo "Setting up React Frontend..."
echo

cd frontend

echo "Installing Node.js dependencies..."
npm install

echo
echo "Frontend setup complete!"
echo
echo "To start the React development server:"
echo "  cd frontend"
echo "  npm start"
echo
echo "The React app will run on http://localhost:3000"
echo "Make sure the Flask backend is running on http://localhost:5000"
