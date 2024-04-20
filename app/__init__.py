from flask import Flask

from config import Config
from app.extensions import db, migrate

def create_app(config_class = Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize Flask Extension here
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
