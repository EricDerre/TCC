# ! Alteração de IA - Revisar
"""
Estado central de fault injection (viabiliza a metodologia de
Fuzzing/Mutação Dinâmica da documentação do TCC). Inicializado por env var
FAULT_MODE no boot (runs determinísticos), sobrescrevível via
POST /api/admin/fault-mode em runtime.

Uso nas rotas (produtos.py/pedidos.py): monte um dict puro a partir do ORM,
chame apply_fault(dict, entity=...) por último, e retorne via
JSONResponse(content=...) explícito — isso faz o FastAPI pular a validação
de response_model, que senão filtraria/desfaria silenciosamente qualquer
campo alterado pela injeção antes de sair pela rede (response_model continua
declarado nas rotas só pra gerar a doc OpenAPI do contrato "normal").

Três famílias de modo (26/10/2026): os que mexem num item (apply_fault),
os que mexem na lista inteira (apply_fault_lista: registro duplicado, item a
menos, tipo trocado entre itens) e os que trocam a resposta inteira
(resposta_especial: corpo truncado, vazio, HTML, 429, 404). malformed_json
continua sendo a resposta truncada de sempre, agora por resposta_especial.
"""
import random
import re
import time
from typing import Any, Optional

from fastapi.responses import JSONResponse, Response

from .config import settings

MODOS_ANTIGOS = {
    "normal",
    "error_500",
    "latency",
    "type_drift",
    "field_missing",
    "field_renamed",
    "malformed_json",
}
# ! Alteração de IA - Revisar: modos novos da ficha 28 (26/10/2026, Fase 4, pacote P2): um por
# causa da taxonomia do AgenteCore que a tela consegue mostrar, com o nome da própria causa.
# CAUSA_DO_MODO diz que causa cada modo produz (os sete antigos têm nome em inglês);
# CAMPO_PADRAO é o campo alvo quando o POST admin não informa target_field.
# ! Motivo: os sete modos antigos produzem só 6 das 23 causas e só 20 dos 72 casos de
# avaliação do AgenteCore reproduzem na tela (contagem por script em 26/10/2026); sem um modo
# por causa, a Fase 4 avaliaria o resto só em texto e a Fase 5 teria seis cenários de
# contrato, todos iguais na mesma página.
NOVOS_MODOS = {
    "escala_ou_unidade_errada",
    "formato_de_data_divergente",
    "chave_de_juncao_errada",
    "contagem_inconsistente",
    "nulo_inesperado",
    "valor_fora_do_dominio",
    "corpo_vazio",
    "corpo_nao_e_json",
    "codificacao_incorreta",
    "limite_de_requisicoes",
    "recurso_inexistente",
    "registro_duplicado",
    "estrutura_aninhada_divergente",
    "colecao_no_lugar_de_objeto",
}
MODES = MODOS_ANTIGOS | NOVOS_MODOS
CAUSA_DO_MODO = {
    "error_500": "erro_interno_do_servidor",
    "latency": "tempo_de_resposta_excedido",
    "type_drift": "tipo_divergente",
    "field_missing": "campo_ausente",
    "field_renamed": "campo_renomeado",
    "malformed_json": "resposta_truncada",
    **{m: m for m in NOVOS_MODOS},
}
CAMPO_PADRAO = {
    "escala_ou_unidade_errada": "preco",
    "formato_de_data_divergente": "data_pedido",
    "chave_de_juncao_errada": "tipo",
    "nulo_inesperado": "tipo",
    "valor_fora_do_dominio": "preco",
    "codificacao_incorreta": "nome",
    "estrutura_aninhada_divergente": "preco",
}
MODOS_DE_LISTA = {"registro_duplicado", "contagem_inconsistente", "chave_de_juncao_errada"}
MODOS_DE_RESPOSTA = {
    "malformed_json",
    "corpo_vazio",
    "corpo_nao_e_json",
    "limite_de_requisicoes",
    "recurso_inexistente",
}
MALFORMED_BODY = '[{"id": 1, "nome": "resposta truncada de propos'
HTML_DE_ERRO = "<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>"


class FaultState:
    def __init__(
        self,
        mode: str = "normal",
        target_field: Optional[str] = None,
        probability: float = 1.0,
    ):
        self.mode = mode if mode in MODES else "normal"
        self.target_field = target_field
        self.probability = probability


# ! Alteração de IA - Revisar: o estado inicial passa a receber também o campo-alvo do .env.
# ! Motivo: sem isso, FAULT_MODE=type_drift/field_missing/field_renamed no .env não tinha
# efeito nenhum — apply_fault() só altera a resposta quando target_field está definido, e
# ele só podia ser definido pelo endpoint admin em tempo de execução.
state = FaultState(mode=settings.fault_mode, target_field=settings.fault_target_field)


class ErrorFault(Exception):
    """Levantada quando o modo error_500 deve disparar — o router converte
    isso num HTTPException 500."""


def _should_apply() -> bool:
    return random.random() < state.probability


def _campo(data: dict[str, Any]) -> Optional[str]:
    """O campo alvo: o do estado ou o padrão do modo, desde que exista no dict."""
    field = state.target_field or CAMPO_PADRAO.get(state.mode)
    return field if field and field in data else None


def _data_br(valor: Any) -> Any:
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(valor))
    return f"{m.group(3)}/{m.group(2)}/{m.group(1)}" if m else valor


def _fora_do_dominio(valor: Any) -> Any:
    if isinstance(valor, bool):
        return "talvez"
    if isinstance(valor, (int, float)):
        return -abs(valor) - 1
    if isinstance(valor, str):
        return "Pendente" if valor in ("Em Análise", "Cancelado") else f"{valor} (inválido)"
    return valor


def apply_fault(data: dict[str, Any], entity: str) -> dict[str, Any]:
    """Aplica o modo de falha ativo a um dict de resposta já pronto. Chame
    por último, logo antes de devolver a resposta. entity é só um rótulo
    (não usado pra filtrar por enquanto) — mantido pra facilitar modos
    futuros que dependam do tipo de entidade. Modos de lista e de resposta
    inteira não passam por aqui (apply_fault_lista e resposta_especial)."""
    if state.mode == "normal" or state.mode in MODOS_DE_RESPOSTA or state.mode in MODOS_DE_LISTA:
        return data
    if not _should_apply():
        return data

    if state.mode == "latency":
        time.sleep(2)
        return data

    if state.mode == "error_500":
        raise ErrorFault(f"fault injection: error_500 em {entity}")

    field = _campo(data)
    if field is None:
        return data
    valor = data[field]
    if state.mode == "type_drift":
        # ! Alteração de IA - Revisar: (26/10/2026) campo que já é texto vira o inteiro 1 (um id
        # no lugar do rótulo); os outros tipos continuam virando texto.
        # ! Motivo: na corrida 17 o único caso que não reproduziu foi `type_drift` em `tipo`:
        # str("Carnes") não muda nada, e o caso gravado descreve o tipo chegando como número.
        data = {**data, field: 1 if isinstance(valor, str) else str(valor)}
    elif state.mode == "field_missing":
        data = {k: v for k, v in data.items() if k != field}
    elif state.mode == "field_renamed":
        data = {**data}
        data[f"{field}_v2"] = data.pop(field)
    # ! Alteração de IA - Revisar: os modos novos de item (ficha 28): preço em centavos, data
    # em DD/MM/AAAA, campo nulo, valor fora do domínio, acentos estragados (utf-8 lido como
    # latin-1) e campo aninhado num objeto.
    # ! Motivo: cada um produz na tela um sintoma da causa de mesmo nome (R$ 8990,00; "destaque:
    # talvez"; "PÃ£o de Alho"; "[object Object]" no preço), sem mudar status nem forma da resposta.
    elif state.mode == "escala_ou_unidade_errada":
        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            data = {**data, field: round(valor * 100, 2)}
    elif state.mode == "formato_de_data_divergente":
        data = {**data, field: _data_br(valor)}
    elif state.mode == "nulo_inesperado":
        data = {**data, field: None}
    elif state.mode == "valor_fora_do_dominio":
        data = {**data, field: _fora_do_dominio(valor)}
    elif state.mode == "codificacao_incorreta":
        if isinstance(valor, str):
            data = {**data, field: valor.encode("utf-8").decode("latin-1")}
    elif state.mode == "estrutura_aninhada_divergente":
        data = {**data, field: {"valor": valor, "moeda": "BRL"}}

    return data


def apply_fault_lista(itens: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """! Alteração de IA - Revisar: os modos que mexem na lista inteira (ficha 28): registro
    duplicado (o primeiro item repetido), contagem inconsistente (o último item some) e chave
    de junção errada (o campo alvo, por padrão `tipo`, gira entre os itens: cada um recebe o
    do seguinte). Um sorteio só por lista.
    ! Motivo: apply_fault vê um item de cada vez e não tem como repetir, tirar ou trocar
    entre itens; sem esta função as causas de contagem, duplicação e junção não teriam modo."""
    if state.mode not in MODOS_DE_LISTA or not itens or not _should_apply():
        return itens
    if state.mode == "registro_duplicado":
        return [itens[0], dict(itens[0]), *itens[1:]]
    if state.mode == "contagem_inconsistente":
        return itens[:-1]
    campo = state.target_field or CAMPO_PADRAO["chave_de_juncao_errada"]
    valores = [item.get(campo) for item in itens]
    girados = valores[1:] + valores[:1]
    return [{**item, campo: v} if campo in item else item for item, v in zip(itens, girados)]


def resposta_especial(entity: str = "produto") -> Optional[Response]:
    """! Alteração de IA - Revisar: a resposta inteira dos modos que não mexem no dict:
    malformed_json (o corpo truncado de sempre), corpo_vazio, corpo_nao_e_json (HTML com 200),
    limite_de_requisicoes (429 com Retry-After) e recurso_inexistente (404 mesmo com id válido).
    None nos outros modos. Estes modos ignoram probability, como malformed_json já ignorava.
    ! Motivo: as rotas testavam só malformed_json por conta própria; com os modos novos de
    resposta, a decisão fica num lugar só e cada rota chama isto antes de consultar o banco."""
    if state.mode not in MODOS_DE_RESPOSTA:
        return None
    if state.mode == "malformed_json":
        return Response(content=MALFORMED_BODY, media_type="application/json")
    if state.mode == "corpo_vazio":
        return Response(content="", media_type="application/json")
    if state.mode == "corpo_nao_e_json":
        return Response(content=HTML_DE_ERRO, media_type="text/html")
    if state.mode == "limite_de_requisicoes":
        return JSONResponse(
            status_code=429,
            content={"detail": "limite de requisições excedido"},
            headers={"Retry-After": "60"},
        )
    return JSONResponse(status_code=404, content={"detail": f"{entity} não encontrado"})
