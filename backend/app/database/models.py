from datetime import datetime
from typing import Optional
import enum

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.setup import Base


class SkillType(str, enum.Enum):
    """Enum para tipos de skills"""
    EXPERIENCE = "experience"
    DEV_SKILL = "dev-skill"
    CERTIFICATE = "certificate"
    EXTRA = "extra"


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    user_profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    user_skills: Mapped[list["UserSkills"]] = relationship(
        "UserSkills", back_populates="user", cascade="all, delete-orphan"
    )
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="user", cascade="all, delete-orphan"
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, index=True)
    current_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    years_of_experience: Mapped[Optional[int]] = mapped_column(nullable=True)
    salary_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    spoken_languages: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    user: Mapped["User"] = relationship("User", back_populates="user_profile")


class UserSkills(Base):
    __tablename__ = "user_skills"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    skill_text: Mapped[str] = mapped_column(Text, nullable=False)
    skill_type: Mapped[SkillType] = mapped_column(Enum(SkillType), nullable=False, index=True)
    raw_input: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    user: Mapped["User"] = relationship("User", back_populates="user_skills")


class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    cv_style: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    user: Mapped["User"] = relationship("User", back_populates="projects")
    cvs: Mapped[list["CV"]] = relationship(
        "CV", back_populates="project", cascade="all, delete-orphan"
    )


class Template(Base):
    __tablename__ = "templates"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)
    template_content: Mapped[str] = mapped_column(Text, nullable=False)
    style: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    cvs: Mapped[list["CV"]] = relationship("CV", back_populates="template")


class CV(Base):
    __tablename__ = "cvs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id"), nullable=False, index=True)
    base_cv_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cvs.id"), nullable=True, index=True)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    rendered_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    compiled_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    conversation_history: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    project: Mapped["Project"] = relationship("Project", back_populates="cvs")
    template: Mapped["Template"] = relationship("Template", back_populates="cvs")
    base_cv: Mapped[Optional["CV"]] = relationship(
        "CV", remote_side=[id], back_populates="derived_cvs"
    )
    derived_cvs: Mapped[list["CV"]] = relationship(
        "CV", back_populates="base_cv", cascade="all, delete-orphan"
    )
    application: Mapped[Optional["Application"]] = relationship("Application", back_populates="cv")


class JobOffering(Base):
    __tablename__ = "job_offerings"
    
    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    keyword: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    salary: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    work_mode: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    post_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    sectors: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    uid: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    api_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="job_offering"
    )


class Application(Base):
    __tablename__ = "applications"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    job_offering_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("job_offerings.id"), nullable=False, index=True
    )
    cv_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cvs.id"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    user: Mapped["User"] = relationship("User", back_populates="applications")
    job_offering: Mapped["JobOffering"] = relationship("JobOffering", back_populates="applications")
    cv: Mapped[Optional["CV"]] = relationship("CV", back_populates="application")

