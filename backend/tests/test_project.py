from fastapi import status


def test_create_project(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    project_data = {
        "name": "Software Engineer Job Search",
        "target_role": "Backend Developer",
        "cv_style": "professional",
        "preferences": {"location": "remote", "salary_min": 50000}
    }
    
    response = client.post(f"/api/v1/projects?user_id={user_id}", json=project_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["target_role"] == project_data["target_role"]
    assert data["cv_style"] == project_data["cv_style"]
    assert data["preferences"] == project_data["preferences"]
    assert data["user_id"] == user_id
    assert "id" in data


def test_create_project_minimal(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    project_data = {
        "name": "Job Search"
    }
    
    response = client.post(f"/api/v1/projects?user_id={user_id}", json=project_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["target_role"] is None
    assert data["cv_style"] is None
    assert data["preferences"] is None


def test_get_project(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    project_data = {
        "name": "My Project",
        "target_role": "Developer"
    }
    create_response = client.post(f"/api/v1/projects?user_id={user_id}", json=project_data)
    project_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/projects/{project_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == project_data["name"]
    assert data["target_role"] == project_data["target_role"]


def test_get_project_not_found(client):
    response = client.get("/api/v1/projects/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_projects(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    client.post(f"/api/v1/projects?user_id={user_id}", json={"name": "Project 1"})
    client.post(f"/api/v1/projects?user_id={user_id}", json={"name": "Project 2"})
    client.post(f"/api/v1/projects?user_id={user_id}", json={"name": "Project 3"})
    
    response = client.get(f"/api/v1/users/{user_id}/projects")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    project_names = {p["name"] for p in data}
    assert project_names == {"Project 1", "Project 2", "Project 3"}


def test_get_user_projects_empty(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}/projects")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0


def test_update_project(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    project_data = {
        "name": "Original Name",
        "target_role": "Developer"
    }
    create_response = client.post(f"/api/v1/projects?user_id={user_id}", json=project_data)
    project_id = create_response.json()["id"]
    
    update_data = {
        "name": "Updated Name",
        "cv_style": "elegant"
    }
    response = client.patch(f"/api/v1/projects/{project_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["cv_style"] == "elegant"
    assert data["target_role"] == "Developer"


def test_update_project_not_found(client):
    update_data = {"name": "Updated Name"}
    response = client.patch("/api/v1/projects/99999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_project(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    project_data = {"name": "Project to Delete"}
    create_response = client.post(f"/api/v1/projects?user_id={user_id}", json=project_data)
    project_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/projects/{project_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/projects/{project_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_project_not_found(client):
    response = client.delete("/api/v1/projects/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

