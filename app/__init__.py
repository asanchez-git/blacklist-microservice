from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise ValueError("DATABASE_URL is not configured")

    db.init_app(app)

    from app.routes.blacklists import blacklists_bp
    from app.routes.health import health_bp

    app.register_blueprint(blacklists_bp)
    app.register_blueprint(health_bp)

    with app.app_context():
        db.create_all()

    return app