
import os

from flask import Flask

from extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Create the instance folder if it doesn't exist.
    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///api_logs.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    # Initialize database with this Flask app.
    db.init_app(app)

    # Import the model so SQLAlchemy knows about its table.
    from models import request_logs

    # Register API routes.
    from controllers.log_controller import api_bp
    app.register_blueprint(api_bp)

    # Register request monitoring.
    from monitoring.request_hooks import register_request_hooks
    register_request_hooks(app)

    # Create database tables if they don't exist.
    with app.app_context():
        db.create_all()

    return app
