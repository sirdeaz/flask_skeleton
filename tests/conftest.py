import pytest
import tempfile
import os

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    class Config:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

    app = create_app(Config)

    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()