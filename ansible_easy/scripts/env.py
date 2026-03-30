from pydantic import Field
from pydantic_settings import BaseSettings


class RuntimeEnvironmentModel(BaseSettings):
    log_file_path: str = Field(strict=False, default="/tmp")
    log_file_name: str = Field(strict=False, default="ansible-easy.log")
    log_level: str = Field(strict=False, default="INFO")


runtime = RuntimeEnvironmentModel()
