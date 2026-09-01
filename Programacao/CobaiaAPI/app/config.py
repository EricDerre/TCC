# ! Alteração de IA - Revisar: configuração da CobaiaAPI lida do .env, com os defaults
# de banco iguais aos de Programacao/CobaiaFront/conn/connect.php.
# ! Motivo: os dois alvos (site PHP e API) compartilham o MESMO banco ti93phpdb01 de
# propósito, para que uma reserva criada por um apareça no outro. O connect.php é
# intocado e espera root sem senha — se os defaults daqui divergissem dele, a API
# apontaria para outro banco e os dois alvos mostrariam dados diferentes.
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
