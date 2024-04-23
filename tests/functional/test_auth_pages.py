from flask_login import current_user, login_user
import pytest

from app.models.user import User
from app.extensions import db

def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_login_post(client):
    response = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 302
    assert response.location == '/profile'

def test_signup_get(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200

def test_signup_post(client):
    response = client.post('/auth/signup', data={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User', 'password': 'password'})
    assert response.status_code == 302
    assert response.location == '/auth/login'
    assert db.session.query(User).filter_by(email='test@example.com').first() is not None

def test_logout_get(app, client, user):
    with app.app_context():
        login_user(user)
        response = client.get('/auth/logout')
        assert response.status_code == 302
        assert response.location == '/auth/login'
        assert current_user.is_anonymous

