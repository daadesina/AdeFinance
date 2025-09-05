from flask import Flask
from database import db, session_ext
from config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    session_ext.init_app(app)

    # Import and register routes
    from app.routes.auth import auth_bp
    from app.routes.base import base_bp
    from app.routes.dashboard import dashboard_bp




    app.register_blueprint(auth_bp)
    app.register_blueprint(base_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()


    return app