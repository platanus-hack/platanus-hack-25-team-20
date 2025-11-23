import pytest
from datetime import datetime

from app.database.models import JobOffering


def test_list_job_offerings_empty(client):
    """Test listing job offerings when there are none"""
    response = client.get("/api/v1/job-offerings")
    assert response.status_code == 200
    assert response.json() == []


def test_list_job_offerings(client, pg):
    """Test listing all job offerings without filters"""
    # Insert job offerings directly
    job1 = JobOffering(
        id="job-1",
        keyword="python-backend",
        company_name="Google",
        role_name="Senior Backend Engineer",
        location="Santiago, Chile",
        work_mode="Hybrid",
        salary="$80k-$120k",
        description="Python backend development",
    )
    job2 = JobOffering(
        id="job-2",
        keyword="frontend",
        company_name="Meta",
        role_name="Frontend Developer",
        location="Remote",
        work_mode="Remote",
        salary="$70k-$100k",
    )
    job3 = JobOffering(
        id="job-3",
        keyword="python-backend",
        company_name="Amazon",
        role_name="Software Engineer",
        location="USA",
        work_mode="On-site",
    )
    
    pg.add_all([job1, job2, job3])
    pg.commit()
    
    # List all
    response = client.get("/api/v1/job-offerings")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Check IDs
    ids = [job["id"] for job in data]
    assert "job-1" in ids
    assert "job-2" in ids
    assert "job-3" in ids


def test_get_job_offering_by_id(client, pg):
    """Test getting a specific job offering by ID"""
    job = JobOffering(
        id="test-job-123",
        keyword="python-backend",
        company_name="Test Company",
        role_name="Python Developer",
        location="Santiago",
        description="Test description",
        salary="$50k-$80k",
    )
    pg.add(job)
    pg.commit()
    
    response = client.get("/api/v1/job-offerings/test-job-123")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == "test-job-123"
    assert data["keyword"] == "python-backend"
    assert data["company_name"] == "Test Company"
    assert data["role_name"] == "Python Developer"
    assert data["location"] == "Santiago"
    assert data["salary"] == "$50k-$80k"


def test_get_job_offering_not_found(client):
    """Test getting a non-existent job offering"""
    response = client.get("/api/v1/job-offerings/non-existent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_filter_by_keyword_exact(client, pg):
    """Test exact keyword filter"""
    job1 = JobOffering(
        id="job-python-1",
        keyword="python-backend",
        company_name="Company A",
        role_name="Backend Dev",
    )
    job2 = JobOffering(
        id="job-python-2",
        keyword="python-backend",
        company_name="Company B",
        role_name="Python Engineer",
    )
    job3 = JobOffering(
        id="job-frontend-1",
        keyword="frontend",
        company_name="Company C",
        role_name="Frontend Dev",
    )
    
    pg.add_all([job1, job2, job3])
    pg.commit()
    
    # Filter by keyword
    response = client.get("/api/v1/job-offerings?keyword=python-backend")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    
    keywords = [job["keyword"] for job in data]
    assert all(k == "python-backend" for k in keywords)
    
    ids = [job["id"] for job in data]
    assert "job-python-1" in ids
    assert "job-python-2" in ids
    assert "job-frontend-1" not in ids


def test_filter_by_keyword_no_results(client, pg):
    """Test keyword filter with no matching results"""
    job = JobOffering(
        id="job-1",
        keyword="python-backend",
        company_name="Test",
        role_name="Dev",
    )
    pg.add(job)
    pg.commit()
    
    response = client.get("/api/v1/job-offerings?keyword=non-existent-keyword")
    assert response.status_code == 200
    assert response.json() == []


def test_search_by_company_name(client, pg):
    """Test search filter on company_name (case-insensitive)"""
    job1 = JobOffering(
        id="job-1",
        keyword="backend",
        company_name="Google Chile",
        role_name="Engineer",
    )
    job2 = JobOffering(
        id="job-2",
        keyword="frontend",
        company_name="Meta",
        role_name="Developer",
    )
    job3 = JobOffering(
        id="job-3",
        keyword="backend",
        company_name="Amazon",
        role_name="Senior Google Specialist",  # "Google" en role_name también
    )
    
    pg.add_all([job1, job2, job3])
    pg.commit()
    
    # Search by company name (case-insensitive)
    response = client.get("/api/v1/job-offerings?search=google")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2  # job-1 (company) y job-3 (role)
    
    ids = [job["id"] for job in data]
    assert "job-1" in ids
    assert "job-3" in ids
    assert "job-2" not in ids


def test_search_by_role_name(client, pg):
    """Test search filter on role_name (case-insensitive)"""
    job1 = JobOffering(
        id="job-1",
        keyword="backend",
        company_name="Company A",
        role_name="Senior Backend Engineer",
    )
    job2 = JobOffering(
        id="job-2",
        keyword="frontend",
        company_name="Company B",
        role_name="Frontend Developer",
    )
    job3 = JobOffering(
        id="job-3",
        keyword="backend",
        company_name="Company C",
        role_name="Junior Backend Developer",
    )
    
    pg.add_all([job1, job2, job3])
    pg.commit()
    
    # Search "backend" in role_name
    response = client.get("/api/v1/job-offerings?search=backend")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    
    ids = [job["id"] for job in data]
    assert "job-1" in ids
    assert "job-3" in ids
    assert "job-2" not in ids


def test_search_case_insensitive(client, pg):
    """Test that search is case-insensitive"""
    job = JobOffering(
        id="job-1",
        keyword="backend",
        company_name="Google",
        role_name="Engineer",
    )
    pg.add(job)
    pg.commit()
    
    # Different case variations should all work
    for search_term in ["google", "GOOGLE", "GoOgLe", "GOOGLE"]:
        response = client.get(f"/api/v1/job-offerings?search={search_term}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "job-1"


def test_combined_filters_keyword_and_search(client, pg):
    """Test combining keyword exact filter with search"""
    job1 = JobOffering(
        id="job-1",
        keyword="python-backend",
        company_name="Google",
        role_name="Senior Python Engineer",
    )
    job2 = JobOffering(
        id="job-2",
        keyword="python-backend",
        company_name="Amazon",
        role_name="Backend Developer",
    )
    job3 = JobOffering(
        id="job-3",
        keyword="frontend",
        company_name="Google",
        role_name="Frontend Developer",
    )
    job4 = JobOffering(
        id="job-4",
        keyword="python-backend",
        company_name="Meta",
        role_name="Full Stack Engineer",
    )
    
    pg.add_all([job1, job2, job3, job4])
    pg.commit()
    
    # Filter: keyword=python-backend AND search=google
    response = client.get("/api/v1/job-offerings?keyword=python-backend&search=google")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1  # Solo job-1 cumple ambas condiciones
    assert data[0]["id"] == "job-1"
    assert data[0]["keyword"] == "python-backend"
    assert "Google" in data[0]["company_name"]


def test_search_partial_match(client, pg):
    """Test that search works with partial matches"""
    job = JobOffering(
        id="job-1",
        keyword="backend",
        company_name="Google Chile SpA",
        role_name="Software Engineer",
    )
    pg.add(job)
    pg.commit()
    
    # Partial matches should work
    response = client.get("/api/v1/job-offerings?search=chile")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "job-1"


def test_pagination_skip_and_limit(client, pg):
    """Test pagination parameters"""
    # Create 10 job offerings
    jobs = [
        JobOffering(
            id=f"job-{i}",
            keyword="backend",
            company_name=f"Company {i}",
            role_name=f"Role {i}",
        )
        for i in range(10)
    ]
    pg.add_all(jobs)
    pg.commit()
    
    # Test limit
    response = client.get("/api/v1/job-offerings?limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    # Test skip
    response = client.get("/api/v1/job-offerings?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    # IDs should be different from first 5
    first_batch = client.get("/api/v1/job-offerings?skip=0&limit=5").json()
    first_ids = {job["id"] for job in first_batch}
    second_ids = {job["id"] for job in data}
    assert first_ids.isdisjoint(second_ids)  # No overlap


def test_search_no_results(client, pg):
    """Test search with no matching results"""
    job = JobOffering(
        id="job-1",
        keyword="backend",
        company_name="Google",
        role_name="Engineer",
    )
    pg.add(job)
    pg.commit()
    
    response = client.get("/api/v1/job-offerings?search=nonexistent")
    assert response.status_code == 200
    assert response.json() == []


def test_job_offering_with_all_fields(client, pg):
    """Test job offering with all optional fields populated"""
    job = JobOffering(
        id="complete-job",
        keyword="python-backend",
        company_name="Tech Corp",
        role_name="Senior Backend Engineer",
        description="Full job description here",
        url="https://example.com/job/123",
        salary="$100k-$150k",
        location="Remote",
        work_mode="Remote",
        type="Full-time",
        post_date=datetime(2024, 11, 23),
        last_updated=datetime(2024, 11, 23),
        sectors="Technology, Finance",
        extra_data={"benefits": ["health", "dental"], "level": "senior"},
        uid="unique-123",
        api_url="https://api.example.com/jobs/123",
    )
    pg.add(job)
    pg.commit()
    
    response = client.get("/api/v1/job-offerings/complete-job")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == "complete-job"
    assert data["keyword"] == "python-backend"
    assert data["company_name"] == "Tech Corp"
    assert data["role_name"] == "Senior Backend Engineer"
    assert data["description"] == "Full job description here"
    assert data["url"] == "https://example.com/job/123"
    assert data["salary"] == "$100k-$150k"
    assert data["location"] == "Remote"
    assert data["work_mode"] == "Remote"
    assert data["type"] == "Full-time"
    assert data["sectors"] == "Technology, Finance"
    assert data["extra_data"] == {"benefits": ["health", "dental"], "level": "senior"}
    assert data["uid"] == "unique-123"
    assert data["api_url"] == "https://api.example.com/jobs/123"
    assert "created_at" in data
    assert "updated_at" in data


def test_multiple_keywords_different_offerings(client, pg):
    """Test that different keywords can coexist"""
    keywords = ["python-backend", "javascript-frontend", "java-backend", "react-frontend", "devops"]
    
    jobs = [
        JobOffering(
            id=f"job-{i}",
            keyword=keyword,
            company_name=f"Company {i}",
            role_name=f"Role {i}",
        )
        for i, keyword in enumerate(keywords)
    ]
    pg.add_all(jobs)
    pg.commit()
    
    # Test each keyword filter
    for keyword in keywords:
        response = client.get(f"/api/v1/job-offerings?keyword={keyword}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["keyword"] == keyword

