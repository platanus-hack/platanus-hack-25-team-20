from pydantic import BaseModel


class GeneratedCVContent(BaseModel):
    """Clase base para content generado por LLM según template"""
    pass


class Experience(BaseModel):
    title: str
    company: str
    date: str
    description: str


class Education(BaseModel):
    degree: str
    institution: str
    date: str
    description: str


class Skill(BaseModel):
    category: str
    skill_list: str


class GeneratedCVContentSimple(GeneratedCVContent):
    """Content específico para simple-cv.typ template"""
    firstname: str
    lastname: str
    email: str
    phone: str
    github: str | None = None
    linkedin: str | None = None
    address: str
    summary: str
    experiences: list[Experience]
    education: list[Education]
    skills: list[Skill]

