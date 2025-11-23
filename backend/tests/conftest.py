import pytest
from fastapi.testclient import TestClient
from pytest_mock_resources import create_postgres_fixture

from app.main import app
from app.database.setup import Base, get_db
from scripts.seed_templates import seed_templates

pg = create_postgres_fixture(Base, session=True)


@pytest.fixture
def client(pg):
    
    def override_get_db():
        try:
            yield pg
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    seed_templates(pg)
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

