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


def test_type_drift_em_campo_de_texto_vira_numero(client, modo_de_falha):
    # ! Alteração de IA - Revisar: (26/10/2026) o drift de um campo de texto vira o inteiro 1.
    # ! Motivo: str("Carnes") não mudava nada e o caso semt-16 da avaliação não reproduzia na tela.
    modo_de_falha("type_drift", "tipo")
    p = client.get("/api/produtos/1").json()
    assert p["tipo"] == 1 and isinstance(p["tipo"], int)


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


# ! Alteração de IA - Revisar: testes dos modos novos da ficha 28 (26/10/2026, Fase 4, pacote
# P2): um modo por causa da taxonomia do AgenteCore que a tela consegue mostrar, com o nome da
# própria causa. Escritos antes do código, no mesmo molde dos testes acima (fixture
# modo_de_falha pelo endpoint admin, banco real semeado).
# ! Motivo: os sete modos atuais produzem só 6 das 23 causas e só 20 dos 72 casos de avaliação
# reproduzem na tela (contagem por script em 26/10/2026); sem um modo por causa, a Fase 4
# avaliaria o resto só em texto.


def _normal(client, caminho):
    return client.get(caminho).json()


def test_modos_cobrem_as_causas_da_ficha_28():
    from app.fault_injection import CAUSA_DO_MODO, MODES, NOVOS_MODOS

    assert set(NOVOS_MODOS) == {
        "escala_ou_unidade_errada", "formato_de_data_divergente", "chave_de_juncao_errada",
        "contagem_inconsistente", "nulo_inesperado", "valor_fora_do_dominio", "corpo_vazio",
        "corpo_nao_e_json", "codificacao_incorreta", "limite_de_requisicoes", "recurso_inexistente",
        "registro_duplicado", "estrutura_aninhada_divergente", "colecao_no_lugar_de_objeto",
    }
    assert set(NOVOS_MODOS) <= MODES and "normal" in MODES
    assert CAUSA_DO_MODO["malformed_json"] == "resposta_truncada"
    assert CAUSA_DO_MODO["error_500"] == "erro_interno_do_servidor"
    assert CAUSA_DO_MODO["latency"] == "tempo_de_resposta_excedido"
    assert all(CAUSA_DO_MODO[m] == m for m in NOVOS_MODOS)
    assert len(set(CAUSA_DO_MODO.values())) == 20


def test_escala_ou_unidade_errada_multiplica_por_cem(client, modo_de_falha):
    normal = _normal(client, "/api/produtos/1")
    modo_de_falha("escala_ou_unidade_errada")
    p = client.get("/api/produtos/1").json()
    assert abs(p["preco"] - normal["preco"] * 100) < 1e-6, (p["preco"], normal["preco"])


def test_formato_de_data_divergente_troca_o_iso(modo_de_falha):
    from app.fault_injection import apply_fault

    modo_de_falha("formato_de_data_divergente")
    pedido = apply_fault({"data_pedido": "2026-10-26", "pessoas": 4}, entity="pedido")
    assert pedido["data_pedido"] == "26/10/2026" and pedido["pessoas"] == 4
    assert apply_fault({"id": 1, "preco": 1.0}, entity="produto") == {"id": 1, "preco": 1.0}


def test_chave_de_juncao_errada_troca_o_tipo_por_outro(client, modo_de_falha):
    normal = _normal(client, "/api/produtos")
    modo_de_falha("chave_de_juncao_errada")
    lista = client.get("/api/produtos").json()
    assert [p["id"] for p in lista] == [p["id"] for p in normal]
    assert sorted(p["tipo"] for p in lista) == sorted(p["tipo"] for p in normal)
    assert any(a["tipo"] != b["tipo"] for a, b in zip(normal, lista))
    um = client.get("/api/produtos/1").json()
    assert um["tipo"] != next(p["tipo"] for p in normal if p["id"] == 1)


def test_contagem_inconsistente_tira_um_item(client, modo_de_falha):
    n = len(_normal(client, "/api/produtos"))
    modo_de_falha("contagem_inconsistente")
    assert len(client.get("/api/produtos").json()) == n - 1


def test_nulo_inesperado_zera_o_campo(client, modo_de_falha):
    modo_de_falha("nulo_inesperado", "tipo")
    assert client.get("/api/produtos/1").json()["tipo"] is None


def test_valor_fora_do_dominio(client, modo_de_falha):
    from app.fault_injection import apply_fault

    modo_de_falha("valor_fora_do_dominio", "preco")
    assert client.get("/api/produtos/1").json()["preco"] < 0
    modo_de_falha("valor_fora_do_dominio", "status")
    assert apply_fault({"status": "Em Análise"}, entity="pedido")["status"] == "Pendente"
    modo_de_falha("valor_fora_do_dominio", "destaque")
    assert apply_fault({"destaque": True}, entity="produto")["destaque"] == "talvez"


def test_codificacao_incorreta_estraga_os_acentos(client, modo_de_falha):
    modo_de_falha("codificacao_incorreta", "nome")
    nomes = [p["nome"] for p in client.get("/api/produtos").json()]
    assert any("Ã" in n for n in nomes), nomes
    assert not any("Pão" in n for n in nomes), nomes


def test_registro_duplicado_repete_o_primeiro(client, modo_de_falha):
    n = len(_normal(client, "/api/produtos"))
    modo_de_falha("registro_duplicado")
    lista = client.get("/api/produtos").json()
    assert len(lista) == n + 1 and lista[0]["id"] == lista[1]["id"]


def test_estrutura_aninhada_divergente_aninha_o_campo(client, modo_de_falha):
    normal = _normal(client, "/api/produtos/1")
    modo_de_falha("estrutura_aninhada_divergente", "preco")
    p = client.get("/api/produtos/1").json()
    assert isinstance(p["preco"], dict) and p["preco"]["valor"] == normal["preco"]


def test_colecao_no_lugar_de_objeto_so_no_detalhe(client, modo_de_falha):
    modo_de_falha("colecao_no_lugar_de_objeto")
    um = client.get("/api/produtos/1").json()
    assert isinstance(um, list) and um[0]["id"] == 1
    lista = client.get("/api/produtos").json()
    assert isinstance(lista, list) and isinstance(lista[0], dict)


def test_corpo_vazio_nas_duas_rotas(client, modo_de_falha):
    modo_de_falha("corpo_vazio")
    for caminho in ("/api/produtos", "/api/produtos/1"):
        resp = client.get(caminho)
        assert resp.status_code == 200 and resp.text == "", caminho


def test_corpo_nao_e_json_devolve_html_com_200(client, modo_de_falha):
    modo_de_falha("corpo_nao_e_json")
    resp = client.get("/api/produtos")
    assert resp.status_code == 200 and "text/html" in resp.headers["content-type"]
    with pytest.raises(ValueError):
        resp.json()


def test_limite_de_requisicoes_429_com_retry_after(client, modo_de_falha):
    modo_de_falha("limite_de_requisicoes")
    resp = client.get("/api/produtos")
    assert resp.status_code == 429 and resp.headers["retry-after"] == "60"
    assert client.get("/api/produtos/1").status_code == 429


def test_recurso_inexistente_404_em_id_valido(client, modo_de_falha):
    modo_de_falha("recurso_inexistente")
    assert client.get("/api/produtos/1").status_code == 404
    assert client.get("/api/produtos").status_code == 404
