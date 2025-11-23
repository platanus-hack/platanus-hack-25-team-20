from enum import StrEnum

from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.database.models import User, UserProfile, Project, UserSkills, Template, CV, JobOffering, Application
from app.database.setup import engine


class AdminCategory(StrEnum):
    USERS = "Usuarios"
    PROJECTS = "Proyectos"
    TEMPLATES = "Templates"
    CVS = "CVs"
    JOBS = "Ofertas de Trabajo"
    APPLICATIONS = "Postulaciones"


class EnhancedModelView(ModelView):
    """
    Clase base para vistas de admin con configuraciones comunes.
    """
    can_view_details = True
    can_edit = True
    can_create = True
    can_delete = True
    column_default_sort = "id"
    column_display_pk = True
    form_excluded_columns = ["created_at", "updated_at"]


class UserAdmin(EnhancedModelView, model=User):
    category = AdminCategory.USERS
    name = "Usuario"
    name_plural = "Usuarios"
    icon = "fa-solid fa-user"
    
    column_list = [
        "id",
        "email",
        "full_name",
        "created_at",
        "updated_at",
    ]
    
    column_searchable_list = ["email", "full_name"]
    
    form_columns = ["email", "hashed_password", "full_name"]


class UserProfileAdmin(EnhancedModelView, model=UserProfile):
    category = AdminCategory.USERS
    name = "Perfil de Usuario"
    name_plural = "Perfiles de Usuarios"
    icon = "fa-solid fa-id-card"
    
    column_list = [
        "id",
        "user_id",
        "current_role",
        "years_of_experience",
        "salary_range",
        "created_at",
        "updated_at",
    ]
    
    column_searchable_list = ["current_role"]
    
    form_columns = [
        "user_id",
        "current_role",
        "years_of_experience",
        "salary_range",
        "spoken_languages",
    ]


class ProjectAdmin(EnhancedModelView, model=Project):
    category = AdminCategory.PROJECTS
    name = "Proyecto"
    name_plural = "Proyectos"
    icon = "fa-solid fa-folder"
    
    column_list = [
        "id",
        "user_id",
        "name",
        "target_role",
        "cv_style",
        "created_at",
        "updated_at",
    ]
    
    column_searchable_list = ["name", "target_role"]
    
    form_columns = [
        "user_id",
        "name",
        "target_role",
        "cv_style",
        "preferences",
    ]


class UserSkillsAdmin(EnhancedModelView, model=UserSkills):
    category = AdminCategory.USERS
    name = "Habilidad de Usuario"
    name_plural = "Habilidades de Usuarios"
    icon = "fa-solid fa-star"
    
    column_list = [
        "id",
        "user_id",
        "skill_type",
        "skill_text",
        "source",
        "created_at",
        "updated_at",
    ]
    
    column_searchable_list = ["skill_text", "source"]
    
    form_columns = [
        "user_id",
        "skill_text",
        "skill_type",
        "raw_input",
        "source",
    ]


class TemplateAdmin(EnhancedModelView, model=Template):
    category = AdminCategory.TEMPLATES
    name = "Template"
    name_plural = "Templates"
    icon = "fa-solid fa-file-code"
    
    column_list = [
        "id",
        "name",
        "description",
        "template_type",
        "style",
        "created_at",
    ]
    
    column_searchable_list = ["name", "description"]
    
    form_columns = [
        "name",
        "description",
        "template_type",
        "template_content",
        "style",
    ]


class CVAdmin(EnhancedModelView, model=CV):
    category = AdminCategory.CVS
    name = "CV"
    name_plural = "CVs"
    icon = "fa-solid fa-file-pdf"
    
    column_list = [
        "id",
        "project_id",
        "template_id",
        "base_cv_id",
        "compiled_path",
        "created_at",
        "updated_at",
    ]
    
    form_columns = [
        "project_id",
        "template_id",
        "base_cv_id",
        "content",
        "compiled_path",
        "conversation_history",
    ]
    
    column_details_exclude_list = ["conversation_history"]


class JobOfferingAdmin(EnhancedModelView, model=JobOffering):
    category = AdminCategory.JOBS
    name = "Oferta de Trabajo"
    name_plural = "Ofertas de Trabajo"
    icon = "fa-solid fa-briefcase"
    
    column_list = [
        "id",
        "keyword",
        "company_name",
        "role_name",
        "location",
        "work_mode",
        "type",
        "salary",
        "post_date",
        "created_at",
    ]
    
    column_searchable_list = ["keyword", "company_name", "role_name", "location"]
    
    form_columns = [
        "id",
        "keyword",
        "company_name",
        "description",
        "url",
        "salary",
        "role_name",
        "location",
        "work_mode",
        "type",
        "post_date",
        "last_updated",
        "sectors",
        "extra_data",
        "uid",
        "api_url",
    ]


class ApplicationAdmin(EnhancedModelView, model=Application):
    category = AdminCategory.APPLICATIONS
    name = "Postulación"
    name_plural = "Postulaciones"
    icon = "fa-solid fa-paper-plane"
    
    column_list = [
        "id",
        "user_id",
        "job_offering_id",
        "cv_id",
        "status",
        "created_at",
        "updated_at",
    ]
    
    column_searchable_list = ["status", "notes"]
    
    form_columns = [
        "user_id",
        "job_offering_id",
        "cv_id",
        "status",
        "notes",
    ]


class AdminAuth(AuthenticationBackend):
    """Autenticación básica username/password para la interfaz de admin."""
    
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        valid_username = settings.admin_username
        valid_password = settings.admin_password
        
        if username == valid_username and password == valid_password:
            request.session.update({"authenticated": True})
            return True
        return False
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request) -> bool:
        return request.session.get("authenticated", False)


def setup_admin(app: FastAPI) -> Admin:
    """
    Configura las vistas de SQLAdmin para la aplicación.
    """
    if not settings.secret_key:
        raise ValueError("SECRET_KEY no está configurado")
    
    authentication_backend = AdminAuth(secret_key=settings.secret_key)
    
    admin = Admin(
        app,
        engine,
        title="CV Generator Admin",
        authentication_backend=authentication_backend,
    )
    
    admin.add_view(UserAdmin)
    admin.add_view(UserProfileAdmin)
    admin.add_view(UserSkillsAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(TemplateAdmin)
    admin.add_view(CVAdmin)
    admin.add_view(JobOfferingAdmin)
    admin.add_view(ApplicationAdmin)
    
    return admin

