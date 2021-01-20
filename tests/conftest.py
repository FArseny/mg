from app.config import TestingConfig
from app.service.task_manager import TaskManager
from app import db, create_app

import pytest


@pytest.fixture(autouse=True)
def run_around_tests():
    print("before clear fut dict")
    TaskManager.FutureDict.clear()
    yield



@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestingConfig)

    with app.app_context():
        from app.model.task import Task
        db.create_all()
        
    yield app
    
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()

