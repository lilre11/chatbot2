#!/bin/bash
set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for database to be ready..."
    while ! python -c "
import sys
sys.path.append('/app')
from app import create_app
from services.database_service import DatabaseService
from config import config

app = create_app(config['production'])
with app.app_context():
    db_service = DatabaseService()
    if db_service.is_db_working():
        print('Database is ready!')
        exit(0)
    else:
        print('Database not ready yet...')
        exit(1)
" 2>/dev/null; do
    echo "Database is unavailable - sleeping for 2 seconds"
    sleep 2
done
}

# Function to initialize database
init_db() {
    echo "Initializing database..."
    python -c "
import sys
sys.path.append('/app')
from app import create_app
from services.database_service import DatabaseService
from config import config
import os

config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config[config_name])
with app.app_context():
    db_service = DatabaseService()
    if db_service.is_db_working():
        db_service.init_db()
        print('Database initialized successfully!')
    else:
        print('Database not available, skipping initialization')
"
}

# Function to create admin user
create_admin() {
    echo "Creating admin user..."
    python -c "
import sys
sys.path.append('/app')
from app import create_app
from services.database_service import DatabaseService
from config import config
import os

config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config[config_name])
with app.app_context():
    db_service = DatabaseService()
    if db_service.is_db_working():
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin_password_change_this')
        
        try:
            db_service.create_user(admin_email, admin_password)
            print('Admin user created successfully!')
        except Exception as e:
            print(f'Admin user might already exist: {e}')
    else:
        print('Database not available, skipping admin user creation')
"
}

# Main execution
echo "Starting chatbot backend..."

# Wait for database if DATABASE_URL is set
if [ ! -z "$DATABASE_URL" ]; then
    wait_for_db
    init_db
    create_admin
else
    echo "No DATABASE_URL set, running in standalone mode..."
fi

# Start the application
echo "Starting Flask application..."
exec "$@"
