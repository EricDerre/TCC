# ! Alteração de IA - Revisar: configuração da CobaiaAPI lida do .env, com os defaults
# de banco iguais aos de Programacao/CobaiaFront/conn/connect.php.
# ! Motivo: os dois alvos (site PHP e API) compartilham o MESMO banco ti93phpdb01 de
# propósito, para que uma reserva criada por um apareça no outro. O connect.php é
# intocado e espera root sem senha — se os defaults daqui divergissem dele, a API
# apontaria para outro banco e os dois alvos mostrariam dados diferentes.
from typing import Optional

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
    # ! Alteração de IA - Revisar: campo-alvo da injeção de falha também lido do .env.
    # ! Motivo: só o FAULT_MODE era lido. Como type_drift, field_missing e field_renamed
    # exigem um campo-alvo (fault_injection.apply_fault só age quando `target_field`
    # existe no dict), FAULT_MODE=type_drift no .env subia a API em modo "normal" na
    # prática — o que contradiz a promessa de execuções determinísticas por variável de
    # ambiente, de que a medição de MTTR/Task Success da Fase 5 depende.
    fault_target_field: Optional[str] = None
    admin_token: str = "troque-isto-localmente"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8"
        )


settings = Settings()
