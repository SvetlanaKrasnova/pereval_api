import multiprocessing
from typing import Optional

from dotenv import load_dotenv
from pydantic import model_validator, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

load_dotenv()


class AppSettings(BaseSettings):
    input_fstr_db_login: str
    input_fstr_db_pass: str
    input_fstr_db_name: str
    input_fstr_db_host: str
    input_fstr_db_port: int
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: Optional[int] = None
    postgres_dsn: PostgresDsn = None
    model_config = SettingsConfigDict()

    @model_validator(mode='before')
    @classmethod
    def set_postgres_dsn(cls, data: dict) -> Self:
        data['postgres_dsn'] = MultiHostUrl(
            f'postgresql+asyncpg://{data["input_fstr_db_login"]}'
            f':{data["input_fstr_db_pass"]}@{data["input_fstr_db_host"]}'
            f':{data["input_fstr_db_port"]}/{data["input_fstr_db_name"]}',
        )
        return data


app_settings = AppSettings()

uvicorn_options = {
    'host': app_settings.app_host,
    'port': app_settings.app_port,
    'workers': app_settings.cpu_count or multiprocessing.cpu_count(),
    'reload': app_settings.reload,
}
