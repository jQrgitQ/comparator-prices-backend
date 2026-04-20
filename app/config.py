from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str | None = None
    app_name: str = "Comparator API"
    debug: bool = True
    secret_key: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()