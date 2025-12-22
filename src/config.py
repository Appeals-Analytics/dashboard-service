from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  api_base_url: str
  app_title: str

  model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
