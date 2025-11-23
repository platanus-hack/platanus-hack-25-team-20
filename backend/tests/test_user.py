from fastapi import status


def test_create_user(client):
    """Test creating a new user."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/api/v1/users", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data  # Should not expose password


def test_create_user_duplicate_email(client):
    """Test creating a user with duplicate email fails."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # Create first user
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Try to create second user with same email
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_user(client):
    """Test getting a user by ID."""
    # First create a user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Get the user
    response = client.get(f"/api/v1/users/{user_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]


def test_get_user_not_found(client):
    """Test getting a non-existent user returns 404."""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_login_success(client):
    """Test successful user login."""
    # First create a user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    client.post("/api/v1/users", json=user_data)
    
    # Login
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/login", json=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]


def test_login_wrong_password(client):
    """Test login with wrong password fails."""
    # First create a user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    client.post("/api/v1/users", json=user_data)
    
    # Try to login with wrong password
    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/users/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login with non-existent user fails."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "somepassword"
    }
    response = client.post("/api/v1/users/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user(client):
    """Test updating user information."""
    # First create a user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Update the user
    update_data = {
        "full_name": "Updated Name"
    }
    response = client.patch(f"/api/v1/users/{user_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name"


def test_update_user_not_found(client):
    """Test updating non-existent user returns 404."""
    update_data = {
        "full_name": "Updated Name"
    }
    response = client.patch("/api/v1/users/99999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

