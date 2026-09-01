# ! Alteração de IA - Revisar: engine e sessão SQLAlchemy apontando para o mesmo
# MariaDB do CobaiaFront, com pool_pre_ping ligado.
# ! Motivo: o MariaDB é iniciado como subprocesso pelo run.py/Cobaia.exe e encerrado
# junto com eles, então conexões do pool podem ficar órfãs entre execuções; sem o
# pre_ping a primeira requisição depois de um restart falharia com conexão morta.
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
