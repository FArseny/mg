import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import ProductionConfig, DevelopmentConfig
import logging.config



db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)

    if config is None:

        if os.getenv('FLASK_ENV') == 'production':
            app.config.from_object(ProductionConfig)
        else:
            app.config.from_object(DevelopmentConfig)
        
        logging.config.fileConfig(fname="logger.conf")

    else:
        app.config.from_object(config)

    from app.routes import bp
    app.register_blueprint(bp)

    db.init_app(app)

    return app