import pytest

def test_login_route(client, farmer_user):
    response = client.post('/auth/login', data={
        'username_or_email': 'test_farmer',
        'password': 'pass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back' in response.data or b'Dashboard' in response.data

def test_invalid_login(client):
    response = client.post('/auth/login', data={
        'username_or_email': 'non_existent',
        'password': 'wrong'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid credentials' in response.data
