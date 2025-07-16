# CB2 - AI Chatbot Platform

A modern, full-stack AI chatbot platform built with Flask (Python) and React (JavaScript/TypeScript).

## 🚀 Features

- **AI-Powered Chat**: Integration with Google's Gemini AI for intelligent conversations
- **User Authentication**: Secure user registration and login system
- **Admin Dashboard**: Comprehensive admin panel with system monitoring
- **Real-time Chat**: Interactive chat interface with conversation history
- **Responsive Design**: Modern UI that works on desktop and mobile devices

## 🏗️ Architecture

```
cb2/
├── app.py                 # Main Flask application
├── models.py             # Database models and schema
├── routes/               # API route handlers
│   ├── auth_routes.py    # Authentication endpoints
│   ├── chat_routes.py    # Chat functionality
│   └── admin_routes.py   # Admin dashboard APIs
├── services/             # Business logic services
│   ├── database_service.py
│   └── gemini_service.py
├── frontend/             # React frontend application
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   └── utils/        # Utility functions
└── static/               # Static assets (CSS, JS)
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Google Generative AI** - AI chat integration
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Bootstrap 5** - CSS framework
- **Axios** - HTTP client

### Database
- **SQL Server** - Primary database (via pyodbc/pymssql)

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- SQL Server instance
- Google AI API key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cb2
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Start backend server
python app.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Admin Dashboard: http://localhost:3000/admin

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server

# Google AI Configuration
GOOGLE_AI_API_KEY=your_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Security
BCRYPT_LOG_ROUNDS=12
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_api.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Chat Endpoints
- `POST /api/chat/send` - Send message to AI
- `GET /api/chat/conversations` - Get user conversations
- `GET /api/chat/messages/:conversation_id` - Get conversation messages

### Admin Endpoints
- `GET /api/admin/status` - System status
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/users` - User management
- `GET /api/admin/logs` - System logs

## 🔧 Development

### Code Style
- Backend: Follow PEP 8 guidelines
- Frontend: Use ESLint and Prettier
- Use meaningful commit messages

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Update documentation
4. Submit pull request

### Database Migrations
```bash
# Create new migration
python migrate_database.py

# Apply migrations
python init_db.py
```

## 🚀 Deployment

### Production Setup
1. Set `FLASK_ENV=production` in environment
2. Configure production database
3. Set up reverse proxy (nginx)
4. Use WSGI server (gunicorn)

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review existing issues

## 🔄 Changelog

### v1.0.0
- Initial release
- Basic chat functionality
- User authentication
- Admin dashboard
- React frontend

