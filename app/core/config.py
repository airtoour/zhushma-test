from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


load_dotenv()


class DataBaseConfig(BaseSettings):
    """Конфигурация Базы данных"""
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10



class Settings(BaseSettings):
    """Общая конфигурация системы"""
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
    )

    db: DataBaseConfig


settings = Settings()  # type: ignore
