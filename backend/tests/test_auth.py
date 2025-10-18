def test_register(client):
    """Test user registration"""
    response = client.post('/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'access_token' in data
    assert 'user' in data
    assert data['user']['email'] == 'newuser@example.com'

def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # First registration
    client.post('/auth/register', json={
        'email': 'duplicate@example.com',
        'password': 'password123'
    })
    
    # Try to register again with same email
    response = client.post('/auth/register', json={
        'email': 'duplicate@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_login(client):
    """Test user login"""
    # Register first
    client.post('/auth/register', json={
        'email': 'login@example.com',
        'password': 'password123'
    })
    
    # Login
    response = client.post('/auth/login', json={
        'email': 'login@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'user' in data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    """Test getting current user"""
    response = client.get('/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'email' in data
    assert data['email'] == 'test@example.com'
