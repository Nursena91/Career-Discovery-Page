from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "career-discovery-agent"
    environment: str = "development"
    debug: bool = True
    enable_live_sources: bool = False
    remotive_api_url: str = "https://remotive.com/api/remote-jobs"
    source_request_timeout_seconds: float = 8.0

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
