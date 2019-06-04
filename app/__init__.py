from flask import Flask

from app.extensions import db, limiter, migrate, flask_uuid
from app.config import Config
from app.errors import handle_429_request

def create_app(config_class=Config):

    app = Flask(__name__)
    # set app configs
    app.config.from_object(config_class)

    db.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app)
    flask_uuid.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # register custom errors
    app.register_error_handler(429, handle_429_request)

    return app

from app import models

