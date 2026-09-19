from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE,env_file_encoding="utf-8",extra="ignore")

    llm_model:str
    llm_base_url:str
    llm_api_key:str

    commerce_api_base_url:str
    database_url:str

    app_host:str
    app_port:int

settings = Settings()

if __name__ == "__main__":
    print(settings.llm_model)