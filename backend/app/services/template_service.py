from typing import Optional

from jinja2 import Template as JinjaTemplate
from sqlalchemy.orm import Session

from app.database.models import Template


def get_templates(db: Session) -> list[Template]:
    return db.query(Template).all()


def get_template(db: Session, template_id: int) -> Optional[Template]:
    return db.query(Template).filter(Template.id == template_id).first()


def render_template(template: Template, data: dict) -> str:
    jinja_template = JinjaTemplate(
        template.template_content,
        variable_start_string='<<',
        variable_end_string='>>',
        block_start_string='<%',
        block_end_string='%>'
    )
    
    return jinja_template.render(**data)

