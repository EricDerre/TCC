# ! Alteração de IA - Revisar
"""
Testes de fumaça contra o banco real compartilhado (ver plano: CobaiaAPI usa
o mesmo MySQL que o CobaiaFront). Requer o banco já populado via
install.py/seed.sql antes de rodar.
"""


def test_listar_produtos(client):
    resp = client.get("/api/produtos")
    assert resp.status_code == 200
    produtos = resp.json()
    assert len(produtos) > 0
    assert {"id", "nome", "tipo", "preco", "destaque"} <= produtos[0].keys()


def test_produto_inexistente(client):
    resp = client.get("/api/produtos/999999")
    assert resp.status_code == 404


def test_fault_mode_requires_token(client):
    resp = client.post("/api/admin/fault-mode", json={"mode": "error_500"})
    assert resp.status_code == 403
