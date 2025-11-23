from fastapi import status


def test_create_user_profile(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    profile_data = {
        "current_role": "Software Engineer",
        "years_of_experience": 5,
        "salary_range": "$80k-$120k",
        "spoken_languages": ["English", "Spanish", "French"]
    }
    
    response = client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["current_role"] == profile_data["current_role"]
    assert data["years_of_experience"] == profile_data["years_of_experience"]
    assert data["salary_range"] == profile_data["salary_range"]
    assert data["spoken_languages"] == profile_data["spoken_languages"]
    assert data["user_id"] == user_id
    assert "id" in data


def test_create_user_profile_minimal(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    profile_data = {
        "spoken_languages": []
    }
    
    response = client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["current_role"] is None
    assert data["years_of_experience"] is None
    assert data["salary_range"] is None
    assert data["spoken_languages"] == []


def test_create_duplicate_user_profile(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    profile_data = {
        "current_role": "Engineer",
        "spoken_languages": ["English"]
    }
    
    client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    
    response = client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_user_profile(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    profile_data = {
        "current_role": "Data Scientist",
        "years_of_experience": 3,
        "spoken_languages": ["English"]
    }
    create_response = client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    profile_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/profiles/{profile_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == profile_id
    assert data["current_role"] == profile_data["current_role"]


def test_get_user_profile_by_user(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    profile_data = {
        "current_role": "Product Manager",
        "spoken_languages": ["English", "German"]
    }
    client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    
    response = client.get(f"/api/v1/users/{user_id}/profile")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_id"] == user_id
    assert data["current_role"] == profile_data["current_role"]


def test_get_user_profile_not_found(client):
    response = client.get("/api/v1/profiles/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_profile_by_user_not_found(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}/profile")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_profile(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    profile_data = {
        "current_role": "Junior Developer",
        "years_of_experience": 1,
        "spoken_languages": ["English"]
    }
    create_response = client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    profile_id = create_response.json()["id"]
    
    update_data = {
        "current_role": "Senior Developer",
        "years_of_experience": 5,
        "spoken_languages": ["English", "Spanish"]
    }
    response = client.patch(f"/api/v1/profiles/{profile_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["current_role"] == update_data["current_role"]
    assert data["years_of_experience"] == update_data["years_of_experience"]
    assert data["spoken_languages"] == update_data["spoken_languages"]


def test_update_user_profile_not_found(client):
    update_data = {"current_role": "Engineer"}
    response = client.patch("/api/v1/profiles/99999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_profile(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    profile_data = {
        "current_role": "Engineer",
        "spoken_languages": ["English"]
    }
    create_response = client.post(f"/api/v1/users/{user_id}/profile", json=profile_data)
    profile_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/profiles/{profile_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/profiles/{profile_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_profile_not_found(client):
    response = client.delete("/api/v1/profiles/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

