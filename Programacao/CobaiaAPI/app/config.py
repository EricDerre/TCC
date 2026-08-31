# ! Alteração de IA - Revisar
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    # Mesmo banco que Programacao/CobaiaFront/conn/connect.php usa (decisão:
    # 1 banco só compartilhado entre os dois alvos, ver plano).
    db_name: str = "ti93phpdb01"

    fault_mode: str = "normal"
    admin_token: str = "troque-isto-localmente"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8"
        )


settings = Settings()
