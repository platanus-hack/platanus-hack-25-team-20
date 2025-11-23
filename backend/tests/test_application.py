import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.models import JobOffering


def test_create_application(client: TestClient, pg: Session):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "app_test@example.com",
            "full_name": "Application Test User",
            "password": "testpass123",
        },
    )
    assert user_response.status_code == status.HTTP_201_CREATED
    user_id = user_response.json()["id"]
    
    job_offering = JobOffering(
        id="test-job-1",
        company_name="Test Company",
        role_name="Backend Developer",
    )
    pg.add(job_offering)
    pg.commit()
    
    response = client.post(
        "/api/v1/applications",
        json={
            "user_id": user_id,
            "job_offering_id": "test-job-1",
            "status": "draft",
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user_id"] == user_id
    assert data["job_offering_id"] == "test-job-1"
    assert data["status"] == "draft"
    assert data["cv_id"] is None


def test_get_application(client: TestClient, pg: Session):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "app_test2@example.com",
            "full_name": "Application Test User 2",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    job_offering = JobOffering(
        id="test-job-2",
        company_name="Test Company 2",
        role_name="Frontend Developer",
    )
    pg.add(job_offering)
    pg.commit()
    
    create_response = client.post(
        "/api/v1/applications",
        json={
            "user_id": user_id,
            "job_offering_id": "test-job-2",
        },
    )
    application_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/applications/{application_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == application_id
    assert data["user_id"] == user_id
    assert data["job_offering_id"] == "test-job-2"


def test_get_user_applications(client: TestClient, pg: Session):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "app_test3@example.com",
            "full_name": "Application Test User 3",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    for i in range(3):
        job_offering = JobOffering(
            id=f"test-job-3-{i}",
            company_name=f"Test Company {i}",
            role_name=f"Developer {i}",
        )
        pg.add(job_offering)
    pg.commit()
    
    for i in range(3):
        client.post(
            "/api/v1/applications",
            json={
                "user_id": user_id,
                "job_offering_id": f"test-job-3-{i}",
            },
        )
    
    response = client.get(f"/api/v1/users/{user_id}/applications")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    
    for application in data:
        assert application["user_id"] == user_id


def test_update_application(client: TestClient, pg: Session):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "app_test4@example.com",
            "full_name": "Application Test User 4",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    job_offering = JobOffering(
        id="test-job-4",
        company_name="Test Company 4",
        role_name="Full Stack Developer",
    )
    pg.add(job_offering)
    pg.commit()
    
    create_response = client.post(
        "/api/v1/applications",
        json={
            "user_id": user_id,
            "job_offering_id": "test-job-4",
            "status": "draft",
        },
    )
    application_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/applications/{application_id}",
        json={
            "status": "sent",
            "notes": "Sent via LinkedIn",
        },
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "sent"
    assert data["notes"] == "Sent via LinkedIn"


def test_delete_application(client: TestClient, pg: Session):
    user_response = client.post(
        "/api/v1/users",
        json={
            "email": "app_test5@example.com",
            "full_name": "Application Test User 5",
            "password": "testpass123",
        },
    )
    user_id = user_response.json()["id"]
    
    job_offering = JobOffering(
        id="test-job-5",
        company_name="Test Company 5",
        role_name="DevOps Engineer",
    )
    pg.add(job_offering)
    pg.commit()
    
    create_response = client.post(
        "/api/v1/applications",
        json={
            "user_id": user_id,
            "job_offering_id": "test-job-5",
        },
    )
    application_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/api/v1/applications/{application_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/applications/{application_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_get_job_offering_applications(client: TestClient, pg: Session):
    job_offering = JobOffering(
        id="test-job-6",
        company_name="Popular Company",
        role_name="Software Engineer",
    )
    pg.add(job_offering)
    pg.commit()
    
    for i in range(2):
        user_response = client.post(
            "/api/v1/users",
            json={
                "email": f"app_test6_{i}@example.com",
                "full_name": f"User {i}",
                "password": "testpass123",
            },
        )
        user_id = user_response.json()["id"]
        
        client.post(
            "/api/v1/applications",
            json={
                "user_id": user_id,
                "job_offering_id": "test-job-6",
            },
        )
    
    response = client.get("/api/v1/job-offerings/test-job-6/applications")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    
    for application in data:
        assert application["job_offering_id"] == "test-job-6"

