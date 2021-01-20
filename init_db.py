from flask import Flask
from app.config import ProductionConfig, DevelopmentConfig, TestingConfig


def init_all_db():
    from app import db
    from app.model.task import Task

    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    app.config.from_object(DevelopmentConfig)
    with app.app_context():
        db.create_all()
    
    app.config.from_object(TestingConfig)
    with app.app_context():
        db.create_all()


init_all_db()