from pathlib import Path

from sqlalchemy.orm import Session

from app.database.models import Template
from app.database.setup import SessionLocal


def seed_templates(db: Session):
    templates_dir = Path(__file__).parent.parent / "templates"
    
    templates_data = [
        {
            "filename": "simple-cv.typ",
            "name": "Simple CV",
            "description": "Clean and simple CV template",
            "template_type": "typst",
            "style": "simple"
        }
    ]
    
    for template_info in templates_data:
        typ_file = templates_dir / template_info["filename"]
        if not typ_file.exists():
            print(f"Warning: {typ_file} not found, skipping...")
            continue
        
        content = typ_file.read_text(encoding="utf-8")
        
        existing = db.query(Template).filter(Template.name == template_info["name"]).first()
        
        if existing:
            existing.template_content = content
            existing.description = template_info["description"]
            existing.template_type = template_info["template_type"]
            existing.style = template_info["style"]
            print(f"Updated template: {template_info['name']}")
        else:
            new_template = Template(
                name=template_info["name"],
                description=template_info["description"],
                template_type=template_info["template_type"],
                template_content=content,
                style=template_info["style"]
            )
            db.add(new_template)
            print(f"Created template: {template_info['name']}")
    
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_templates(db)
        print("Templates seeded successfully!")
    finally:
        db.close()

