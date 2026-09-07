import pytest

def test_unauthenticated_access_redirection(client):
    response = client.get('/farmer/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data or b'login' in response.request.path

def test_role_access_denied(client, farmer_user):
    # Log in as Farmer
    client.post('/auth/login', data={'username_or_email': 'test_farmer', 'password': 'pass123'})
    
    # Try accessing Admin Dashboard
    response = client.get('/admin/dashboard')
    assert response.status_code == 403
