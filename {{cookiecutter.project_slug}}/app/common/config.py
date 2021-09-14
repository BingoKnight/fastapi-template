import os
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator, Field


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ENV_TYPE: str = "local"
    PROJECT_NAME: str = '{{cookiecutter.project_slug}}'
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        postgres_user = values.get("POSTGRES_USER")
        postgres_password = values.get("POSTGRES_PASSWORD")

        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=postgres_user,
            password=postgres_password,
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
