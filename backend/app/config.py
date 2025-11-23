from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/hackaton_db"
    secret_key: str = "change-this-in-production"
    environment: str = "development"
    debug: bool = True
    anthropic_api_key: str = ""
    admin_username: str = "admin"
    admin_password: str = "admin"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

