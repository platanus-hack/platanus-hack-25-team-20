from fastapi import status


def test_create_user_skill_dev_skill(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    skills_data = {
        "skill_text": "FastAPI - Expert level, 5 years of experience building REST APIs",
        "skill_type": "dev-skill",
        "raw_input": "Expert in FastAPI",
        "source": "LinkedIn"
    }
    
    response = client.post(f"/api/v1/users/{user_id}/skills", json=skills_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["skill_text"] == skills_data["skill_text"]
    assert data["skill_type"] == skills_data["skill_type"]
    assert data["raw_input"] == skills_data["raw_input"]
    assert data["source"] == skills_data["source"]
    assert data["user_id"] == user_id
    assert "id" in data


def test_create_user_skill_experience(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    skills_data = {
        "skill_text": "5 years as Software Engineer at Google",
        "skill_type": "experience"
    }
    
    response = client.post(f"/api/v1/users/{user_id}/skills", json=skills_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["skill_text"] == skills_data["skill_text"]
    assert data["skill_type"] == skills_data["skill_type"]
    assert data["raw_input"] is None
    assert data["source"] is None


def test_get_user_skill(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    skills_data = {
        "skill_text": "AWS Certified Solutions Architect",
        "skill_type": "certificate",
        "source": "Credly"
    }
    create_response = client.post(f"/api/v1/users/{user_id}/skills", json=skills_data)
    skills_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/skills/{skills_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == skills_id
    assert data["skill_text"] == skills_data["skill_text"]
    assert data["skill_type"] == skills_data["skill_type"]


def test_get_user_skill_not_found(client):
    response = client.get("/api/v1/skills/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_skills_grouped(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    # Crear skills de diferentes tipos
    client.post(f"/api/v1/users/{user_id}/skills", json={
        "skill_text": "Python - Advanced",
        "skill_type": "dev-skill",
        "source": "GitHub"
    })
    client.post(f"/api/v1/users/{user_id}/skills", json={
        "skill_text": "3 years at Meta",
        "skill_type": "experience"
    })
    client.post(f"/api/v1/users/{user_id}/skills", json={
        "skill_text": "AWS Certified",
        "skill_type": "certificate"
    })
    client.post(f"/api/v1/users/{user_id}/skills", json={
        "skill_text": "Fluent in Spanish",
        "skill_type": "extra"
    })
    
    response = client.get(f"/api/v1/users/{user_id}/skills")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verificar estructura agrupada
    assert "experience" in data
    assert "dev_skills" in data
    assert "certificates" in data
    assert "extra" in data
    
    # Verificar que cada grupo tiene el skill correcto
    assert len(data["dev_skills"]) == 1
    assert data["dev_skills"][0]["skill_text"] == "Python - Advanced"
    
    assert len(data["experience"]) == 1
    assert data["experience"][0]["skill_text"] == "3 years at Meta"
    
    assert len(data["certificates"]) == 1
    assert data["certificates"][0]["skill_text"] == "AWS Certified"
    
    assert len(data["extra"]) == 1
    assert data["extra"][0]["skill_text"] == "Fluent in Spanish"


def test_get_user_skills_grouped_empty(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}/skills")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Todos los grupos deben estar vacíos
    assert data["experience"] == []
    assert data["dev_skills"] == []
    assert data["certificates"] == []
    assert data["extra"] == []


def test_update_user_skill(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    skills_data = {
        "skill_text": "Python - Beginner",
        "skill_type": "dev-skill"
    }
    create_response = client.post(f"/api/v1/users/{user_id}/skills", json=skills_data)
    skills_id = create_response.json()["id"]
    
    update_data = {
        "skill_text": "Python - Expert level, 5+ years",
        "source": "LinkedIn"
    }
    response = client.patch(f"/api/v1/skills/{skills_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["skill_text"] == update_data["skill_text"]
    assert data["source"] == update_data["source"]
    assert data["skill_type"] == "dev-skill"  # No cambiado


def test_update_user_skill_not_found(client):
    update_data = {"skill_text": "New text"}
    response = client.patch("/api/v1/skills/99999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_skill(client):
    user_response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    user_id = user_response.json()["id"]
    
    skills_data = {
        "skill_text": "Docker expertise",
        "skill_type": "dev-skill"
    }
    create_response = client.post(f"/api/v1/users/{user_id}/skills", json=skills_data)
    skills_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/skills/{skills_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/skills/{skills_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_skill_not_found(client):
    response = client.delete("/api/v1/skills/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

