from fastapi import status

from app.database.models import Template


def test_get_templates_empty(client):
    response = client.get("/api/v1/templates")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_templates_with_data(client, pg):
    pg.add(Template(
        name="Test Template",
        description="A test template",
        template_type="typst",
        template_content="Test content",
        style="professional"
    ))
    pg.add(Template(
        name="Another Template",
        description="Another test template",
        template_type="typst",
        template_content="More content",
        style="creative"
    ))
    pg.commit()
    
    response = client.get("/api/v1/templates")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    template_names = [t["name"] for t in data]
    assert "Simple CV" in template_names
    assert "Test Template" in template_names
    assert "Another Template" in template_names
    assert "template_content" not in data[0]


def test_get_template_detail(client, pg):
    template = Template(
        name="Detailed Template",
        description="Template with content",
        template_type="typst",
        template_content="This is the full content",
        style="formal"
    )
    pg.add(template)
    pg.commit()
    pg.refresh(template)
    
    response = client.get(f"/api/v1/templates/{template.id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Detailed Template"
    assert data["template_content"] == "This is the full content"
    assert data["style"] == "formal"


def test_get_template_not_found(client):
    response = client.get("/api/v1/templates/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_render_template_simple(pg):
    from app.services.template_service import render_template
    
    template = Template(
        name="Test",
        template_type="typst",
        template_content="Hello << name >>, your email is << email >>",
        style="test"
    )
    
    result = render_template(template, {
        "name": "John Doe",
        "email": "john@example.com"
    })
    
    assert result == "Hello John Doe, your email is john@example.com"


def test_render_template_with_loop(pg):
    from app.services.template_service import render_template
    
    template = Template(
        name="Test",
        template_type="typst",
        template_content="Skills:\n<% for skill in skills %>\n- << skill >>\n<% endfor %>",
        style="test"
    )
    
    result = render_template(template, {
        "skills": ["Python", "JavaScript", "Docker"]
    })
    
    assert "- Python" in result
    assert "- JavaScript" in result
    assert "- Docker" in result

