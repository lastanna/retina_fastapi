import os
import pathlib
from logging import config as logging_config
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = Field(alias='app_title', default='OcuLab')
    project_folder: str = os.path.join(pathlib.Path(__file__).parent.parent.resolve())
    res_path: str = os.path.join(project_folder, 'res')
    models_path: str = os.path.join(project_folder, 'models')
    project_host: str = Field(alias='project_host', default='0.0.0.0')
    project_port: int = Field(alias='project_port', default=8000)
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')

app_settings = AppSettings()

if __name__ == '__main__':
    print(app_settings)