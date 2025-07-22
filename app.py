from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
import logging
import os
import warnings
from sqlalchemy.exc import SAWarning

# SQLAlchemy uyarılarını bastır
warnings.filterwarnings("ignore", category=SAWarning, message=".*Unrecognized server version info.*")

# models.py'deki db objesini import et
from models import db

# Logging ayarları
def setup_logging(app):
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.logger.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))

# Uygulama fabrikası
def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Session cookie ayarları
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_DOMAIN'] = None

    # Logging setup
    setup_logging(app)

    # CORS ayarları
    CORS(app,
         origins=app.config.get('CORS_ORIGINS', ['http://192.168.1.147']),
         supports_credentials=True,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    # SQLAlchemy başlat
    db.init_app(app)

    # Veritabanı tablolarını oluştur
    with app.app_context():
        try:
            db.create_all()
            # Test database connection and set flag
            from models import User
            User.query.limit(1).first()  # Test query
            app.db_working = True
            app.logger.info("Database connection successful")
        except Exception as e:
            app.logger.warning(f"Veritabanı bağlantısı başarısız. create_all atlandı: {e}")
            app.db_working = False

    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Chatbot API is running',
            'version': '1.0.0',
            'api_base': '/api',
            'endpoints': {
                'health': '/api/health',
                'documentation': '/api/api-docs',
                'chat': '/api/chat',
                'admin': '/api/admin',
                'auth': '/api/auth'
            }
        })

    # Blueprintleri import edip kaydet
    from routes.chat_routes import chat_bp
    from routes.admin_routes import admin_bp
    from routes.auth_routes import auth_bp
    from routes.main_routes import main_bp

    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(main_bp, url_prefix='/api')

    # Error handlerlar
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500

    # İstek öncesi loglama
    @app.before_request
    def log_request():
        app.logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")

    # Yanıt sonrası loglama
    @app.after_request
    def log_response(response):
        app.logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
        return response

    return app

# Uygulama çalıştır
if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config.get('DEBUG', True), host='0.0.0.0', port=5000)

