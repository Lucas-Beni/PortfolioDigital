import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = "portfolio-secret-key-2024-very-secure-local-development"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure SQLite database (local file)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize the app with the extension
db.init_app(app)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "login"  # rota usada para login
login_manager.login_message = "Por favor faça login para acessar esta página."
login_manager.init_app(app)

# necessário para o Flask-Login saber como carregar o usuário
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401
    db.create_all()
    
    # Create admin user if it doesn't exist
    admin_user = models.User.query.filter_by(email='adm@adm.com').first()
    if not admin_user:
        admin_user = models.User.create_local_user(
            email='adm@adm.com',
            password='adm123',
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        logging.info("Admin user created: adm@adm.com")
    else:
        logging.info("Admin user already exists")
    
    logging.info("Database tables created and admin user configured")
