from pathlib import Path

from app.database.models import Template
from app.database.setup import SessionLocal
from app.services.template_service import render_template
from scripts.seed_templates import seed_templates


def test_render():
    """
    Render a test CV using sample data.
    This script seeds templates first, then renders with test data.
    """
    db = SessionLocal()
    try:
        print("Seeding templates...")
        seed_templates(db)
        
        template = db.query(Template).filter(Template.name == "Simple CV").first()
        
        if not template:
            print("Error: Template 'Simple CV' not found after seeding.")
            return
        
        test_data = {
            "firstname": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez@example.com",
            "phone": "+56 9 1234 5678",
            "github": "github.com/juanperez",
            "linkedin": "linkedin.com/in/juanperez",
            "address": "Santiago, Chile",
            "summary": "Desarrollador de software con más de 5 años de experiencia en Python y desarrollo web.",
            "experiences": [
                {
                    "title": "Ingeniero de Software Senior",
                    "company": "Tech Company Inc.",
                    "date": "2020 - Presente",
                    "description": "Lideré el desarrollo de arquitectura de microservicios usando FastAPI y Docker."
                },
                {
                    "title": "Desarrollador de Software",
                    "company": "StartupXYZ",
                    "date": "2018 - 2020",
                    "description": "Desarrollé APIs REST y aplicaciones frontend con React."
                }
            ],
            "education": [
                {
                    "degree": "Ingeniería Civil en Computación",
                    "institution": "Universidad de Chile",
                    "date": "2014 - 2018",
                    "description": "Título profesional con especialización en ingeniería de software."
                }
            ],
            "skills": [
                {
                    "category": "Lenguajes de Programación",
                    "skill_list": "Python, JavaScript, TypeScript"
                },
                {
                    "category": "Frameworks",
                    "skill_list": "FastAPI, React, Django"
                },
                {
                    "category": "Herramientas",
                    "skill_list": "Docker, PostgreSQL, Git"
                }
            ]
        }
        
        rendered = render_template(template, test_data)
        
        output_file = Path(__file__).parent.parent / "templates" / "rendered_test.typ"
        output_file.write_text(rendered, encoding="utf-8")
        
        print(f"\n✅ Template rendered successfully!")
        print(f"📄 Output: {output_file}")
        print(f"\n🔨 To compile to PDF, run:")
        print(f"  typst compile templates/rendered_test.typ templates/rendered_test.pdf")
        
    finally:
        db.close()


if __name__ == "__main__":
    test_render()

