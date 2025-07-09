<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# AI Chatbot Project Instructions

## Project Overview
This is a full-stack chatbot application that integrates:
- **React Frontend** with Bootstrap for responsive UI
- **Python Flask Backend** as REST API server
- **Ubuntu SQL Server** running on a virtual machine
- **Google Gemini AI** API for intelligent responses

## Architecture
### Backend (Flask API)
- `app.py` - Main Flask application factory
- `config.py` - Configuration management with environment variables
- `models.py` - SQLAlchemy database models
- `services/` - Business logic layer (Gemini AI, Database operations)
- `routes/` - API endpoints for chat and admin operations

### Frontend (React)
- `frontend/src/App.js` - Main React application with routing
- `frontend/src/pages/` - React page components (Home, Chat, Admin)
- `frontend/src/components/` - Reusable React components
- `frontend/package.json` - Node.js dependencies and scripts

## Key Features
- Real-time chat interface with React components
- Persistent storage in SQL Server database (with graceful fallback)
- Context-aware AI responses using conversation history
- Admin dashboard with system monitoring
- RESTful API endpoints for all operations
- CORS-enabled backend for React frontend integration
- Automatic fallback when database is unavailable

## Database Schema
- `users` - User accounts and session management
- `conversations` - Chat sessions between users and AI
- `messages` - Individual messages in conversations
- `system_logs` - Application logging and monitoring

## Development Guidelines
- **Frontend**: Use React functional components with hooks
- **Backend**: Follow Flask best practices and blueprints pattern
- **Database**: Use SQLAlchemy ORM with graceful error handling
- **Styling**: Use React Bootstrap components for consistent UI
- **State Management**: Use React hooks (useState, useEffect) for local state
- **API Communication**: Use Axios for HTTP requests to Flask backend
- **Error Handling**: Robust error handling with fallback modes
- **CORS**: Configured for React development server (localhost:3000)

## Configuration
- **Backend**: Flask runs on http://localhost:5000
- **Frontend**: React development server on http://localhost:3000
- Database connection to Ubuntu VM SQL Server via pyodbc
- Gemini API key configuration via environment variables
- CORS enabled for React frontend communication
- Automatic fallback to AI-only mode when database is unavailable
