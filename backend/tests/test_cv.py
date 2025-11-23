from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.types.cv_content_types import GeneratedCVContentSimple, Experience, Education, Skill


@pytest.fixture
def mock_llm_response():
    """Mock LLM response"""
    return GeneratedCVContentSimple(
        firstname="Juan",
        lastname="Pérez",
        email="juan.perez@example.com",
        phone="+56912345678",
        github="github.com/juanperez",
        linkedin="linkedin.com/in/juanperez",
        address="Santiago, Chile",
        summary="Desarrollador Full Stack con 5 años de experiencia en tecnologías web modernas.",
        experiences=[
            Experience(
                title="Senior Developer",
                company="Tech Corp",
                date="2020 - Presente",
                description="Desarrollo de aplicaciones web con React y Python."
            ),
            Experience(
                title="Developer",
                company="Startup XYZ",
                date="2018 - 2020",
                description="Desarrollo backend con Django y PostgreSQL."
            ),
        ],
        education=[
            Education(
                degree="Ingeniería Civil en Computación",
                institution="Universidad de Chile",
                date="2014 - 2018",
                description="Especialización en desarrollo de software."
            ),
        ],
        skills=[
            Skill(category="Lenguajes", skill_list="Python, JavaScript, TypeScript"),
            Skill(category="Frameworks", skill_list="React, FastAPI, Django"),
            Skill(category="Bases de Datos", skill_list="PostgreSQL, MongoDB"),
        ],
    )


def test_create_cv(client: TestClient, mock_llm_response):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123",
        },
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={
            "name": "Proyecto Test",
            "target_role": "Backend Developer",
            "cv_style": "Profesional",
        },
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]
    
    client.post(
        f"/api/v1/users/{user_id}/skills",
        json={
            "skill_text": "Python - 5 años de experiencia",
            "skill_type": "dev-skill",
            "source": "manual",
        },
    )
    
    response = client.get("/api/v1/templates")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) > 0
    template_id = templates[0]["id"]
    
    with patch("app.services.llm_service.client.chat.completions.create") as mock_create:
        mock_create.return_value = mock_llm_response
        
        cv_response = client.post(
            f"/api/v1/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
                "messages": [
                    {"role": "user", "content": "Genera un CV profesional enfocado en desarrollo backend"}
                ],
            },
        )
    
    assert cv_response.status_code == 201
    cv_data = cv_response.json()
    assert cv_data["project_id"] == project_id
    assert cv_data["template_id"] == template_id
    assert cv_data["base_cv_id"] is None
    assert cv_data["content"]["firstname"] == "Juan"
    assert cv_data["content"]["lastname"] == "Pérez"
    assert cv_data["content"]["email"] == "juan.perez@example.com"
    assert len(cv_data["content"]["experiences"]) == 2
    assert len(cv_data["content"]["education"]) == 1
    assert len(cv_data["content"]["skills"]) == 3
    assert cv_data["rendered_content"] is not None
    assert "Juan" in cv_data["rendered_content"]
    assert "Pérez" in cv_data["rendered_content"]
    assert len(cv_data["conversation_history"]) == 1
    assert cv_data["conversation_history"][0]["role"] == "user"
    assert "content" in cv_data["conversation_history"][0]
    mock_create.assert_called_once()


def test_create_cv_with_base_cv(client: TestClient, mock_llm_response):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test2@example.com",
            "full_name": "Test User 2",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={
            "name": "Proyecto Frontend",
            "target_role": "Frontend Developer",
        },
    )
    project_id = project_response.json()["id"]
    
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    
    with patch("app.services.llm_service.client.chat.completions.create") as mock_create:
        mock_create.return_value = mock_llm_response
        
        base_cv_response = client.post(
            f"/api/v1/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
            },
        )
        
        base_cv_id = base_cv_response.json()["id"]
        
        new_cv_response = client.post(
            f"/api/v1/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
                "base_cv_id": base_cv_id,
                "messages": [
                    {"role": "user", "content": "Adapta el CV para estar más enfocado en React"}
                ],
            },
        )
        
        assert mock_create.call_count == 2
    
    assert new_cv_response.status_code == 201
    new_cv_data = new_cv_response.json()
    assert new_cv_data["base_cv_id"] == base_cv_id
    assert new_cv_data["content"] is not None
    assert new_cv_data["rendered_content"] is not None


def test_get_cv(client: TestClient, mock_llm_response):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test3@example.com",
            "full_name": "Test User 3",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={"name": "Proyecto Data Science", "target_role": "Data Scientist"},
    )
    project_id = project_response.json()["id"]
    
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    
    with patch("app.services.llm_service.client.chat.completions.create") as mock_create:
        mock_create.return_value = mock_llm_response
        
        cv_response = client.post(
            f"/api/v1/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
            },
        )
    
    cv_id = cv_response.json()["id"]
    
    get_response = client.get(f"/api/v1/cvs/{cv_id}")
    assert get_response.status_code == 200
    cv_data = get_response.json()
    assert cv_data["id"] == cv_id
    assert cv_data["project_id"] == project_id
    assert cv_data["template_id"] == template_id
    assert cv_data["content"]["firstname"] == "Juan"
    assert cv_data["content"]["lastname"] == "Pérez"
    assert cv_data["rendered_content"] is not None


def test_get_project_cvs(client: TestClient, mock_llm_response):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test4@example.com",
            "full_name": "Test User 4",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={"name": "Proyecto DevOps", "target_role": "DevOps Engineer"},
    )
    project_id = project_response.json()["id"]
    
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    
    with patch("app.services.llm_service.client.chat.completions.create") as mock_create:
        mock_create.return_value = mock_llm_response
        
        for i in range(3):
            client.post(
                f"/api/v1/projects/{project_id}/cvs",
                json={
                    "project_id": project_id,
                    "template_id": template_id,
                    "messages": [
                        {"role": "user", "content": f"Genera CV número {i+1}"}
                    ],
                },
            )
    
    list_response = client.get(f"/api/v1/projects/{project_id}/cvs")
    assert list_response.status_code == 200
    cvs = list_response.json()
    assert len(cvs) == 3
    
    for cv in cvs:
        assert cv["project_id"] == project_id
        assert cv["content"] is not None
        assert cv["rendered_content"] is not None
    
    contents = [cv["conversation_history"][0]["content"] for cv in cvs]
    assert "CV 1" in " ".join(contents) or "CV número 1" in " ".join(contents)
    assert "CV 2" in " ".join(contents) or "CV número 2" in " ".join(contents)
    assert "CV 3" in " ".join(contents) or "CV número 3" in " ".join(contents)


def test_update_cv(client: TestClient, mock_llm_response):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test5@example.com",
            "full_name": "Test User 5",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={"name": "Proyecto ML", "target_role": "ML Engineer"},
    )
    project_id = project_response.json()["id"]
    
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    
    with patch("app.services.llm_service.client.chat.completions.create") as mock_create:
        mock_create.return_value = mock_llm_response
        
        cv_response = client.post(
            f"/api/v1/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
            },
        )
    
    cv_id = cv_response.json()["id"]
    original_rendered = cv_response.json()["rendered_content"]
    
    updated_content = {
        "firstname": "María",
        "lastname": "González",
        "email": "maria@example.com",
        "phone": "+56987654321",
        "address": "Valparaíso, Chile",
        "summary": "Actualizado",
        "experiences": [],
        "education": [],
        "skills": [],
    }
    
    update_response = client.patch(
        f"/api/v1/cvs/{cv_id}",
        json={"content": updated_content},
    )
    
    assert update_response.status_code == 200
    updated_cv = update_response.json()
    assert updated_cv["content"]["firstname"] == "María"
    assert updated_cv["content"]["lastname"] == "González"
    assert updated_cv["content"]["email"] == "maria@example.com"
    assert updated_cv["content"]["summary"] == "Actualizado"
    assert updated_cv["rendered_content"] is not None
    assert updated_cv["rendered_content"] != original_rendered
    assert "María" in updated_cv["rendered_content"]
    assert "González" in updated_cv["rendered_content"]


def test_delete_cv(client: TestClient, mock_llm_response):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test6@example.com",
            "full_name": "Test User 6",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={"name": "Proyecto Product", "target_role": "Product Manager"},
    )
    project_id = project_response.json()["id"]
    
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    
    with patch("app.services.llm_service.client.chat.completions.create") as mock_create:
        mock_create.return_value = mock_llm_response
        
        cv_response = client.post(
            f"/api/v1/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
            },
        )
    
    cv_id = cv_response.json()["id"]
    
    delete_response = client.delete(f"/api/v1/cvs/{cv_id}")
    assert delete_response.status_code == 204
    
    get_response = client.get(f"/api/v1/cvs/{cv_id}")
    assert get_response.status_code == 404


def test_regenerate_cv(client: TestClient, mock_llm_response):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test7@example.com",
            "full_name": "Test User 7",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={"name": "Proyecto UX", "target_role": "UX Designer"},
    )
    project_id = project_response.json()["id"]
    
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    
    with patch("app.services.llm_service.client.chat.completions.create") as mock_create:
        mock_create.return_value = mock_llm_response
        
        cv_response = client.post(
            f"/api/v1/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
            },
        )
        
        cv_id = cv_response.json()["id"]
        
        regen_response = client.post(
            f"/api/v1/cvs/{cv_id}/regenerate",
            json={
                "messages": [
                    {"role": "user", "content": "Hazlo más enfocado en diseño de interfaces"}
                ]
            },
        )
        
        assert mock_create.call_count == 2
    
    assert regen_response.status_code == 200
    regen_cv = regen_response.json()
    assert len(regen_cv["conversation_history"]) >= 2
    assert regen_cv["conversation_history"][0]["role"] == "user"
    assert "content" in regen_cv["conversation_history"][0]
    assert regen_cv["conversation_history"][-1]["role"] == "user"
    assert "content" in regen_cv["conversation_history"][-1]


def test_create_cv_template_not_found(client: TestClient):
    """Test creating CV with non-existent template_id"""
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test8@example.com",
            "full_name": "Test User 8",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={"name": "Proyecto Test", "target_role": "Developer"},
    )
    project_id = project_response.json()["id"]
    
    cv_response = client.post(
        f"/api/v1/projects/{project_id}/cvs",
        json={
            "project_id": project_id,
            "template_id": 99999,
        },
    )
    
    assert cv_response.status_code == 404


def test_create_cv_project_not_found(client: TestClient):
    """Test creating CV with non-existent project_id"""
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    cv_response = client.post(
        f"/api/v1/projects/99999/cvs",
        json={
            "project_id": 99999,
            "template_id": template_id,
        },
    )
    
    assert cv_response.status_code == 404


def test_create_cv_project_id_mismatch(client: TestClient):
    """Test creating CV with project_id mismatch between URL and body"""
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "test9@example.com",
            "full_name": "Test User 9",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    project_response = client.post(
        f"/api/v1/projects?user_id={user_id}",
        json={"name": "Proyecto Test", "target_role": "Developer"},
    )
    project_id = project_response.json()["id"]
    
    response = client.get("/api/v1/templates")
    templates = response.json()
    template_id = templates[0]["id"]
    
    cv_response = client.post(
        f"/api/v1/projects/{project_id}/cvs",
        json={
            "project_id": project_id + 1,
            "template_id": template_id,
        },
    )
    
    assert cv_response.status_code == 400


def test_get_cv_not_found(client: TestClient):
    """Test getting non-existent CV"""
    response = client.get("/api/v1/cvs/99999")
    assert response.status_code == 404


def test_update_cv_not_found(client: TestClient):
    """Test updating non-existent CV"""
    response = client.patch(
        "/api/v1/cvs/99999",
        json={"content": {"firstname": "Test"}},
    )
    assert response.status_code == 404


def test_delete_cv_not_found(client: TestClient):
    """Test deleting non-existent CV"""
    response = client.delete("/api/v1/cvs/99999")
    assert response.status_code == 404


def test_regenerate_cv_not_found(client: TestClient):
    """Test regenerating non-existent CV"""
    response = client.post(
        "/api/v1/cvs/99999/regenerate",
        json={"messages": [{"role": "user", "content": "Test"}]},
    )
    assert response.status_code == 404
