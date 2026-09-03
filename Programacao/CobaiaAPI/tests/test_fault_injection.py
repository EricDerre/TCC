# ! Alteração de IA - Revisar: testes que garantem que a injeção de falha chega de fato à
# resposta HTTP, e que as rotas de pedido respondem como o contrato descreve.
# ! Motivo: a decisão central da CobaiaAPI é devolver JSONResponse explícito para o
# response_model NÃO revalidar a resposta. Se alguém "corrigir" as rotas para o padrão do
# FastAPI, o modo type_drift (preco número -> texto) some silenciosamente antes de sair
# pela rede, o agente deixa de ter o que interceptar, e nenhum teste acusava. Os testes de
# pedido são só de leitura: o banco é o mesmo do CobaiaFront (ti93phpdb01), e criar
# reservas a cada execução da suíte deixaria lixo na área do cliente.
import pytest

from app.config import settings
from app.fault_injection import state


@pytest.fixture
def modo_de_falha(client):
    """Liga um modo de falha pelo endpoint admin e devolve tudo a 'normal' no fim —
    o estado é global no processo e vazaria para os outros testes."""
    def ligar(mode, target_field=None):
        resp = client.post(
            "/api/admin/fault-mode",
            json={"mode": mode, "target_field": target_field},
            headers={"X-Admin-Token": settings.admin_token},
        )
        assert resp.status_code == 200, resp.text
    yield ligar
    state.mode, state.target_field, state.probability = "normal", None, 1.0


def test_type_drift_chega_ao_fio(client, modo_de_falha):
    modo_de_falha("type_drift", "preco")
    produtos = client.get("/api/produtos").json()
    assert produtos and all(isinstance(p["preco"], str) for p in produtos)


def test_field_renamed_chega_ao_fio(client, modo_de_falha):
    modo_de_falha("field_renamed", "preco")
    p = client.get("/api/produtos/1").json()
    assert "preco" not in p and "preco_v2" in p


def test_field_missing_chega_ao_fio(client, modo_de_falha):
    modo_de_falha("field_missing", "destaque")
    assert "destaque" not in client.get("/api/produtos/1").json()


def test_malformed_json_chega_ao_fio(client, modo_de_falha):
    modo_de_falha("malformed_json")
    resp = client.get("/api/produtos")
    assert resp.status_code == 200
    with pytest.raises(ValueError):  # json.JSONDecodeError é subclasse de ValueError
        resp.json()


def test_error_500(client, modo_de_falha):
    modo_de_falha("error_500")
    assert client.get("/api/produtos").status_code == 500


def test_modo_invalido_e_400(client):
    resp = client.post(
        "/api/admin/fault-mode",
        json={"mode": "inexistente"},
        headers={"X-Admin-Token": settings.admin_token},
    )
    assert resp.status_code == 400


def test_listar_pedidos_do_cliente_de_teste(client):
    resp = client.get("/api/pedidos", params={"login": "11122233344"})
    assert resp.status_code == 200
    for p in resp.json():
        assert {"id_pedido", "pessoas", "data_pedido", "status", "nome", "cpf"} <= p.keys()
        assert p["status"] in ("Em Análise", "Cancelado")


def test_listar_pedidos_sem_login_e_422(client):
    assert client.get("/api/pedidos").status_code == 422


def test_listar_pedidos_cliente_inexistente_e_404(client):
    assert client.get("/api/pedidos", params={"login": "00000000000"}).status_code == 404


def test_cancelar_pedido_inexistente_e_404(client):
    assert client.post("/api/pedidos/999999/cancelar").status_code == 404
