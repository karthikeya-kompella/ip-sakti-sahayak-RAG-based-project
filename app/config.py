from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    CHROMA_PERSIST_DIR: str
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    OPENROUTER_API_KEY: str
    GENERATION_MODEL_NAME: str = "nvidia/nemotron-3.5-lightning:free"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()


if __name__ == "__main__":
    print("DATABASE:", settings.DATABASE_URL)
    print("REDIS:", settings.REDIS_URL)
    print("CHROMA:", settings.CHROMA_PERSIST_DIR)
    print("MODEL:", settings.embedding_model_name)

