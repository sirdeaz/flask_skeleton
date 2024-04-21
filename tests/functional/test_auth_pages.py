import pytest

def test_login(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    

def test_signup(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200

def test_logout(client):
    response = client.get('/auth/logout')
    assert response.status_code == 200