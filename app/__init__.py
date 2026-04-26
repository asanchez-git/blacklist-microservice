import os
from flask import Flask
from app.extensions import db




def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or os.getenv("APP_SETTINGS", "development")

    config_map = {
        "development": "app.config.DevelopmentConfig",
        "testing": "app.config.TestingConfig",
        "production": "app.config.ProductionConfig",
    }

    app.config.from_object(config_map[config_name])

    db.init_app(app)

    from app.routes.blacklists import blacklists_bp
    from app.routes.health import health_bp

    app.register_blueprint(blacklists_bp)
    app.register_blueprint(health_bp)

    with app.app_context():
        db.create_all()

    return app