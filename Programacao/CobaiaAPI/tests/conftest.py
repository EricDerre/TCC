# ! Alteração de IA - Revisar: fixture única de TestClient apontando para o app real.
# ! Motivo: não há banco de teste isolado — os testes rodam contra o mesmo MariaDB
# populado pelo install.py (decisão de banco único do projeto), então o cliente é
# criado sobre o app de verdade, sem mock de sessão. Consequência prática: os testes
# exigem que o instalador já tenha rodado pelo menos uma vez.
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
