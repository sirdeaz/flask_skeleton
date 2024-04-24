from flask_login import current_user, login_user
import pytest

from app.models.user import User
from app.extensions import db

def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_login_post_succeed(app, client, user):
    with app.app_context():
        response = client.post('/auth/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/profile'

def test_login_post_fail(app, client, user):
    with app.app_context():
        assert user == db.session.query(User).first()
        response = client.post('/auth/login', data={'email': user.email, 'password': 'wrongpassword'}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/auth/login'

#TODO: change to @pytest.mark.parametrize?
def test_login_email_required(app, client):
    with app.app_context():
        response = client.post('/auth/login', data={'password': 'password'}, follow_redirects=True)
    
        assert b'Please check your login details and try again.' in response.data
        assert response.status_code == 200
        assert response.request.path == '/auth/login'

def test_login_password_required(app, client):
    with app.app_context():
        response = client.post('/auth/login', data={'email': 'test@example.com'}, follow_redirects=True)
        assert b'Please check your login details and try again.' in response.data
        assert response.status_code == 200
        assert response.request.path == '/auth/login'

def test_signup_get(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200

def test_signup_post(app, client):
    response = client.post('/auth/signup', data={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'
    with app.app_context():
        user = db.session.query(User).filter_by(email='test@example.com').first()
        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'

#TODO: change to @pytest.mark.parametrize?
def test_signup_email_required(app, client):
    response = client.post('/auth/signup', data={'first_name': 'Test', 'last_name': 'User', 'password': 'password'}, follow_redirects=True)
    assert b'All fields are required' in response.data
    assert response.status_code == 200
    assert response.request.path == '/auth/signup'

def test_signup_password_required(app, client):
    response = client.post('/auth/signup', data={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}, follow_redirects=True)
    assert b'All fields are required' in response.data
    assert response.status_code == 200
    assert response.request.path == '/auth/signup'

def test_signup_first_name_required(app, client):
    response = client.post('/auth/signup', data={'email': 'test@example.com', 'last_name': 'User', 'password': 'password'}, follow_redirects=True)
    assert b'All fields are required' in response.data
    assert response.status_code == 200
    assert response.request.path == '/auth/signup'

def test_signup_last_name_required(app, client):
    response = client.post('/auth/signup', data={'email': 'test@example.com', 'first_name': 'Test', 'password': 'password'}, follow_redirects=True)
    assert b'All fields are required' in response.data
    assert response.status_code == 200
    assert response.request.path == '/auth/signup'

def test_signup_email_unique(app, client):
    with app.app_context():
        user = User(email='test@example.com', first_name='Test', last_name='User', password='password')
        db.session.add(user)
        db.session.commit()
        response = client.post('/auth/signup', data={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User', 'password': 'password'}, follow_redirects=True)
        assert b'Email already exists.' in response.data
        assert response.status_code == 200
        assert response.request.path == '/auth/signup'

def test_logout_get_fails(app, client, user):
    with app.app_context():
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/auth/login'

def test_logout_get_succeeds(app, client, user):
    with app.app_context():
        response = client.post('/auth/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'