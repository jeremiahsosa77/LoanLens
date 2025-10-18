from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://loanlens_user:loanlens_password@localhost:5432/loanlens_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Configure CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(','))
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.profile import profile_bp
    from routes.accounts import accounts_bp
    from routes.loans import loans_bp
    from routes.scenarios import scenarios_bp
    from routes.calculate import calculate_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(accounts_bp, url_prefix='/accounts')
    app.register_blueprint(loans_bp, url_prefix='/loans')
    app.register_blueprint(scenarios_bp, url_prefix='/scenarios')
    app.register_blueprint(calculate_bp, url_prefix='/calculate')
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Only run in debug mode if explicitly set in environment
    debug_mode = os.getenv('FLASK_ENV') == 'development' and os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
