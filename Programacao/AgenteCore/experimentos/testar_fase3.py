#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria o runner de testes da Fase 3 (funções teste_<nome>(),
# main() roda todas na ordem de definição e reporta "<nome> ok" ou falha) e o primeiro
# teste, teste_fixtures_corrigidos(), que confere a correção do achado 4.20 do Memorial
# nos 4 casos sin-1, sin-2, semt-13 e efe-13 de banco_casos.py / banco_casos_extra.py.
# ! Motivo: a regra do harness é zero dependência nova (só biblioteca padrão), então não
# há pytest instalado — sem um runner mínimo os testes da Fase 3 não teriam onde rodar.
# O primeiro teste documenta em código o achado 4.20: até esta correção, sin-1/sin-2/
# semt-13 tinham sintoma "R$ NaN" e efe-13 tinha cartões duplicados, e nenhum dos dois é
# produzido por produtos_api.php de fato (formatarPreco() e o innerHTML do grid,
# linhas 64-67 e 104).
"""Testes de regressão do harness da Fase 3, sem pytest (asserts em Python puro)."""
import inspect
import sys
import traceback

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: mesmo defeito de lá — no Windows o console roda em cp1252, que não imprime
# os símbolos usados nas mensagens de falha (aspas tipográficas, acentos); sem isso o
# runner aborta com UnicodeEncodeError antes de reportar qualquer resultado.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ! Alteração de IA - Revisar: importa biblioteca, recuperação, validar_banco e caminhos,
# além de tempfile/shutil/Path, para os testes da Tarefa 2 (notas do modelo, verbete
# 'aprendido', índice por raiz e caminhos da Fase 3).
# ! Motivo: até aqui o arquivo só testava os fixtures do banco de casos; os testes novos
# precisam montar bibliotecas de mentira em pasta temporária, porque bib.carregar() lê de
# disco e base_conhecimento/ (a biblioteca da Fase 2-B) não pode ser escrita.
# ! Alteração de IA - Revisar: acrescenta json e executar_bateria para os testes da
# Tarefa 3 (leitura tolerante de JSONL, guardas de num_ctx, ambiente residente e
# inferência protegida contra exceção).
# ! Motivo: os testes novos montam JSONL de mentira em disco (json.dumps) e chamam as
# funções extraídas de executar_bateria.py; sem o import não há como testá-las fora do
# próprio módulo.
# ! Alteração de IA - Revisar: acrescenta evolucao_biblioteca para os testes da Tarefa 4
# (partição aprendizado/avaliação, parser de propostas, hash/cópia/diff e fechamento de
# snapshot).
# ! Motivo: os testes novos chamam particionar, parsear_propostas, hash_biblioteca,
# copiar_biblioteca, diff_bibliotecas e fechar_snapshot; sem o import o módulo novo não
# tem onde ser exercitado fora de si mesmo.
# ! Alteração de IA - Revisar: acrescenta os testes da Tarefa 5 — validação das propostas
# (um caso por código de rejeição), aplicação por acréscimo em disco, invariante de
# somente-acréscimo e reconstrução/fechamento de época. Não precisam de import novo: shutil e
# Path, já importados para a limpeza das pastas temporárias, passam a ser usados também para
# apagar e recopiar cópias da biblioteca dentro dos testes.
# ! Motivo: esses testes montam DUAS cópias da biblioteca real (epoca-0 intacta e epoca-1
# editada) em pasta temporária e comparam uma com a outra; com verbete de mentira nenhuma
# das checagens que importam (render_base do alvo para achar o trecho da retificação, teto de
# 800 caracteres de notas, sobreposição com os 90 casos, orçamento do prompt de diagnóstico)
# seria exercitada de verdade.
# ! Alteração de IA - Revisar: acrescenta estrategias para o teste da Tarefa 6 (segundo
# prompt da Fase 3, de proposta de edição -- continuação literal do prompt de diagnóstico
# mais a resposta do modelo, seguida do bloco de correção do caso e das instruções).
# ! Motivo: o teste novo chama estrategias.linear_com_biblioteca (para montar, com um caso
# real de CASOS, o mesmo prompt de diagnóstico que o executor usa) e
# estrategias.proposta_de_edicao; sem o import não haveria como exercitar a função nova
# fora do próprio módulo.
# ! Alteração de IA - Revisar: acrescenta executar_fase3 para os testes da Tarefa 7 (época
# completa de diagnóstico + proposta, retomada depois de interrupção e projeção de tempo).
# ! Motivo: os testes novos chamam executar_fase3.rodar_modelo_fase3 e
# executar_fase3.projecao_tempo, e trocam executar_fase3.oll.gerar por um stub que devolve
# respostas prontas — sem o import não haveria como exercitar o executor sem Ollama ligado
# (uma época real são horas de inferência em CPU).
# ! Alteração de IA - Revisar: acrescenta avaliar e avaliar_fase3 para os testes da Tarefa
# 8 (funções estatísticas escritas à mão e a avaliação inteira da Fase 3 sobre uma árvore
# fase3/ sintética montada em pasta temporária).
# ! Motivo: os testes novos chamam avaliar_fase3.cochran_q, qui_quadrado_sf, holm,
# g_cohen, acuracia_balanceada, distribuicao_de_rotulos e avaliar_saida, e conferem
# avaliar.mcnemar_exato(0, 0) — o p bilateral que o pareado da Fase 3 reaproveita da Fase
# 2-B — no mesmo teste das outras funções, para as duas implementações do mesmo bloco
# estatístico ficarem conferidas lado a lado. Sem os imports não há como exercitar o
# módulo novo fora dele mesmo.
import json
import shutil
import tempfile
from pathlib import Path

import avaliar
import avaliar_fase3
import biblioteca as bib
import caminhos
import estrategias
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import recuperacao
import validar_banco
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from taxonomia import validar_caso

# ! Alteração de IA - Revisar: acrescenta comparar_fases para o teste da Tarefa 9 (comparação
# entre as fases 2-A, 2-B e 3 por modelo).
# ! Motivo: o teste novo chama comparar_fases.gerar_comparacao sobre avaliacao.json/
# avaliacao_fase3.json/resumo_fase3.json de mentira gravados em disco -- sem o import não há
# como exercitar o módulo novo fora dele mesmo.
import comparar_fases

# ! Alteração de IA - Revisar: acrescenta html e gerar_relatorio_fase3 para o teste da Tarefa
# 11 (o relatório HTML navegável da Fase 3 -- resumo, documentação por época, pareado/
# Cochran, propostas e diagnósticos caso a caso com filtros, e diffs por época).
# ! Motivo: o teste novo chama gerar_relatorio_fase3.gerar_relatorio sobre a árvore sintética
# gravada em disco e confere que uma resposta hostil aparece ESCAPADA no HTML comparando com
# html.escape(...) do próprio módulo padrão -- sem os imports não há como exercitar o módulo
# novo nem montar o texto esperado para a comparação.
import html

import gerar_relatorio_fase3


def teste_fixtures_corrigidos() -> None:
    """Achado 4.20 do Memorial: produtos_api.php nunca produz 'R$ NaN' nem duplica
    cartões. formatarPreco(preco) (produtos_api.php:64-67) faz Number(preco) e, se o
    resultado for NaN, devolve String(preco) SEM concatenar 'R$' -- então o que aparece
    na tela é 'undefined' (preco ausente) ou o texto cru '89,90' (vírgula não converte
    para número em JS), nunca 'R$ NaN'. grid.innerHTML =
    produtos.map(cartaoProduto).join("") (linha 104) substitui o conteúdo inteiro do
    grid a cada resposta -- duas respostas nunca se somam em cartões duplicados; o que
    se vê é a última resposta a chegar, mesmo que seja a mais velha. Este teste falhava
    (RED) contra os fixtures originais, que descreviam os dois sintomas que o código
    real não produz."""
    todos = CASOS + CASOS_EXTRA

    ids = [c["id"] for c in todos]
    assert len(todos) == 90, f"esperado 90 casos, achou {len(todos)}"
    assert len(set(ids)) == len(ids), "há id repetido no banco de casos"

    por_id = {c["id"]: c for c in todos}
    trecho_esperado_no_sintoma = {
        "sin-1": "undefined",
        "sin-2": "undefined",
        "semt-13": "89,90",
        "efe-13": "preco antigo",
    }
    for cid, trecho in trecho_esperado_no_sintoma.items():
        caso = por_id[cid]
        problemas = validar_caso(caso)
        assert problemas == [], f"{cid}: gabarito inválido -> {problemas}"
        assert trecho in caso["entrada"]["sintoma"], (
            f"{cid}: sintoma deveria conter {trecho!r} -> {caso['entrada']['sintoma']!r}")

    for caso in todos:
        texto_entrada = " ".join(str(v) for v in caso["entrada"].values())
        assert "R$ NaN" not in texto_entrada, (
            f"{caso['id']}: entrada ainda descreve 'R$ NaN', que produtos_api.php não produz")
        assert "repetido duas vezes" not in texto_entrada, (
            f"{caso['id']}: entrada ainda descreve cartões duplicados, "
            "que o innerHTML do grid (produtos_api.php:104) impede")


# ! Alteração de IA - Revisar: fixtures temporárias dos testes da Fase 3 — quem precisa de
# uma biblioteca de mentira cria a pasta com _pasta_temporaria() e main() apaga todas no fim.
# ! Motivo: os testes de notas do modelo e de verbete 'aprendido' precisam de arquivos .md
# em disco (bib.carregar() só lê de disco) e não podem escrever em base_conhecimento/, que é
# a biblioteca original da Fase 2-B e não muda na Fase 3.
_TEMPORARIOS: list[Path] = []


def _pasta_temporaria() -> Path:
    caminho = Path(tempfile.mkdtemp(prefix="fase3_teste_"))
    _TEMPORARIOS.append(caminho)
    return caminho


def _verbete_em_disco(raiz: Path, relativo: str, texto: str) -> dict:
    """Grava o .md e devolve o verbete já carregado por bib.carregar()."""
    destino = raiz / relativo
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(texto, encoding="utf-8")
    return [v for v in bib.carregar(raiz) if v["caminho"] == destino][0]


def _campo_ausente_com(corpo_extra: str, pasta: str = "erros") -> dict:
    """Cópia de base_conhecimento/erros/campo_ausente.md com um trecho acrescentado ao fim
    do corpo — é a única forma de edição que a Fase 3 permite ao modelo (só acréscimo)."""
    original = (bib.BASE / "erros" / "campo_ausente.md").read_text(encoding="utf-8")
    return _verbete_em_disco(_pasta_temporaria(), f"{pasta}/campo_ausente.md",
                             original.rstrip() + "\n\n" + corpo_extra.strip() + "\n")


_NOTAS_EXEMPLO = (
    "## Notas do modelo\n"
    "- [E1 · sin-4 · nota] Quando o preco vem ausente, o botao mostra a palavra undefined"
    " — Motivo: o caso mostrou o botao com undefined\n"
    '- [E2 · sin-6 · retificação de "nem com nulo"] A chave pode vir ausente ou com nulo;'
    " sao causas diferentes — Motivo: o verbete confundia os dois casos\n"
)

_APRENDIDO = """---
id: nota-precos
titulo: Preco ausente x preco com virgula
sistema: CobaiaAPI
entidade_principal: Produto
tipo: aprendido
status: ativo
palavras_chave: [preco, virgula, undefined, formatacao]
causas_relacionadas: [tipo_divergente]
---
## Resumo
Preco ausente imprime undefined; preco com virgula imprime o texto cru, sem R$.
"""


def teste_render_original_inalterado() -> None:
    """A biblioteca original não tem notas do modelo, então nada do que a Fase 2-B mediu
    pode mudar: render == render_base, o texto indexado pelo BM25 continua o mesmo (a
    fórmula antiga é reproduzida aqui e comparada) e validar() não acusa nada."""
    verbetes = bib.carregar()
    for v in verbetes:
        rot = f"{v['pasta']}/{v['caminho'].name}"
        assert bib.notas(v) == [], f"{rot}: verbete da biblioteca original com notas"
        assert bib.render_notas(v) == "", f"{rot}: render_notas não vazio"
        assert bib.render(v) == bib.render_base(v), f"{rot}: render mudou"
        m = v["meta"]
        antigo = " ".join([
            m.get("titulo", ""), *v["secoes"].values(),
            " ".join(m.get("palavras_chave", [])), " ".join(m.get("sintomas", [])),
            " ".join(m.get("endpoints", [])), m.get("entidade_principal", ""),
        ])
        assert recuperacao._texto_indexavel(v) == antigo, f"{rot}: texto indexado mudou"
    assert bib.validar(verbetes, CASOS + CASOS_EXTRA) == [], "biblioteca original acusada"

    # O teto global continua valendo por padrão (é o da Fase 2-B) e só some com
    # teto_global=None, que é o que a Fase 3 passa: biblioteca dobrada estoura os 6.700.
    dobrada = verbetes + verbetes
    assert any("biblioteca inteira estimada" in p for p in bib.validar(dobrada, [])), \
        "o teto global de tokens deixou de ser checado por padrão"
    assert not any("biblioteca inteira estimada" in p
                   for p in bib.validar(dobrada, [], teto_global=None)), \
        "teto_global=None deveria desligar a checagem do tamanho da biblioteca inteira"


def teste_notas_render_e_validacao() -> None:
    """Notas do modelo: parse (época, caso, operação, trecho, texto, motivo), render que
    leva ao prompt só o texto e a retificação (o motivo fica fora), texto indexável com o
    texto da nota e sem o motivo, e os três limites de validar (formato da linha, 6 notas
    por verbete, 800 caracteres renderizados)."""
    v = _campo_ausente_com(_NOTAS_EXEMPLO)
    rot = "erros/campo_ausente.md"

    ns = bib.notas(v)
    assert len(ns) == 2, f"esperado 2 notas, achou {len(ns)}: {ns}"
    assert ns[0] == {
        "epoca": 1, "caso": "sin-4", "operacao": "nota", "trecho": None,
        "texto": "Quando o preco vem ausente, o botao mostra a palavra undefined",
        "motivo": "o caso mostrou o botao com undefined"}, ns[0]
    assert ns[1] == {
        "epoca": 2, "caso": "sin-6", "operacao": "retificacao", "trecho": "nem com nulo",
        "texto": "A chave pode vir ausente ou com nulo; sao causas diferentes",
        "motivo": "o verbete confundia os dois casos"}, ns[1]

    render_notas = bib.render_notas(v)
    assert render_notas.startswith(" Notas: "), render_notas
    assert "undefined." in render_notas, render_notas
    assert ('Retificação: onde diz "nem com nulo", leia: A chave pode vir ausente ou com '
            "nulo; sao causas diferentes.") in render_notas, render_notas
    assert "Motivo" not in render_notas, f"o motivo não pode ir ao prompt: {render_notas}"
    assert bib.render(v) == bib.render_base(v) + render_notas
    original = [x for x in bib.carregar() if x["id"] == "campo_ausente"][0]
    assert bib.render_base(v) == bib.render_base(original), "render_base cresceu com a nota"

    indexavel = recuperacao._texto_indexavel(v)
    assert "undefined" in indexavel, indexavel
    assert "o caso mostrou" not in indexavel, "o motivo da nota não pode entrar no BM25"

    probs = [p for p in bib.validar([v], [], teto_global=None) if p.startswith(rot)]
    assert probs == [], f"verbete com notas válidas foi acusado: {probs}"

    ruim = _campo_ausente_com(_NOTAS_EXEMPLO + "- nota solta sem formato\n")
    assert len(bib.notas(ruim)) == 2, "a linha malformada não pode virar nota"
    probs = [p for p in bib.validar([ruim], [], teto_global=None) if p.startswith(rot)]
    assert any("nota malformada na linha 3" in p for p in probs), probs

    demais = "## Notas do modelo\n" + "\n".join(
        f"- [E{i} · sin-{i} · nota] nota curta numero {i} — Motivo: motivo {i}"
        for i in range(1, 8))
    v7 = _campo_ausente_com(demais)
    assert len(bib.notas(v7)) == 7
    probs = [p for p in bib.validar([v7], [], teto_global=None) if p.startswith(rot)]
    assert any(f"7 notas do modelo (teto {bib.TETO_NOTAS_POR_VERBETE})" in p
               for p in probs), probs

    longo = "detalhe conferido no caso " + "x" * 280
    grandes = "## Notas do modelo\n" + "\n".join(
        f"- [E{i} · sin-{i} · nota] {longo} — Motivo: motivo {i}" for i in range(1, 4))
    vg = _campo_ausente_com(grandes)
    assert len(bib.render_notas(vg)) > bib.TETO_CHARS_NOTAS_VERBETE
    probs = [p for p in bib.validar([vg], [], teto_global=None) if p.startswith(rot)]
    assert any("notas renderizadas" in p and f"(teto {bib.TETO_CHARS_NOTAS_VERBETE})" in p
               for p in probs), probs


def teste_verbete_aprendido() -> None:
    """Verbete novo escrito pelo modelo: só vale com tipo 'aprendido' DENTRO de
    aprendidos/ e com causas_relacionadas preenchido; e nunca vira verbete de ouro
    (por_causa continua só com tipo 'erro')."""
    v = _verbete_em_disco(_pasta_temporaria(), "aprendidos/nota-precos.md", _APRENDIDO)
    probs = [p for p in bib.validar([v], [], teto_global=None)
             if p.startswith("aprendidos/nota-precos.md")]
    assert probs == [], f"verbete aprendido válido foi acusado: {probs}"
    assert bib.por_causa([v]) == {}, "verbete 'aprendido' não pode virar verbete de ouro"

    fora = _verbete_em_disco(_pasta_temporaria(), "erros/nota-precos.md", _APRENDIDO)
    probs = bib.validar([fora], [], teto_global=None)
    assert any("fora da pasta aprendidos/" in p for p in probs), probs

    sem_causas = _APRENDIDO.replace("causas_relacionadas: [tipo_divergente]\n", "")
    orfao = _verbete_em_disco(_pasta_temporaria(), "aprendidos/nota-precos.md", sem_causas)
    probs = bib.validar([orfao], [], teto_global=None)
    assert any("sem causas_relacionadas" in p for p in probs), probs


def teste_caminhos_fase3() -> None:
    """Tudo da Fase 3 numa subpasta própria, menos os gráficos da corrida oficial, que vão
    para a pasta comum (a numeração das figuras do TCC é uma sequência só)."""
    padrao = caminhos.fase3()
    assert padrao["raiz"].name == "fase3", padrao["raiz"]
    assert padrao["graficos"] == caminhos.GRAFICOS, padrao["graficos"]
    assert padrao["avaliacao"] == padrao["raiz"] / "avaliacao_fase3.json", padrao["avaliacao"]
    piloto = caminhos.fase3("fase3_piloto")
    assert piloto["graficos"].parent.name == "fase3_piloto", piloto["graficos"]
    assert piloto["raiz"].parent == padrao["raiz"].parent


def teste_escrever_indice_raiz() -> None:
    """O índice de uma cópia da Fase 3 é gravado DENTRO da cópia; base_conhecimento/ não
    pode ser tocada (só validar_banco.py --indice, sem --raiz, escreve lá)."""
    tmp = _pasta_temporaria()
    original = (bib.BASE / "erros" / "campo_ausente.md").read_text(encoding="utf-8")
    _verbete_em_disco(tmp, "erros/campo_ausente.md", original)
    indice_base = bib.BASE / "INDICE.md"
    antes_texto = indice_base.read_text(encoding="utf-8")
    antes_mtime = indice_base.stat().st_mtime_ns

    destino = validar_banco.escrever_indice(bib.carregar(tmp), tmp)

    assert destino == tmp / "INDICE.md", destino
    gerado = destino.read_text(encoding="utf-8")
    assert tmp.name in gerado, "o cabeçalho deve dizer de qual raiz é o índice"
    assert "campo_ausente" in gerado, gerado
    assert indice_base.read_text(encoding="utf-8") == antes_texto, "INDICE.md da base mudou"
    assert indice_base.stat().st_mtime_ns == antes_mtime, "INDICE.md da base foi regravado"


def teste_ler_jsonl_tolerante() -> None:
    """ler_jsonl ignora a linha que não parseia (a truncada por uma interrupção no meio da
    gravação) e devolve [] quando o arquivo não existe -- mesma tolerância que
    _ja_feitos já tinha embutida antes da Tarefa 3 extrair a leitura."""
    pasta = _pasta_temporaria()
    arquivo = pasta / "teste.jsonl"
    linhas = [
        json.dumps({"caso": "a", "estrategia": "linear"}, ensure_ascii=False),
        '{"caso": "x", "estrat',  # linha truncada, não fecha o JSON
        json.dumps({"caso": "b", "estrategia": "linear"}, ensure_ascii=False),
    ]
    arquivo.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    registros = executar_bateria.ler_jsonl(arquivo)
    assert len(registros) == 2, f"esperado 2 registros, achou {len(registros)}: {registros}"
    assert [r["caso"] for r in registros] == ["a", "b"], registros

    assert executar_bateria.ler_jsonl(pasta / "nao_existe.jsonl") == []


def teste_guardas_num_ctx() -> None:
    """As duas guardas de num_ctx extraídas de rodar_modelo: a estimada por chars/token
    (antes de inferir) e a real, com a contagem do tokenizador do modelo (depois da
    primeira inferência de cada condição)."""
    assert executar_bateria.guarda_estimativa(2600, 600, "A2") == 1600

    try:
        executar_bateria.guarda_estimativa(2.6 * 8000, 600, "A2")
        assert False, "guarda_estimativa deveria levantar SystemExit acima do num_ctx"
    except SystemExit as e:
        assert "encurtar a biblioteca" in str(e), str(e)

    executar_bateria.guarda_tokens_reais(500, 600, "A2")  # não levanta

    try:
        executar_bateria.guarda_tokens_reais(7600, 600, "A2")
        assert False, "guarda_tokens_reais deveria levantar SystemExit perto do num_ctx"
    except SystemExit as e:
        assert "provável truncamento do prefixo" in str(e), str(e)

    executar_bateria.guarda_tokens_reais(0, 600, "A2")  # tokens_entrada=0: não levanta


def teste_ambiente_residente() -> None:
    """ambiente_residente() resume oll.residentes() nas mesmas três chaves finais que
    rodar_modelo grava em todo registro (somente_cpu, modelos_residentes, memoria_mb)."""
    original = executar_bateria.oll.residentes
    try:
        executar_bateria.oll.residentes = lambda: [
            {"nome": "x", "memoria_mb": 2300, "vram_mb": 0}]
        assert executar_bateria.ambiente_residente() == {
            "somente_cpu": True, "modelos_residentes": 1, "memoria_mb": 2300}

        executar_bateria.oll.residentes = lambda: []
        assert executar_bateria.ambiente_residente() == {
            "somente_cpu": True, "modelos_residentes": 0, "memoria_mb": None}
    finally:
        executar_bateria.oll.residentes = original


def teste_inferir_seguro() -> None:
    """inferir_seguro() captura qualquer exceção de oll.gerar (rede/timeout) e devolve o
    mesmo dicionário de erro que rodar_modelo gravava embutido, sem derrubar a bateria."""
    original = executar_bateria.oll.gerar

    def _levanta(modelo, prompt, max_tokens):
        raise TimeoutError("x")

    try:
        executar_bateria.oll.gerar = _levanta
        r = executar_bateria.inferir_seguro("modelo-x", "prompt", 600)
        assert r == {"segundos": None, "tokens_entrada": 0, "tokens_saida": 0,
                     "resposta": "", "erro": "TimeoutError: x"}, r
    finally:
        executar_bateria.oll.gerar = original


def teste_particao() -> None:
    """particionar() tem de dar 18 células (classe, nível) de 5 casos cada, 3 para
    aprendizado e 2 para avaliação -- e repetir a chamada com o mesmo banco de casos tem
    de dar o mesmo resultado (o hash não depende de nenhum estado externo).
    gravar_ou_conferir_particao grava na primeira chamada e, daí em diante, só confere: um
    particao.json gravado por uma regra ou um banco de casos diferente tem de parar a
    execução, nunca seguir silenciosamente com uma partição misturada entre modelos."""
    todos = CASOS + CASOS_EXTRA
    particao = evo.particionar(todos)
    assert particao["n_aprendizado"] == 54, particao["n_aprendizado"]
    assert particao["n_avaliacao"] == 36, particao["n_avaliacao"]

    por_celula: dict[tuple[int, int], dict[str, int]] = {}
    for info in particao["casos"].values():
        chave = (info["classe"], info["nivel"])
        cont = por_celula.setdefault(chave, {"aprendizado": 0, "avaliacao": 0})
        cont[info["particao"]] += 1
    assert len(por_celula) == 18, len(por_celula)
    for chave, cont in por_celula.items():
        assert cont == {"aprendizado": 3, "avaliacao": 2}, f"{chave}: {cont}"

    assert len(particao["casos"]) == 90, len(particao["casos"])
    assert len(set(particao["casos"])) == 90, "id repetido em casos"

    outra = evo.particionar(todos)
    assert outra == particao, "particionar não é determinístico"

    pasta = _pasta_temporaria()
    caminho = pasta / "particao.json"
    gravado = evo.gravar_ou_conferir_particao(caminho, particao)
    assert gravado == particao, gravado
    assert caminho.exists()
    conferido = evo.gravar_ou_conferir_particao(caminho, particao)
    assert conferido == particao, conferido

    diferente = json.loads(json.dumps(particao))
    algum_id = next(iter(diferente["casos"]))
    atual = diferente["casos"][algum_id]["particao"]
    diferente["casos"][algum_id]["particao"] = (
        "avaliacao" if atual == "aprendizado" else "aprendizado")
    caminho_divergente = pasta / "particao_divergente.json"
    caminho_divergente.write_text(json.dumps(diferente, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
    try:
        evo.gravar_ou_conferir_particao(caminho_divergente, particao)
        assert False, "particao divergente deveria levantar SystemExit"
    except SystemExit as e:
        assert "particao.json existente difere" in str(e), str(e)

    # Os 4 casos cujo enunciado mudou entre a 2-B e a Fase 3 (achado 4.20) caem em
    # 'aprendizado' pelo sha256 — é o que comparar_fases.py pressupõe ao parear 2B_A2 x F3_L0
    # nos 36 de avaliação (que então não contêm nenhum enunciado diferente entre as fases).
    # Se a semente ou o banco mudarem e algum for para 'avaliacao', este assert acusa e a
    # Tabela 5 do Memorial precisa ser reescrita, não a regra da partição.
    for caso_id in ("sin-1", "sin-2", "semt-13", "efe-13"):
        assert evo.particao_de(particao, caso_id) == "aprendizado", (
            f"{caso_id}: {evo.particao_de(particao, caso_id)} — o pareamento nos 36 da "
            "comparação entre fases pressupõe os 4 fixtures corrigidos em aprendizado")


def teste_parser_propostas() -> None:
    """parsear_propostas lê o texto livre que o modelo devolve para a proposta de edição:
    blocos PROPOSTA n .. FIM com campos CAMPO: valor, tolerando negrito, VERBETE com ou sem
    colchetes, TEXTO partido em duas linhas e a palavra NENHUMA (solta ou dentro de um
    bloco) -- e sinaliza quando a resposta parece ter sido cortada pelo teto de tokens."""
    dois_blocos = (
        "PROPOSTA 1\n"
        "OPERACAO: nota\n"
        "VERBETE: campo_ausente\n"
        "TEXTO: Quando o preco vem ausente, o botao mostra a palavra undefined\n"
        "MOTIVO: o caso mostrou o botao com undefined\n"
        "FIM\n"
        "PROPOSTA 2\n"
        "OPERACAO: retificacao\n"
        "VERBETE: [tipo_divergente]\n"
        "TEXTO: A data pode vir com hora junto do dia\n"
        "MOTIVO: o verbete nao previa hora no campo de data\n"
        "FIM\n"
    )
    r = evo.parsear_propostas(dois_blocos)
    assert r["nenhuma"] is False, r
    assert len(r["blocos"]) == 2, r["blocos"]
    assert all(b["malformado"] is None for b in r["blocos"]), r["blocos"]
    assert r["blocos"][0]["campos"]["OPERACAO"] == "nota", r["blocos"][0]
    assert r["blocos"][0]["campos"]["VERBETE"] == "campo_ausente", r["blocos"][0]
    assert r["blocos"][1]["campos"]["VERBETE"] == "tipo_divergente", r["blocos"][1]

    r_nenhuma = evo.parsear_propostas("NENHUMA")
    assert r_nenhuma["nenhuma"] is True, r_nenhuma
    assert r_nenhuma["blocos"] == [], r_nenhuma

    # Sem contagem de tokens não há como dizer que a resposta foi cortada, então o bloco
    # completo que termina sem FIM vale (ver teste_parser_fim_ausente).
    sem_fim = "PROPOSTA 1\nOPERACAO: nota\nVERBETE: x\nTEXTO: abc\nMOTIVO: def\n"
    r_sem_fim = evo.parsear_propostas(sem_fim)
    assert len(r_sem_fim["blocos"]) == 1, r_sem_fim
    assert r_sem_fim["blocos"][0]["malformado"] is None, r_sem_fim
    assert r_sem_fim["blocos"][0]["fim_ausente"] is True, r_sem_fim
    assert all("fim_ausente" in b for b in r["blocos"]), r["blocos"]

    duas_linhas = ("PROPOSTA 1\nOPERACAO: nota\nVERBETE: x\nTEXTO: primeira parte\n"
                  "segunda parte\nMOTIVO: motivo qualquer\nFIM\n")
    r_duas = evo.parsear_propostas(duas_linhas)
    assert r_duas["blocos"][0]["campos"]["TEXTO"] == "primeira parte segunda parte", r_duas

    negrito = ("**PROPOSTA 1**\n**OPERACAO:** nota\nVERBETE: x\nTEXTO: abc\nMOTIVO: def\n"
              "FIM\n")
    r_negrito = evo.parsear_propostas(negrito)
    assert r_negrito["blocos"][0]["malformado"] is None, r_negrito
    assert r_negrito["blocos"][0]["campos"]["OPERACAO"] == "nota", r_negrito

    com_colchetes = "PROPOSTA 1\nOPERACAO: nota\nVERBETE: [campo_ausente]\nTEXTO: abc\nMOTIVO: def\nFIM\n"
    sem_colchetes = com_colchetes.replace("[campo_ausente]", "campo_ausente")
    assert evo.parsear_propostas(com_colchetes)["blocos"][0]["campos"]["VERBETE"] == "campo_ausente"
    assert evo.parsear_propostas(sem_colchetes)["blocos"][0]["campos"]["VERBETE"] == "campo_ausente"

    sem_motivo = "PROPOSTA 1\nOPERACAO: nota\nVERBETE: x\nTEXTO: abc\nFIM\n"
    r_sem_motivo = evo.parsear_propostas(sem_motivo)
    assert r_sem_motivo["blocos"][0]["malformado"] == "falta MOTIVO", r_sem_motivo

    op_nenhuma = "PROPOSTA 1\nOPERACAO: nenhuma\nFIM\n"
    r_op_nenhuma = evo.parsear_propostas(op_nenhuma)
    assert r_op_nenhuma["nenhuma"] is True, r_op_nenhuma
    assert r_op_nenhuma["blocos"][0]["malformado"] is None, r_op_nenhuma

    incompleta = "PROPOSTA 1\nOPERACAO: nota\nVERBETE: x\nTEXTO: abc\nMOTIVO: def\n"
    r_truncada = evo.parsear_propostas(incompleta, tokens_saida=700, max_tokens=700)
    assert r_truncada["truncada"] is True, r_truncada
    assert r_truncada["blocos"][0]["malformado"] == "sem FIM", r_truncada
    r_nao_truncada = evo.parsear_propostas(incompleta, tokens_saida=100, max_tokens=700)
    assert r_nao_truncada["truncada"] is False, r_nao_truncada
    assert r_nao_truncada["blocos"][0]["malformado"] is None, r_nao_truncada


def teste_parser_campo_fechado() -> None:
    """CAMPOS_PROPOSTA é um conjunto FECHADO: uma linha só abre um campo novo se o nome dela
    (maiúsculo, sem acento) estiver nesse conjunto -- uma linha 'Exemplo: ...' escrita pelo
    modelo dentro do TEXTO não pode virar um campo 'EXEMPLO' e cortar o texto ao meio; e
    minúsculas continuam abrindo campo normalmente ('texto:' abre TEXTO)."""
    resposta = (
        "PROPOSTA 1\n"
        "operacao: nota\n"
        "verbete: x\n"
        "texto: Antes de comparar dois numeros\n"
        "Exemplo: 10 e 10.0 sao considerados iguais\n"
        "motivo: o verbete nao citava exemplo\n"
        "FIM\n"
    )
    r = evo.parsear_propostas(resposta)
    assert r["blocos"][0]["malformado"] is None, r["blocos"]
    assert r["blocos"][0]["campos"]["OPERACAO"] == "nota", r["blocos"][0]
    texto = r["blocos"][0]["campos"]["TEXTO"]
    assert "Exemplo:" in texto, texto
    assert texto == ("Antes de comparar dois numeros Exemplo: 10 e 10.0 sao considerados "
                     "iguais"), texto
    assert "EXEMPLO" not in r["blocos"][0]["campos"], r["blocos"][0]["campos"]


def teste_parser_fim_ausente() -> None:
    """Bloco que chega ao fim da resposta (ou à PROPOSTA seguinte) sem a linha FIM.

    No piloto real da Fase 3, o qwen2.5-coder:3b escreveu os 12 campos do bloco e
    simplesmente não escreveu o FIM -- em respostas de 185 a 192 tokens, com teto de 700,
    isto é, sem nenhum corte. Pelas regras antigas as 6 propostas do piloto foram recusadas
    como 'sem FIM' e a biblioteca não cresceu. Quem diz se a resposta foi cortada é a
    contagem de tokens, não a palavra FIM: sem corte e com os quatro campos obrigatórios
    escritos, o bloco vale e sai marcado com fim_ausente=True para a avaliação contar
    quantas propostas chegaram assim."""
    sem_fim = ("PROPOSTA 1\n"
               "OPERACAO: nota\n"
               "VERBETE: campo_ausente\n"
               "TEXTO: Quando o preco nao vem, o botao imprime undefined\n"
               "MOTIVO: o verbete nao dizia o que aparece no botao\n")

    completo = evo.parsear_propostas(sem_fim, tokens_saida=190, max_tokens=700)
    assert len(completo["blocos"]) == 1, completo
    assert completo["truncada"] is False, completo
    assert completo["blocos"][0]["malformado"] is None, completo["blocos"]
    assert completo["blocos"][0]["fim_ausente"] is True, completo["blocos"]
    assert completo["blocos"][0]["campos"]["MOTIVO"] == (
        "o verbete nao dizia o que aparece no botao"), completo["blocos"]

    cortado = evo.parsear_propostas(sem_fim, tokens_saida=700, max_tokens=700)
    assert cortado["truncada"] is True, cortado
    assert cortado["blocos"][0]["malformado"] == "sem FIM", cortado["blocos"]

    sem_texto = ("PROPOSTA 1\nOPERACAO: nota\nVERBETE: campo_ausente\n"
                 "MOTIVO: o verbete nao dizia o que aparece no botao\n")
    faltando = evo.parsear_propostas(sem_texto, tokens_saida=120, max_tokens=700)
    assert faltando["blocos"][0]["malformado"] == "falta TEXTO", faltando["blocos"]
    assert faltando["blocos"][0]["fim_ausente"] is True, faltando["blocos"]

    com_fim = evo.parsear_propostas(sem_fim + "FIM\n", tokens_saida=195, max_tokens=700)
    assert com_fim["blocos"][0]["malformado"] is None, com_fim["blocos"]
    assert com_fim["blocos"][0]["fim_ausente"] is False, com_fim["blocos"]

    # O executor grava propostas_parseadas como veio: a chave existe em TODO bloco.
    for resultado in (completo, cortado, faltando, com_fim):
        for b in resultado["blocos"]:
            assert "fim_ausente" in b, b


def teste_parser_proposta_nova_fecha_anterior_sem_fim() -> None:
    """PROPOSTA 2 começando antes do FIM do bloco 1 fecha o bloco 1 ali mesmo: com os
    quatro campos obrigatórios escritos e sem corte na resposta, o bloco 1 vale e sai
    marcado com fim_ausente=True; sem algum dos campos, continua 'falta <CAMPO>'."""
    resposta = (
        "PROPOSTA 1\n"
        "OPERACAO: nota\n"
        "VERBETE: x\n"
        "TEXTO: bloco que esqueceu o FIM\n"
        "MOTIVO: motivo do bloco 1\n"
        "PROPOSTA 2\n"
        "OPERACAO: nota\n"
        "VERBETE: y\n"
        "TEXTO: bloco fechado corretamente\n"
        "MOTIVO: motivo do bloco 2\n"
        "FIM\n"
    )
    r = evo.parsear_propostas(resposta)
    assert len(r["blocos"]) == 2, r["blocos"]
    assert r["blocos"][0]["malformado"] is None, r["blocos"][0]
    assert r["blocos"][0]["fim_ausente"] is True, r["blocos"][0]
    assert r["blocos"][0]["campos"]["VERBETE"] == "x", r["blocos"][0]
    assert r["blocos"][1]["malformado"] is None, r["blocos"][1]
    assert r["blocos"][1]["fim_ausente"] is False, r["blocos"][1]
    assert r["blocos"][1]["campos"]["VERBETE"] == "y", r["blocos"][1]

    # Sem MOTIVO, o bloco 1 continua sendo acusado -- o que mudou foi só a exigência do FIM.
    sem_motivo = resposta.replace("MOTIVO: motivo do bloco 1\n", "")
    r2 = evo.parsear_propostas(sem_motivo)
    assert r2["blocos"][0]["malformado"] == "falta MOTIVO", r2["blocos"][0]
    assert r2["blocos"][0]["fim_ausente"] is True, r2["blocos"][0]


def teste_particao_exige_18_celulas() -> None:
    """particionar() tem de exigir exatamente 18 células (classe, nível) -- não só 5 casos
    por célula. Uma 19ª célula (mesmo com 5 casos nela, como as demais) nunca seria notada
    pela checagem "5 por célula" sozinha, e a Fase 3 espera sempre as 18 combinações fixas
    de classe x nível (ver taxonomia.CLASSES/NIVEIS)."""
    base = list(CASOS + CASOS_EXTRA)
    duplicada = [
        {**c, "id": f"{c['id']}-dup{i}", "classe": 1, "nivel": 99}
        for i, c in enumerate(c for c in base if c["classe"] == 1 and c["nivel"] == 1)
    ]
    noventa_e_cinco = base + duplicada
    assert len(noventa_e_cinco) == 95, len(noventa_e_cinco)
    try:
        evo.particionar(noventa_e_cinco)
        assert False, "19 células deveria levantar ValueError"
    except ValueError as e:
        assert "18" in str(e), str(e)


def teste_arquivos_md_ignora_indice_sem_case() -> None:
    """_arquivos_md ignora INDICE.md em qualquer variação de maiúsculas/minúsculas -- a
    mesma tolerância que bib.carregar() já tem (arq.name.upper() == "INDICE.MD") -- para
    hash_biblioteca e diff_bibliotecas nunca confundirem um índice gerado com um verbete
    novo, independente de como o índice foi nomeado."""
    raiz = _pasta_temporaria()
    _verbete_em_disco(raiz, "erros/campo_ausente.md",
                      (bib.BASE / "erros" / "campo_ausente.md").read_text(encoding="utf-8"))
    (raiz / "indice.md").write_text("# indice gerado em minusculo\n", encoding="utf-8")
    assert "indice.md" not in evo._arquivos_md(raiz), evo._arquivos_md(raiz)


def teste_hash_copia_diff_fechamento() -> None:
    """Hash determinístico por conteúdo (duas cópias da mesma origem batem; um byte a mais
    já diverge), cópia sem INDICE.md, diff por arquivo (novo/tocado, linhas e por_verbete
    com a nota ACRESCENTADA nesta comparação) e o fechamento de época gravando
    fechamento.json com os mesmos números que hash_biblioteca/contar_notas calculam."""
    raiz = _pasta_temporaria()
    a = evo.copiar_biblioteca(bib.BASE, raiz / "a")
    b = evo.copiar_biblioteca(bib.BASE, raiz / "b")
    assert not (a / "INDICE.md").exists(), "a cópia não deveria trazer o INDICE.md"
    assert not (b / "INDICE.md").exists(), "a cópia não deveria trazer o INDICE.md"

    hash_a = evo.hash_biblioteca(a)
    assert evo.hash_biblioteca(b) == hash_a, "cópias da mesma origem deveriam bater"

    campo_ausente_b = b / "erros" / "campo_ausente.md"
    with campo_ausente_b.open("ab") as f:
        f.write(b"\n")
    assert evo.hash_biblioteca(b) != hash_a, "um byte a mais já deveria mudar o hash"

    # Verbete novo (tipo 'aprendido', operação novo_verbete) só em b.
    (b / "aprendidos").mkdir(parents=True, exist_ok=True)
    (b / "aprendidos" / "x.md").write_text(
        _APRENDIDO.replace("id: nota-precos", "id: x"), encoding="utf-8")

    # Nota do modelo acrescentada ao FINAL de erros/campo_ausente.md -- a única forma de
    # edição que a Fase 3 permite num verbete existente.
    texto_atual = campo_ausente_b.read_text(encoding="utf-8")
    nota = ('- [E1 · sin-4 · nota] Quando o preco vem ausente, o botao mostra undefined'
           ' — Motivo: o caso mostrou o botao com undefined\n')
    campo_ausente_b.write_text(
        texto_atual.rstrip("\n") + "\n\n## Notas do modelo\n" + nota, encoding="utf-8")

    diff = evo.diff_bibliotecas(a, b)
    assert diff["arquivos_novos"] == ["aprendidos/x.md"], diff["arquivos_novos"]
    assert diff["arquivos_tocados"] == ["erros/campo_ausente.md"], diff["arquivos_tocados"]
    assert diff["linhas_acrescentadas"] >= 2, diff["linhas_acrescentadas"]
    assert diff["por_verbete"]["campo_ausente"]["notas"] == 1, diff["por_verbete"]
    assert "+++ b/erros/campo_ausente.md" in diff["unificado"], diff["unificado"]

    destino = raiz / "diff_a_b"
    escrito = evo.escrever_diff(a, b, destino, "a", "b")
    assert escrito == diff, escrito
    assert destino.with_suffix(".json").exists()
    assert destino.with_suffix(".md").exists()
    gravado = json.loads(destino.with_suffix(".json").read_text(encoding="utf-8"))
    assert "unificado" not in gravado, gravado

    # A Fase 3 nomeia os arquivos de diff pelo nome do modelo (ex.: qwen2.5-coder_3b), que
    # tem ponto -- Path.with_suffix() trocaria tudo depois do ÚLTIMO ponto, truncando o
    # nome (isso é o que este bloco protege).
    destino_pontuado = raiz / "diff__E1__qwen2.5-coder_3b"
    evo.escrever_diff(a, b, destino_pontuado, "a", "b")
    assert (raiz / "diff__E1__qwen2.5-coder_3b.json").exists(), (
        "nome com ponto (qwen2.5-coder) não pode truncar a extensão do .json")
    assert (raiz / "diff__E1__qwen2.5-coder_3b.md").exists(), (
        "nome com ponto (qwen2.5-coder) não pode truncar a extensão do .md")

    fechamento = evo.fechar_snapshot(b, 1, "modelo-x", 2)
    assert fechamento["hash"] == evo.hash_biblioteca(b), fechamento
    assert fechamento["n_verbetes_novos"] == 1, fechamento
    assert fechamento["n_notas"] == 1, fechamento
    assert fechamento["aceitas_na_epoca"] == 2, fechamento
    assert evo.snapshot_fechado(b) is True
    assert evo.snapshot_fechado(a) is False

    try:
        evo.copiar_biblioteca(bib.BASE, a)
        assert False, "copiar_biblioteca para destino existente deveria levantar FileExistsError"
    except FileExistsError:
        pass


# ! Alteração de IA - Revisar: fixture da Tarefa 5 — duas cópias temporárias da biblioteca
# original (epoca-0 e epoca-1) e o ctx que validar_proposta recebe do executor.
# ! Motivo: validar_proposta decide contra a biblioteca REAL (render_base do alvo, teto de
# notas, sobreposição com os 90 casos, orçamento do prompt de diagnóstico); um verbete de
# mentira com duas linhas não exercitaria nenhuma dessas checagens. epoca-0 fica intacta
# para conferir_somente_acrescimo ter contra o que comparar, e base_conhecimento/ nunca é
# escrita.
_TEXTO_VALIDO = ("Quando a chave de preco nao vem no objeto do produto, o botao de detalhe "
                 "imprime a palavra undefined em vez do valor formatado")
_MOTIVO_VALIDO = "o verbete nao dizia o que aparece no botao quando falta o preco"


def _ambiente_proposta() -> tuple[Path, dict]:
    tmp = _pasta_temporaria()
    evo.copiar_biblioteca(bib.BASE, tmp / "epoca-0")
    evo.copiar_biblioteca(tmp / "epoca-0", tmp / "epoca-1")
    raiz = tmp / "epoca-1"
    ctx = {"raiz": raiz, "verbetes": bib.carregar(raiz), "casos": CASOS + CASOS_EXTRA,
           "ids_visiveis": {"campo_ausente", "contrato-produto", "entidade-produto"},
           "epoca": 1, "caso_id": "sin-4", "modelo": "teste",
           "novos_nesta_epoca": 0, "aceitas_no_caso": 0, "k": 3}
    return tmp, ctx


def _bloco(numero: int = 1, malformado: str | None = None, **campos) -> dict:
    """Bloco no formato que parsear_propostas devolve, partindo da proposta válida de
    referência (nota em campo_ausente) e trocando só o que o teste quer testar. Campo com
    valor None é REMOVIDO, para simular o campo que o modelo esqueceu."""
    base = {"OPERACAO": "nota", "VERBETE": "campo_ausente",
            "TEXTO": _TEXTO_VALIDO, "MOTIVO": _MOTIVO_VALIDO}
    base.update(campos)
    return {"numero": numero, "malformado": malformado,
            "campos": {k: v for k, v in base.items() if v is not None}}


def teste_validar_proposta_aceita() -> None:
    """A proposta de referência (nota curta em campo_ausente, verbete visível no
    diagnóstico) passa pelas 26 checagens e devolve a edição que aplicar_edicao grava:
    arquivo relativo em posix, operação, texto/motivo e as listas de frontmatter vazias."""
    _tmp, ctx = _ambiente_proposta()
    r = evo.validar_proposta(_bloco(), ctx)

    assert r["aceita"] is True, r
    assert r["motivo"] is None, r
    edicao = r["edicao"]
    assert edicao["arquivo"] == "erros/campo_ausente.md", edicao
    assert edicao["operacao"] == "nota", edicao
    assert edicao["verbete"] == "campo_ausente", edicao
    assert edicao["epoca"] == 1 and edicao["caso"] == "sin-4", edicao
    assert edicao["modelo"] == "teste", edicao
    assert edicao["texto"] == _TEXTO_VALIDO, edicao
    assert edicao["motivo"] == _MOTIVO_VALIDO, edicao
    assert edicao["trecho"] is None, edicao
    assert edicao["novo"] is None, edicao
    assert edicao["palavras_chave_novas"] == [], edicao
    assert edicao["sintomas_novos"] == [], edicao

    # Listas do frontmatter: vêm por vírgula, normalizadas, e "nenhuma" vira lista vazia.
    r2 = evo.validar_proposta(
        _bloco(PALAVRAS_CHAVE="Botão, undefined", SINTOMAS="nenhuma"), ctx)
    assert r2["aceita"] is True, r2
    assert r2["edicao"]["palavras_chave_novas"] == ["botao", "undefined"], r2["edicao"]
    assert r2["edicao"]["sintomas_novos"] == [], r2["edicao"]

    # novo_verbete: SISTEMA/ENTIDADE ausentes viram o padrão (Ambos + entidade do caso),
    # para não rejeitar o modelo pequeno por campo esquecido.
    r3 = evo.validar_proposta(
        _bloco(OPERACAO="novo_verbete", VERBETE="preco-ausente-no-botao",
               TITULO="Preco ausente no botao de detalhe", CAUSAS="campo_ausente"), ctx)
    assert r3["aceita"] is True, r3
    edicao3 = r3["edicao"]
    assert edicao3["arquivo"] == "aprendidos/preco-ausente-no-botao.md", edicao3
    assert edicao3["novo"]["sistema"] == "Ambos", edicao3["novo"]
    assert edicao3["novo"]["entidade"] in bib.ENTIDADES, edicao3["novo"]
    assert edicao3["novo"]["causas"] == ["campo_ausente"], edicao3["novo"]

    # Id com sublinhado e hífen no mesmo nome é válido (é a forma dos ids de erros/, como
    # campo_ausente, misturada com a das pastas negocio/contratos, como contrato-produto).
    r4 = evo.validar_proposta(
        _bloco(OPERACAO="novo_verbete", VERBETE="nota-precos_2",
               TITULO="Preco ausente e preco com virgula", CAUSAS="campo_ausente"), ctx)
    assert r4["aceita"] is True, r4
    assert r4["edicao"]["arquivo"] == "aprendidos/nota-precos_2.md", r4["edicao"]


def teste_motivos_de_rejeicao() -> None:
    """Um caso por código de rejeição, cada um partindo da proposta válida e mudando UM
    campo ou UMA condição do ctx. O que este teste protege é a ORDEM: a primeira checagem
    que falha decide o código, e o histograma de rejeições do relatório só é comparável
    entre modelos se o mesmo defeito cair sempre no mesmo código. Ao final, confere que
    todo código de CODIGOS_REJEICAO foi exercitado (menos pasta_invalida, defensivo)."""
    _tmp, ctx = _ambiente_proposta()
    por_id = {c["id"]: c for c in ctx["casos"]}
    vistos: set[str] = set()

    def rejeita(codigo: str, bloco: dict, ctx_usado: dict | None = None) -> dict:
        r = evo.validar_proposta(bloco, ctx_usado or ctx)
        assert r["aceita"] is False, f"{codigo}: deveria ser rejeitada -> {r}"
        assert r["motivo"] == codigo, f"esperado {codigo}, veio {r['motivo']} ({r['detalhe']})"
        assert r["edicao"] is None, f"{codigo}: rejeição não pode devolver edição"
        assert r["detalhe"], f"{codigo}: rejeição sem detalhe"
        assert codigo in evo.CODIGOS_REJEICAO, f"{codigo} fora de CODIGOS_REJEICAO"
        vistos.add(codigo)
        return r

    rejeita("sem_bloco", None)
    rejeita("bloco_malformado", _bloco(malformado="sem FIM"))
    # O separador " — Motivo:" dentro do TEXTO partiria a linha da nota no lugar errado.
    separador = rejeita("bloco_malformado",
                        _bloco(TEXTO=_TEXTO_VALIDO + " — Motivo: motivo embutido"))
    assert separador["detalhe"] == "texto contém o separador da nota", separador
    rejeita("excesso_de_propostas", _bloco(numero=3))
    rejeita("excesso_de_propostas", _bloco(), {**ctx, "aceitas_no_caso": 2})
    rejeita("operacao_invalida", _bloco(OPERACAO="apagar"))
    rejeita("alvo_inexistente", _bloco(VERBETE="verbete-que-nao-existe"))
    rejeita("alvo_nao_visto", _bloco(VERBETE="tipo_divergente"))

    novo = {"OPERACAO": "novo_verbete", "VERBETE": "preco-ausente-no-botao",
            "TITULO": "Preco ausente no botao de detalhe", "CAUSAS": "campo_ausente"}
    # Maiúscula não passa: o id vira o nome do arquivo .md e bib.validar exige id igual ao
    # nome do arquivo, que é sempre minúsculo em base_conhecimento/.
    rejeita("id_invalido", _bloco(**{**novo, "VERBETE": "Novo_Verbete"}))
    rejeita("id_invalido", _bloco(**{**novo, "VERBETE": "id com espaco"}))
    rejeita("id_invalido", _bloco(**{**novo, "VERBETE": "verbete-" + "x" * 40}))
    # Sublinhado é aceito no formato do id -- por isso os ids de erros/ e os 23 nomes de
    # causa raiz (todos com sublinhado) chegam a id_repetido em vez de parar no formato.
    rejeita("id_repetido", _bloco(**{**novo, "VERBETE": "campo_ausente"}))
    rejeita("id_repetido", _bloco(**{**novo, "VERBETE": "tipo_divergente"}))
    rejeita("id_repetido", _bloco(**{**novo, "VERBETE": "contrato-produto"}))
    rejeita("teto_verbetes_novos", _bloco(**novo), {**ctx, "novos_nesta_epoca": 6})
    assert "pasta_invalida" in evo.CODIGOS_REJEICAO, evo.CODIGOS_REJEICAO
    rejeita("vocabulario", _bloco(**{**novo, "SISTEMA": "Mainframe"}))
    rejeita("vocabulario", _bloco(**{**novo, "ENTIDADE": "Fornecedor"}))
    rejeita("causa_fora_do_conjunto", _bloco(**{**novo, "CAUSAS": "bug_estranho"}))
    rejeita("causa_fora_do_conjunto", _bloco(**{**novo, "CAUSAS": None}))
    rejeita("causa_fora_do_conjunto", _bloco(**{**novo, "CAUSAS":
            "campo_ausente, campo_renomeado, nulo_inesperado, tipo_divergente"}))

    rejeita("arquivo_inexistente", _bloco(ARQUIVOS="Programacao/x.py"))
    rejeita("arquivo_inexistente",
            _bloco(TEXTO="O tratamento do campo ausente fica no arquivo inexistente.php, "
                         "que o verbete deveria citar para quem for corrigir"))
    rejeita("endpoint_inexistente",
            _bloco(TEXTO="A chamada GET /api/clientes devolve o objeto sem a chave de preco "
                         "e o botao de detalhe imprime undefined na tela"))
    rejeita("tabela_inexistente",
            _bloco(TEXTO="O campo de preco sai da tabela tbclientes e, quando ele nao vem, "
                         "o botao de detalhe imprime undefined na tela"))

    rejeita("texto_curto", _bloco(TEXTO="curto demais"))
    rejeita("texto_longo", _bloco(TEXTO="palavra repetida " * 20))
    rejeita("motivo_ausente", _bloco(MOTIVO=""))
    rejeita("motivo_curto", _bloco(MOTIVO="curto"))
    rejeita("motivo_longo", _bloco(MOTIVO="motivo repetido " * 20))

    rejeita("retificacao_sem_trecho", _bloco(OPERACAO="retificacao"))
    rejeita("retificacao_sem_trecho", _bloco(OPERACAO="retificacao", TRECHO="curto"))
    rejeita("trecho_nao_encontrado",
            _bloco(OPERACAO="retificacao",
                   TRECHO="esta frase nao aparece em nenhum lugar do verbete"))

    rejeita("palavra_chave_invalida", _bloco(PALAVRAS_CHAVE="bot[ao"))
    rejeita("palavra_chave_invalida", _bloco(PALAVRAS_CHAVE="a, b, c, d, e, f"))
    rejeita("palavra_chave_invalida", _bloco(SINTOMAS="a, b, c, d"))
    rejeita("palavra_chave_invalida", _bloco(PALAVRAS_CHAVE="x" * 41))

    # duplicada: a mesma nota proposta duas vezes no mesmo verbete.
    aceita = evo.validar_proposta(_bloco(), ctx)
    ctx_com_nota = {**ctx, "verbetes": evo.aplicar_em_memoria(ctx["verbetes"],
                                                             aceita["edicao"])}
    rejeita("duplicada", _bloco(), ctx_com_nota)

    lex1 = por_id["lex-1"]["entrada"]
    rejeita("copia_do_caso",
            _bloco(TEXTO=(lex1["sintoma"] + " " + str(lex1.get("observacao", ""))).strip()))
    rejeita("copia_do_caso",
            _bloco(TEXTO="O caso sin-4 mostra que, sem a chave de preco, o botao de "
                         "detalhe do produto imprime undefined na tela"))

    # teto_notas_verbete: 6 notas válidas já aplicadas, a 7ª estoura o teto de notas.
    verbetes_6 = ctx["verbetes"]
    for i in range(1, 7):
        edicao_i = evo.validar_proposta(_bloco(
            TEXTO=f"Detalhe {i} conferido no botao de detalhe do produto da tela inicial"),
            {**ctx, "verbetes": verbetes_6})["edicao"]
        assert edicao_i is not None, i
        verbetes_6 = evo.aplicar_em_memoria(verbetes_6, edicao_i)
    assert len(bib.notas([v for v in verbetes_6 if v["id"] == "campo_ausente"][0])) == 6
    rejeita("teto_notas_verbete", _bloco(
        TEXTO="Detalhe 7 conferido no botao de detalhe do produto da tela inicial"),
        {**ctx, "verbetes": verbetes_6})

    rejeita("teto_verbete_novo", _bloco(**{
        **novo, "VERBETE": "verbete-grande-demais",
        "TITULO": "Titulo comprido de proposito para estourar o teto do verbete " * 5,
        "TEXTO": ("Texto comprido de proposito para estourar o teto do verbete novo " * 5)[:280]}))

    original_teto = evo.TETO_TOKENS_CONTEXTO
    try:
        evo.TETO_TOKENS_CONTEXTO = 10
        rejeita("teto_prompt", _bloco())
    finally:
        evo.TETO_TOKENS_CONTEXTO = original_teto

    original_validar = bib.validar
    try:
        bib.validar = lambda *a, **k: [
            "erros/campo_ausente.md: 40% dos 5-gramas do caso lex-1 aparecem no verbete "
            "— reescrever"]
        rejeita("copia_do_caso_acumulada", _bloco())
        bib.validar = lambda *a, **k: ["erros/campo_ausente.md: sem seção '## Resumo'"]
        rejeita("biblioteca_invalida", _bloco())
        bib.validar = lambda *a, **k: ["negocio/entidade-produto.md: sem seção '## Resumo'"]
        rejeita("biblioteca_invalida", _bloco())
    finally:
        bib.validar = original_validar

    faltam = set(evo.CODIGOS_REJEICAO) - vistos - {"pasta_invalida"}
    assert not faltam, f"códigos de rejeição sem teste: {sorted(faltam)}"


# Trecho real do "## Resumo" de erros/campo_ausente.md. Tem de ter pelo menos 15
# caracteres (checagem retificacao_sem_trecho), então não dá para usar só "nem com nulo".
_TRECHO_REAL = "nem com nulo. No JavaScript"


def _aplicar(ctx: dict, bloco: dict) -> dict:
    """Valida a proposta, grava a edição em disco, recarrega ctx["verbetes"] e devolve a
    edição aceita. Confere de passagem, em TODA aplicação feita pelos testes, que
    aplicar_em_memoria (o que validar_proposta mede antes de aceitar) dá exatamente o
    mesmo verbete que bib.carregar lê depois da gravação — se as duas divergissem, a
    proposta seria medida contra um verbete e aplicada como outro."""
    r = evo.validar_proposta(bloco, ctx)
    assert r["aceita"] is True, f"proposta deveria ser aceita -> {r}"
    edicao = r["edicao"]
    em_memoria = [v for v in evo.aplicar_em_memoria(ctx["verbetes"], edicao)
                  if v["id"] == edicao["verbete"]][0]
    evo.aplicar_edicao(ctx["raiz"], edicao)
    ctx["verbetes"] = bib.carregar(ctx["raiz"])
    do_disco = [v for v in ctx["verbetes"] if v["id"] == edicao["verbete"]][0]
    for chave in ("pasta", "caminho", "meta", "secoes"):
        assert do_disco[chave] == em_memoria[chave], (
            f"{edicao['operacao']} em [{edicao['verbete']}]: '{chave}' em memória "
            f"{em_memoria[chave]!r} != em disco {do_disco[chave]!r}")
    return edicao


def teste_arquivos_citados_resolvidos() -> None:
    """Arquivo citado pelo nome simples, com ou sem número de linha.

    No segundo piloto da Fase 3 o modelo escreveu `ARQUIVOS: connect.php:16` -- nome sem
    caminho e com a linha junto, exatamente como a própria documentação cita arquivos em
    prosa ("fault_injection.py", "produtos.py _to_dict"). A proposta era recusada por
    arquivo_inexistente, embora o arquivo exista e só exista em um lugar. Agora o número de
    linha é descartado e o nome simples é resolvido para o caminho real do repositório, que
    é o que vai para o frontmatter -- senão bib.validar acusaria 'arquivo inexistente' na
    hora de fechar a época. Nome que casa com mais de um arquivo continua recusado: escolher
    um deles seria inventar a referência."""
    _tmp, ctx = _ambiente_proposta()
    resolvido = "Programacao/CobaiaFront/conn/connect.php"
    novo = {"OPERACAO": "novo_verbete", "TITULO": "Conexao do front com o banco",
            "CAUSAS": "campo_ausente"}

    r = evo.validar_proposta(_bloco(**novo, VERBETE="conexao-do-front",
                                    ARQUIVOS="connect.php:16"), ctx)
    assert r["aceita"] is True, r
    assert r["edicao"]["novo"]["arquivos"] == [resolvido], r["edicao"]["novo"]
    assert (bib.RAIZ_REPO / resolvido).exists(), resolvido

    # Caminho completo continua valendo como veio -- só o ":linha" sai.
    r2 = evo.validar_proposta(_bloco(**novo, VERBETE="conexao-do-front-2",
                                     ARQUIVOS=f"{resolvido}:16"), ctx)
    assert r2["aceita"] is True, r2
    assert r2["edicao"]["novo"]["arquivos"] == [resolvido], r2["edicao"]["novo"]

    # index.php existe três vezes em Programacao/ (CobaiaFront/, admin/, cliente/).
    r3 = evo.validar_proposta(_bloco(**novo, VERBETE="conexao-do-front-3",
                                     ARQUIVOS="index.php"), ctx)
    assert r3["motivo"] == "arquivo_inexistente", r3
    assert "ambíguo" in r3["detalhe"] and "3" in r3["detalhe"], r3["detalhe"]

    r4 = evo.validar_proposta(_bloco(**novo, VERBETE="conexao-do-front-4",
                                     ARQUIVOS="inexistente.php"), ctx)
    assert r4["motivo"] == "arquivo_inexistente", r4
    assert "não existe" in r4["detalhe"], r4["detalhe"]

    # Mesma regra para o nome de arquivo citado dentro do TEXTO.
    r5 = evo.validar_proposta(_bloco(
        TEXTO="A conexao do front com o banco fica em connect.php:16 e nao tem nada a ver "
              "com o botao que imprime undefined"), ctx)
    assert r5["aceita"] is True, r5
    r6 = evo.validar_proposta(_bloco(
        TEXTO="A tela inicial do front fica em index.php e nao tem nada a ver com o botao "
              "que imprime a palavra undefined"), ctx)
    assert r6["motivo"] == "arquivo_inexistente", r6
    assert "ambíguo" in r6["detalhe"], r6["detalhe"]

    # O caminho resolvido tem de sobreviver à gravação: bib.validar confere, verbete a
    # verbete, se cada item de 'arquivos' existe em disco.
    _aplicar(ctx, _bloco(**novo, VERBETE="conexao-do-front", ARQUIVOS="connect.php:16"))
    gravado = [v for v in ctx["verbetes"] if v["id"] == "conexao-do-front"][0]
    assert gravado["meta"]["arquivos"] == [resolvido], gravado["meta"]
    assert bib.validar(ctx["verbetes"], ctx["casos"], teto_global=None) == [], \
        bib.validar(ctx["verbetes"], ctx["casos"], teto_global=None)


def teste_aplicar_e_somente_acrescimo() -> None:
    """Aplica em disco as três operações (nota, retificação e verbete novo) na epoca-1 e
    confere: a biblioteca continua válida, a edição em memória dá o MESMO verbete que
    bib.carregar lê depois da gravação, e o invariante de somente-acréscimo não acusa
    nada. Depois, as quatro formas de quebrar o invariante (corpo alterado, item de lista
    apagado, arquivo sumido e arquivo novo fora de aprendidos/) têm de ser acusadas."""
    tmp, ctx = _ambiente_proposta()
    raiz, antiga = ctx["raiz"], tmp / "epoca-0"

    # _aplicar já confere, nas três operações, que aplicar_em_memoria e a gravação em disco
    # devolvem o mesmo verbete (mesmo meta, mesmas seções, mesmo caminho).
    _aplicar(ctx, _bloco(PALAVRAS_CHAVE="botao sem preco", SINTOMAS="botao sem preco"))
    _aplicar(ctx, _bloco(
        OPERACAO="retificacao", TRECHO=_TRECHO_REAL,
        TEXTO="A chave pode nao vir de jeito nenhum ou vir com nulo; sao duas causas "
              "diferentes e a mensagem na tela e a mesma",
        MOTIVO="o verbete nao separava a chave ausente da chave com nulo"))
    ctx["verbetes"] = bib.carregar(raiz)
    _aplicar(ctx, _bloco(OPERACAO="novo_verbete", VERBETE="preco-ausente-no-botao",
                         TITULO="Preco ausente no botao de detalhe",
                         CAUSAS="campo_ausente", SINTOMAS="botao com undefined"))

    verbetes = bib.carregar(raiz)
    assert evo.conferir_somente_acrescimo(antiga, raiz) == [], \
        evo.conferir_somente_acrescimo(antiga, raiz)
    assert bib.validar(verbetes, ctx["casos"], teto_global=None) == [], \
        bib.validar(verbetes, ctx["casos"], teto_global=None)

    alvo = [v for v in verbetes if v["id"] == "campo_ausente"][0]
    renderizado = bib.render(alvo)
    assert " Notas: " in renderizado, renderizado
    assert f'Retificação: onde diz "{_TRECHO_REAL}", leia:' in renderizado, renderizado
    assert len(bib.notas(alvo)) == 2, bib.notas(alvo)
    novo = [v for v in verbetes if v["id"] == "preco-ausente-no-botao"][0]
    assert novo["pasta"] == "aprendidos", novo
    assert novo["meta"]["tipo"] == "aprendido", novo["meta"]
    assert novo["meta"]["causas_relacionadas"] == ["campo_ausente"], novo["meta"]
    assert novo["secoes"]["Sinais"] == "- botao com undefined", novo["secoes"]

    def copia(nome: str) -> Path:
        return evo.copiar_biblioteca(raiz, tmp / nome)

    corpo_mexido = copia("corpo_mexido")
    arq = corpo_mexido / "erros" / "campo_ausente.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace(
        "## Resumo\nUma chave", "## Resumo\nAlguma chave"), encoding="utf-8")
    violacoes = evo.conferir_somente_acrescimo(antiga, corpo_mexido)
    assert any("erros/campo_ausente.md: corpo alterado" in v for v in violacoes), violacoes

    lista_podada = copia("lista_podada")
    arq = lista_podada / "erros" / "campo_ausente.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace(
        "ausente, falta, faltando,", "ausente, faltando,"), encoding="utf-8")
    violacoes = evo.conferir_somente_acrescimo(antiga, lista_podada)
    assert any("palavras_chave" in v for v in violacoes), violacoes

    sem_arquivo = copia("sem_arquivo")
    (sem_arquivo / "negocio" / "limites-do-sistema.md").unlink()
    violacoes = evo.conferir_somente_acrescimo(antiga, sem_arquivo)
    assert "negocio/limites-do-sistema.md: arquivo sumiu" in violacoes, violacoes

    fora_de_aprendidos = copia("fora_de_aprendidos")
    (fora_de_aprendidos / "erros" / "novo.md").write_text(
        _APRENDIDO.replace("id: nota-precos", "id: novo"), encoding="utf-8")
    violacoes = evo.conferir_somente_acrescimo(antiga, fora_de_aprendidos)
    assert "erros/novo.md: arquivo novo fora de aprendidos/" in violacoes, violacoes


def teste_frontmatter_preservado() -> None:
    """A edição é TEXTUAL e preserva o que já estava no arquivo: as tags de revisão
    originais do verbete continuam lá, a linha de rastreio da edição do modelo entra
    antes do '---' de fechamento e as listas do frontmatter crescem por sufixo (o que
    havia antes continua sendo prefixo do que existe depois)."""
    _tmp, ctx = _ambiente_proposta()
    arquivo = ctx["raiz"] / "erros" / "campo_ausente.md"
    antes = arquivo.read_text(encoding="utf-8")
    palavras_antes = [v for v in ctx["verbetes"]
                      if v["id"] == "campo_ausente"][0]["meta"]["palavras_chave"]

    _aplicar(ctx, _bloco(PALAVRAS_CHAVE="botao sem preco, undefined"))

    depois = arquivo.read_text(encoding="utf-8")
    assert "# ! Alteração de IA - Revisar: verbete de causa raiz" in depois, depois
    assert "# ! Motivo: descreve o que o JS faz" in depois, depois
    assert ("# ! Alteração por modelo teste (E1, caso sin-4) - Revisar: nota "
            "acrescentada.") in depois, depois
    assert depois.count("# ! Alteração de IA - Revisar") == antes.count(
        "# ! Alteração de IA - Revisar"), "a tag original foi duplicada ou apagada"

    palavras_depois = [v for v in bib.carregar(ctx["raiz"])
                       if v["id"] == "campo_ausente"][0]["meta"]["palavras_chave"]
    assert palavras_depois[:len(palavras_antes)] == palavras_antes, palavras_depois
    # "undefined" já estava na lista original: não pode entrar de novo.
    assert palavras_depois == palavras_antes + ["botao sem preco"], palavras_depois


def teste_notas_um_unico_cabecalho() -> None:
    """Duas notas no mesmo verbete geram UM cabeçalho '## Notas do modelo' só.
    bib._parse_secoes faz secoes[atual] = "" a cada cabeçalho '##': um segundo
    '## Notas do modelo' no mesmo arquivo apagaria do parse as notas do primeiro, e o
    verbete voltaria ao prompt sem elas."""
    _tmp, ctx = _ambiente_proposta()
    arquivo = ctx["raiz"] / "erros" / "campo_ausente.md"

    _aplicar(ctx, _bloco())
    ctx["verbetes"] = bib.carregar(ctx["raiz"])
    _aplicar(ctx, _bloco(
        TEXTO="Quando a chave de nome nao vem no objeto do produto, o cartao aparece "
              "com o rotulo sem nome na listagem",
        MOTIVO="o verbete citava o preco mas nao o nome no cartao da listagem"))

    texto = arquivo.read_text(encoding="utf-8")
    assert texto.count("## Notas do modelo") == 1, texto
    v = [x for x in bib.carregar(ctx["raiz"]) if x["id"] == "campo_ausente"][0]
    assert len(bib.notas(v)) == 2, bib.notas(v)


def _nota_numerada(i: int) -> dict:
    """Proposta de nota válida e distinta das outras (o texto começa com o número), com
    ~130 caracteres — é o tamanho que faz 6 notas chegarem perto dos 800 caracteres
    renderizados por verbete."""
    return _bloco(
        TEXTO=f"Caso {i}: quando a chave de preco nao chega no objeto do produto, o botao "
              f"de detalhe da tela inicial imprime a palavra undefined",
        MOTIVO=f"o verbete nao dizia o que o botao mostra sem o preco (detalhe {i})")


def teste_abrir_epoca_reconstroi() -> None:
    """O JSONL da execução é a fonte da verdade e a pasta da época é derivada dele:
    abrir_epoca reconstrói epoca-n do zero reaplicando, em ordem, as edições aceitas, e
    confere o hash ao fim de cada caso. Hash divergente para a execução (seguir com uma
    biblioteca diferente da que o modelo viu invalidaria todos os diagnósticos da época);
    época já fechada não é tocada."""
    tmp, ctx = _ambiente_proposta()
    raiz = ctx["raiz"]

    registros = []
    for bloco, caso in ((_bloco(), "sin-4"),
                        (_bloco(OPERACAO="novo_verbete", VERBETE="preco-ausente-no-botao",
                                TITULO="Preco ausente no botao de detalhe",
                                CAUSAS="campo_ausente"), "sin-6")):
        ctx_caso = {**ctx, "caso_id": caso, "verbetes": bib.carregar(raiz)}
        edicao = _aplicar(ctx_caso, bloco)
        registros.append({"caso": caso,
                          "decisoes": [{"aceita": False, "edicao": None},
                                       {"aceita": True, "edicao": edicao}],
                          "hash_biblioteca_apos": evo.hash_biblioteca(raiz)})
    hash_final = evo.hash_biblioteca(raiz)
    assert registros[-1]["hash_biblioteca_apos"] == hash_final

    # historico.jsonl com uma linha de OUTRA época (que não pode ser tocada) e uma linha
    # órfã da época 1 -- o que uma queda entre registrar_historico e a gravação do JSONL
    # deixa para trás. A reconstrução tem de refazer o histórico da época 1 a partir dos
    # registros, sem duplicar a órfã: o JSONL é a fonte da verdade, o histórico é derivado.
    historico = tmp / "historico.jsonl"
    historico.write_text(
        json.dumps({"epoca": 0, "caso": "lex-1", "verbete": "corpo_vazio",
                    "texto": "linha de outra época", "ordem": 1}, ensure_ascii=False)
        + "\n"
        + json.dumps({"epoca": 1, "caso": "sin-4", "verbete": "campo_ausente",
                      "texto": "linha órfã de uma queda", "ordem": 9}, ensure_ascii=False)
        + "\n", encoding="utf-8")

    shutil.rmtree(raiz)
    devolvida = evo.abrir_epoca(tmp, 1, registros)
    assert devolvida == raiz, devolvida
    assert evo.hash_biblioteca(raiz) == hash_final, "reconstrução deu outra biblioteca"

    linhas = [json.loads(l) for l in historico.read_text(encoding="utf-8").splitlines()]
    assert len(linhas) == 3, linhas
    assert linhas[0] == {"epoca": 0, "caso": "lex-1", "verbete": "corpo_vazio",
                         "texto": "linha de outra época", "ordem": 1}, linhas[0]
    da_epoca_1 = [l for l in linhas if l["epoca"] == 1]
    assert len(da_epoca_1) == 2, da_epoca_1
    assert not any("órfã" in l["texto"] for l in da_epoca_1), da_epoca_1
    esperadas = [r["decisoes"][1]["edicao"] for r in registros]
    assert [l["verbete"] for l in da_epoca_1] == [e["verbete"] for e in esperadas], da_epoca_1
    assert [l["texto"] for l in da_epoca_1] == [e["texto"] for e in esperadas], da_epoca_1
    assert [l["ordem"] for l in da_epoca_1] == [1, 2], da_epoca_1
    assert [l["hash_apos"] for l in da_epoca_1] == [
        r["hash_biblioteca_apos"] for r in registros], da_epoca_1

    errados = [{**registros[0], "hash_biblioteca_apos": "000000000000"}]
    try:
        evo.abrir_epoca(tmp, 1, errados)
        assert False, "hash divergente deveria levantar SystemExit"
    except SystemExit as e:
        assert "sin-4" in str(e) and "000000000000" in str(e), str(e)

    # Registro SEM hash é o estado que a corrida deixa quando cai entre aplicar a edição e
    # gravar a linha do JSONL. Reconstruir em silêncio a partir daí levantaria uma época que
    # ninguém conferiu contra o que o modelo viu -- tem de parar, dizendo qual caso.
    sem_chave = {k: v for k, v in registros[0].items() if k != "hash_biblioteca_apos"}
    for rotulo, registro in (("chave ausente", sem_chave),
                             ("string vazia", {**registros[0],
                                               "hash_biblioteca_apos": ""}),
                             ("None", {**registros[0],
                                       "hash_biblioteca_apos": None})):
        try:
            evo.abrir_epoca(tmp, 1, [registro])
            assert False, f"registro com {rotulo} deveria levantar SystemExit"
        except SystemExit as e:
            assert "sin-4" in str(e), f"{rotulo}: {e}"
            assert "hash_biblioteca_apos" in str(e), f"{rotulo}: {e}"

    # Reconstruir de novo não pode duplicar o histórico da época: as linhas da época 1 são
    # apagadas e regravadas a cada reconstrução.
    evo.abrir_epoca(tmp, 1, registros)
    linhas = [json.loads(l) for l in historico.read_text(encoding="utf-8").splitlines()]
    assert len(linhas) == 3, linhas
    assert sum(1 for l in linhas if l["epoca"] == 1) == 2, linhas

    # Época já fechada: abrir_epoca devolve a pasta sem reconstruir nada.
    (raiz / "fechamento.json").write_text("{}", encoding="utf-8")
    arquivo = raiz / "erros" / "campo_ausente.md"
    mtime = arquivo.stat().st_mtime_ns
    evo.abrir_epoca(tmp, 1, [])
    assert arquivo.stat().st_mtime_ns == mtime, "época fechada foi reconstruída"


def teste_registrar_historico() -> None:
    """historico.jsonl guarda uma linha por edição aplicada (a edição inteira mais os
    extras do executor), em append com flush — se a corrida parar no meio, as linhas já
    gravadas continuam legíveis."""
    tmp, ctx = _ambiente_proposta()
    edicao = evo.validar_proposta(_bloco(), ctx)["edicao"]
    evo.registrar_historico(tmp, edicao, {"ordem": 1, "acertou_diagnostico": True,
                                          "hash_apos": "abc123"})
    evo.registrar_historico(tmp, edicao, {"ordem": 2, "acertou_diagnostico": False,
                                          "hash_apos": "def456"})

    linhas = (tmp / "historico.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 2, linhas
    primeira = json.loads(linhas[0])
    assert primeira["verbete"] == "campo_ausente", primeira
    assert primeira["arquivo"] == "erros/campo_ausente.md", primeira
    assert primeira["ordem"] == 1 and primeira["hash_apos"] == "abc123", primeira
    assert json.loads(linhas[1])["acertou_diagnostico"] is False, linhas[1]


def teste_orcamento_prompt() -> None:
    """Com o verbete quase no teto de 800 caracteres de notas, mais uma nota curta ainda
    entra se couber — o teto é do verbete, não da proposta. E, com o teto de tokens do
    contexto baixado para 10, a mesma proposta é recusada por teto_prompt: o orçamento do
    prompt de diagnóstico é checado antes de a nota entrar, não depois de o num_ctx
    estourar no meio da bateria."""
    _tmp, ctx = _ambiente_proposta()
    for i in range(1, 6):
        _aplicar(ctx, _nota_numerada(i))
        ctx["verbetes"] = bib.carregar(ctx["raiz"])

    alvo = [v for v in ctx["verbetes"] if v["id"] == "campo_ausente"][0]
    renderizado = len(bib.render_notas(alvo))
    assert 600 < renderizado <= bib.TETO_CHARS_NOTAS_VERBETE, renderizado
    assert bib.validar(ctx["verbetes"], ctx["casos"], teto_global=None) == [], \
        bib.validar(ctx["verbetes"], ctx["casos"], teto_global=None)

    curta = _bloco(TEXTO="A sexta nota cabe porque o verbete ainda tem folga no teto de "
                         "caracteres de notas")
    r = evo.validar_proposta(curta, ctx)
    assert r["aceita"] is True, r
    depois = evo.aplicar_em_memoria(ctx["verbetes"], r["edicao"])
    alvo_depois = [v for v in depois if v["id"] == "campo_ausente"][0]
    assert len(bib.render_notas(alvo_depois)) <= bib.TETO_CHARS_NOTAS_VERBETE
    assert len(bib.notas(alvo_depois)) == bib.TETO_NOTAS_POR_VERBETE

    original = evo.TETO_TOKENS_CONTEXTO
    try:
        evo.TETO_TOKENS_CONTEXTO = 10
        r2 = evo.validar_proposta(curta, ctx)
        assert r2["motivo"] == "teto_prompt", r2
    finally:
        evo.TETO_TOKENS_CONTEXTO = original


def teste_fechar_epoca() -> None:
    """O fechamento da época grava, sem nenhum número digitado à mão, o índice da cópia, o
    diff contra a época anterior, o diff contra a biblioteca original e o fechamento.json
    com o hash e as contagens. Biblioteca inválida ou invariante quebrado param o
    fechamento com SystemExit — é bug do harness, não do modelo."""
    tmp, ctx = _ambiente_proposta()
    raiz = ctx["raiz"]
    _aplicar(ctx, _bloco())
    ctx["verbetes"] = bib.carregar(raiz)
    _aplicar(ctx, _bloco(OPERACAO="retificacao", TRECHO=_TRECHO_REAL,
                         TEXTO="A chave pode nao vir de jeito nenhum ou vir com nulo; sao "
                               "duas causas diferentes e a tela mostra a mesma coisa",
                         MOTIVO="o verbete nao separava a chave ausente da chave com nulo"))
    ctx["verbetes"] = bib.carregar(raiz)
    _aplicar(ctx, _bloco(OPERACAO="novo_verbete", VERBETE="preco-ausente-no-botao",
                         TITULO="Preco ausente no botao de detalhe",
                         CAUSAS="campo_ausente"))

    fechamento = evo.fechar_epoca(tmp, 1, "teste", ctx["casos"], 3)

    assert (raiz / "INDICE.md").exists(), "INDICE.md da cópia não foi gravado"
    # Os diffs são GERADOS e ficam FORA do snapshot, como irmãos de epoca-1/: dentro dele
    # bib.carregar leria cada diff__*.md como se fosse um verbete de frontmatter ilegível.
    for nome in ("diff__E1.json", "diff__E1.md", "diff__E1__vs_original.json",
                 "diff__E1__vs_original.md"):
        assert (tmp / nome).exists(), f"{nome} deveria estar ao lado de epoca-1/"
        assert not (raiz / nome).exists(), f"{nome} não pode estar DENTRO de epoca-1/"
    assert (raiz / "fechamento.json").exists()
    assert sorted(p.name for p in raiz.iterdir() if p.is_file()) == [
        "INDICE.md", "fechamento.json"], sorted(p.name for p in raiz.iterdir())
    assert bib.validar(bib.carregar(raiz), ctx["casos"], teto_global=None) == [], \
        bib.validar(bib.carregar(raiz), ctx["casos"], teto_global=None)
    gravado = json.loads((raiz / "fechamento.json").read_text(encoding="utf-8"))
    assert gravado == fechamento, (gravado, fechamento)
    assert fechamento["aceitas_na_epoca"] == 3, fechamento
    assert fechamento["epoca"] == 1 and fechamento["modelo"] == "teste", fechamento
    assert fechamento["n_verbetes"] == 36 + 1, fechamento
    assert fechamento["n_verbetes"] == len(bib.carregar(bib.BASE)) + 1, fechamento
    assert fechamento["n_notas"] == 1 and fechamento["n_retificacoes"] == 1, fechamento
    assert fechamento["hash"] == evo.hash_biblioteca(raiz), fechamento
    diff = json.loads((tmp / "diff__E1.json").read_text(encoding="utf-8"))
    assert diff["arquivos_novos"] == ["aprendidos/preco-ausente-no-botao.md"], diff
    assert diff["por_verbete"]["campo_ausente"]["notas"] == 1, diff["por_verbete"]

    # Fechar de novo (a corrida caiu entre o fim da época e a gravação) não pode contar os
    # diff__E1.md da tentativa anterior como verbetes: os números têm de sair iguais.
    refeito = evo.fechar_epoca(tmp, 1, "teste", ctx["casos"], 3)
    assert {k: v for k, v in refeito.items() if k != "fechado_em"} == {
        k: v for k, v in fechamento.items() if k != "fechado_em"}, (refeito, fechamento)

    quebrada = evo.copiar_biblioteca(raiz, tmp / "epoca-2")
    (quebrada / "fechamento.json").unlink()
    (quebrada / "negocio" / "limites-do-sistema.md").unlink()
    try:
        evo.fechar_epoca(tmp, 2, "teste", ctx["casos"], 0)
        assert False, "invariante quebrado deveria levantar SystemExit"
    except SystemExit as e:
        assert "limites-do-sistema.md" in str(e), str(e)


def teste_prompt_proposta() -> None:
    """proposta_de_edicao é a CONTINUAÇÃO LITERAL do prompt de diagnóstico (p) com a
    resposta do modelo (r) -- só um prefixo idêntico entre as duas chamadas reaproveita o
    cache de prefixo do Ollama (achado 4.21 do Memorial). Confere o bloco de correção
    montado a partir do gabarito de CASOS[0] (lex-1: causa_raiz 'resposta_truncada',
    campo_afetado None) e as duas substituições (sem CAUSA_RAIZ respondida; diagnóstico
    correto)."""
    caso = CASOS[0]
    p = estrategias.linear_com_biblioteca(caso, "DOC")
    r = "CAUSA_RAIZ: corpo_vazio\nCAMPO: nenhum\nIMPACTO: x\nFONTE: [a]"
    s = estrategias.proposta_de_edicao(
        p, r, caso, False, "corpo_vazio",
        "[resposta_truncada] Resposta truncada\nResumo.",
        ["entidade-produto", "resposta_truncada"])

    assert s.startswith(p + "\n\n" + r + "\n\n====="), s[:400]
    assert "CAUSA_RAIZ CORRETA: " + caso["gabarito"]["causa_raiz"] in s, s
    assert "CAMPO AFETADO: nenhum" in s, s
    assert "SEU DIAGNÓSTICO: corpo_vazio — incorreto" in s, s
    assert "[entidade-produto], [resposta_truncada]" in s, s
    assert "  - corpo_nao_e_json" in s, s
    assert "[resposta_truncada] Resposta truncada" in s, s

    s_acerto = estrategias.proposta_de_edicao(
        p, r, caso, True, None,
        "[resposta_truncada] Resposta truncada\nResumo.",
        ["entidade-produto", "resposta_truncada"])
    assert "SEU DIAGNÓSTICO: (sem CAUSA_RAIZ) — correto" in s_acerto, s_acerto


# ! Alteração de IA - Revisar: fixtures dos testes do executor da Fase 3 (Tarefa 7) — a
# ordem esperada das chaves dos dois registros, os 6 primeiros casos do banco, um dicionário
# no formato de oll.gerar e o conjunto de stubs que substitui o cliente do Ollama.
# ! Motivo: uma época real do executor são 90 diagnósticos mais 54 propostas por modelo, de
# horas em CPU — sem stub não haveria teste nenhum do fluxo de época, retomada e fechamento.
# A ordem das chaves é comparada com list(registro.keys()) porque a análise da Fase 3 lê os
# JSONL com as mesmas colunas dos da Fase 2-B (executar_bateria.py:205-226): se um campo novo
# entrasse no meio, o arquivo continuaria válido como JSON e a comparação entre as fases
# passaria a ler coluna trocada sem nenhum erro aparecer.
_CHAVES_DIAGNOSTICO = [
    "modelo", "digest", "versao_ollama", "maquina", "caso", "classe", "nivel", "estrategia",
    "condicao",
    "fase", "tipo", "epoca", "biblioteca_epoca", "biblioteca_versao", "particao", "k",
    "contexto_sha256", "notas_no_contexto", "verbetes_novos_no_contexto",
    "contexto_estourou", "verbetes_ids", "verbete_ouro", "causa_plantada",
    "chars_contexto", "gabarito", "teto_tokens",
    "segundos", "tokens_entrada", "tokens_saida", "carga_ms", "prefill_ms", "geracao_ms",
    "total_ms", "resposta",
    "somente_cpu", "modelos_residentes", "memoria_mb",
]

_CHAVES_PROPOSTA = [
    "modelo", "digest", "versao_ollama", "maquina", "fase", "tipo", "epoca", "biblioteca_epoca",
    "biblioteca_versao", "caso", "classe", "nivel", "particao", "k", "verbetes_ids",
    "verbete_ouro", "ouro_no_contexto", "ids_visiveis", "causa_correta_mostrada",
    "campo_mostrado", "causa_respondida", "acertou_diagnostico", "prompt", "teto_tokens",
    "segundos", "tokens_entrada", "tokens_saida", "carga_ms", "prefill_ms", "geracao_ms",
    "total_ms", "resposta",
    "contexto_estourou", "resposta_truncada", "nenhuma", "propostas_parseadas", "decisoes",
    "n_propostas", "n_aceitas", "motivos_rejeicao",
    "somente_cpu", "modelos_residentes", "memoria_mb", "hash_biblioteca_apos",
]

_MODELO_DE_MENTIRA = "modelo:teste"
_SLUG_DE_MENTIRA = "modelo_teste"

_PROPOSTA_DE_MENTIRA = """Vou acrescentar uma observacao ao verbete.

PROPOSTA 1
OPERACAO: nota
VERBETE: [{verbete}]
TEXTO: {texto}
MOTIVO: {motivo}
FIM"""


def _casos_do_piloto(n: int = 6) -> list[dict]:
    """Os n primeiros casos do banco, que é o que `--casos n` seleciona. O stub descobre de
    qual caso é o prompt procurando o SINTOMA OBSERVADO nele, então sintoma repetido entre
    dois casos deixaria o stub responder o gabarito do caso errado sem falhar."""
    casos = (CASOS + CASOS_EXTRA)[:n]
    sintomas = [c["entrada"]["sintoma"] for c in casos]
    assert len(set(sintomas)) == len(sintomas), "sintoma repetido entre os casos do teste"
    return casos


def _c3_temporario(nome: str = "fase3_teste") -> dict:
    """caminhos.fase3() calculado sobre uma raiz temporária — rodar_modelo_fase3 recebe o
    dicionário de caminhos pronto, então nenhum teste escreve em resultados/ nem em
    resultados_alvo/ (os arquivos da Fase 2-B lá não podem mudar)."""
    tmp = _pasta_temporaria()
    anterior = caminhos.RESULTADOS
    caminhos.RESULTADOS = tmp
    try:
        return caminhos.fase3(nome)
    finally:
        caminhos.RESULTADOS = anterior


def _resposta_de_mentira(resposta: str, tokens_entrada: int = 1500) -> dict:
    """Os 8 campos que oll.gerar devolve. tokens_entrada realista (1.500 no diagnóstico,
    2.400 na proposta) porque o executor passa esse número por guarda_tokens_reais antes de
    gravar: um valor perto de num_ctx (8192) abortaria a época no primeiro caso."""
    return {"segundos": 0.5, "tokens_entrada": tokens_entrada, "tokens_saida": 60,
            "carga_ms": 0, "prefill_ms": 300, "geracao_ms": 200, "total_ms": 500,
            "resposta": resposta}


_ERRO_DE_MENTIRA = "Connection refused (de mentira)"


def _ollama_de_mentira(casos: list[dict], propostas_por_caso: dict, chamadas: list,
                       parar_em: int | None = None, falhas_iniciais: int = 0,
                       falhar_sempre: bool = False) -> dict:
    """Stubs de cliente_ollama: gerar devolve o gabarito do caso no diagnóstico e, na
    proposta (prompt que contém o bloco de correção), o texto combinado para aquele caso ou
    NENHUMA. `parar_em` levanta KeyboardInterrupt na n-ésima inferência, para o teste de
    retomada; `falhas_iniciais`/`falhar_sempre` devolvem o dicionário de erro de
    executar_bateria.inferir_seguro (falha de rede/timeout), para o teste da repetição;
    `chamadas` acumula os prompts, que é como o teste conta as inferências."""
    verbetes = bib.carregar()
    ouro_por_caso = {c["id"]: recuperacao.verbete_ouro(verbetes, c)["id"] for c in casos}
    por_sintoma = {c["entrada"]["sintoma"]: c for c in casos}

    def gerar(modelo: str, prompt: str, max_tokens: int = 400) -> dict:
        chamadas.append(prompt)
        if parar_em is not None and len(chamadas) == parar_em:
            raise KeyboardInterrupt(f"interrupcao simulada na {parar_em}a inferencia")
        if falhar_sempre or len(chamadas) <= falhas_iniciais:
            # Levanta como o urllib levantaria com o Ollama fora do ar: é
            # executar_bateria.inferir_seguro que transforma isso no dicionário com 'erro',
            # e é esse caminho inteiro que o teste precisa exercitar.
            raise ConnectionError(_ERRO_DE_MENTIRA)
        caso = next(c for sintoma, c in por_sintoma.items() if sintoma in prompt)
        if "CORREÇÃO DESTE CASO" in prompt:
            return _resposta_de_mentira(
                propostas_por_caso.get(caso["id"], "NENHUMA"), tokens_entrada=2400)
        return _resposta_de_mentira(
            f"CAUSA_RAIZ: {caso['gabarito']['causa_raiz']}\nCAMPO: nenhum\n"
            f"IMPACTO: a tela nao mostra o dado esperado.\n"
            f"FONTE: [{ouro_por_caso[caso['id']]}]")

    return {
        "gerar": gerar,
        "instalados": lambda: {_MODELO_DE_MENTIRA: "deadbeef0000"},
        "residentes": lambda: [{"nome": _MODELO_DE_MENTIRA, "memoria_mb": 1900,
                                "vram_mb": 0}],
        "descarregar": lambda modelo: None,
        "um_modelo_por_vez": lambda: (True, [_MODELO_DE_MENTIRA]),
        "_get": lambda caminho, timeout=30: {"version": "0.0.0-teste"},
    }


def _com_stubs(stubs: dict, funcao):
    """Troca as funções de cliente_ollama pelos stubs (executar_fase3.oll É o módulo
    cliente_ollama, então a troca vale para todo mundo que o importou) e devolve tudo ao
    lugar no finally — sem isso, o teste seguinte herdaria o Ollama de mentira."""
    anteriores = {nome: getattr(executar_fase3.oll, nome) for nome in stubs}
    pausa = executar_fase3.PAUSA_DESCARGA
    # ! As pausas de repetição (30/60 s) são zeradas junto: o teste da inferência que falha
    # espera o executor repetir três vezes, e com as pausas reais a suíte levaria 1,5 minuto
    # só nesse teste.
    pausas_tentativa = executar_fase3.PAUSAS_ENTRE_TENTATIVAS
    executar_fase3.PAUSA_DESCARGA = 0
    executar_fase3.PAUSAS_ENTRE_TENTATIVAS = (0, 0, 0)
    for nome, valor in stubs.items():
        setattr(executar_fase3.oll, nome, valor)
    try:
        return funcao()
    finally:
        for nome, valor in anteriores.items():
            setattr(executar_fase3.oll, nome, valor)
        executar_fase3.PAUSA_DESCARGA = pausa
        executar_fase3.PAUSAS_ENTRE_TENTATIVAS = pausas_tentativa


def _rodar(c3: dict, casos: list[dict], particao: dict, propostas: dict,
           parar_em: int | None = None, k: int = 3, **stub) -> list:
    chamadas: list = []
    stubs = _ollama_de_mentira(casos, propostas, chamadas, parar_em, **stub)
    _com_stubs(stubs, lambda: executar_fase3.rodar_modelo_fase3(
        _MODELO_DE_MENTIRA, casos, particao, 1, k, 600, 700, c3))
    return chamadas


def _proposta_para(caso: dict) -> str:
    """Uma nota no verbete de ouro do caso — é o único id garantidamente visível no
    diagnóstico (ids_visiveis = recuperados ∪ {ouro}), então uma nota nele não é recusada
    por alvo_nao_visto."""
    ouro = recuperacao.verbete_ouro(bib.carregar(), caso)["id"]
    return _PROPOSTA_DE_MENTIRA.format(verbete=ouro, texto=_TEXTO_VALIDO,
                                       motivo=_MOTIVO_VALIDO)


def teste_executor_epoca_completa() -> None:
    """Uma época inteira com 6 casos e Ollama de mentira: diagnóstico dos 6 com a época 0,
    proposta só nos casos de aprendizado, aplicação da única proposta válida, fechamento da
    época 1 e passada final de diagnóstico com a biblioteca já editada. Confere os arquivos
    gerados, a ordem das chaves dos dois registros e que o hash gravado no último registro
    de proposta é o mesmo que fechou a época (é o que abrir_epoca compara ao retomar)."""
    casos = _casos_do_piloto(6)
    particao = evo.particionar(CASOS + CASOS_EXTRA)
    aprendizado = [c for c in casos if evo.particao_de(particao, c["id"]) == "aprendizado"]
    assert aprendizado, "os 6 primeiros casos precisam ter ao menos um de aprendizado"
    primeiro = aprendizado[0]
    ouro_primeiro = recuperacao.verbete_ouro(bib.carregar(), primeiro)["id"]

    c3 = _c3_temporario()
    chamadas = _rodar(c3, casos, particao, {primeiro["id"]: _proposta_para(primeiro)})
    # 6 diagnósticos com L0 + 1 proposta por caso de aprendizado + 6 diagnósticos com L1.
    assert len(chamadas) == 6 + len(aprendizado) + 6, len(chamadas)

    pasta = c3["raiz"] / _SLUG_DE_MENTIRA
    pasta_bib = c3["bibliotecas"] / _SLUG_DE_MENTIRA
    diag0 = executar_bateria.ler_jsonl(pasta / "diagnosticos__L0.jsonl")
    diag1 = executar_bateria.ler_jsonl(pasta / "diagnosticos__L1.jsonl")
    propostas = executar_bateria.ler_jsonl(pasta / "propostas__E1.jsonl")
    assert len(diag0) == 6, len(diag0)
    assert len(diag1) == 6, len(diag1)
    assert len(propostas) == len(aprendizado), (len(propostas), len(aprendizado))

    assert evo.snapshot_fechado(pasta_bib / "epoca-0"), "epoca-0 não fechou"
    assert evo.snapshot_fechado(pasta_bib / "epoca-1"), "epoca-1 não fechou"
    fech0 = json.loads((pasta_bib / "epoca-0" / "fechamento.json").read_text(
        encoding="utf-8"))
    fech1 = json.loads((pasta_bib / "epoca-1" / "fechamento.json").read_text(
        encoding="utf-8"))
    assert fech0["hash"] == evo.hash_biblioteca(bib.BASE), "epoca-0 não é a original"
    assert fech1["aceitas_na_epoca"] == 1, fech1

    historico = executar_bateria.ler_jsonl(pasta_bib / "historico.jsonl")
    assert len(historico) == 1, historico
    assert historico[0]["verbete"] == ouro_primeiro, historico[0]
    assert historico[0]["caso"] == primeiro["id"], historico[0]

    editado = [v for v in bib.carregar(pasta_bib / "epoca-1") if v["id"] == ouro_primeiro][0]
    notas = bib.notas(editado)
    assert len(notas) == 1, notas
    assert notas[0]["texto"] == _TEXTO_VALIDO, notas[0]
    intacto = [v for v in bib.carregar(pasta_bib / "epoca-0") if v["id"] == ouro_primeiro][0]
    assert bib.notas(intacto) == [], "epoca-0 foi editada"

    assert list(diag0[0].keys()) == _CHAVES_DIAGNOSTICO, list(diag0[0].keys())
    assert list(propostas[0].keys()) == _CHAVES_PROPOSTA, list(propostas[0].keys())

    r = diag0[0]
    assert r["fase"] == "3" and r["tipo"] == "diagnostico", r
    assert r["epoca"] == 1 and r["biblioteca_epoca"] == 0, r
    assert r["biblioteca_versao"] == fech0["hash"], r
    assert r["estrategia"] == "linear" and r["condicao"] == "A2", r
    assert r["particao"] == evo.particao_de(particao, r["caso"]), r
    assert r["k"] == 3 and r["teto_tokens"] == 600, r
    assert len(r["contexto_sha256"]) == 12, r
    assert r["notas_no_contexto"] == 0 and r["verbetes_novos_no_contexto"] == [], r
    assert r["contexto_estourou"] is False, r
    assert diag1[0]["epoca"] == 2 and diag1[0]["biblioteca_epoca"] == 1, diag1[0]
    assert diag1[0]["biblioteca_versao"] == fech1["hash"], diag1[0]

    aceita = [p for p in propostas if p["caso"] == primeiro["id"]][0]
    assert aceita["n_propostas"] == 1 and aceita["n_aceitas"] == 1, aceita
    assert aceita["nenhuma"] is False and aceita["motivos_rejeicao"] == [], aceita
    assert aceita["decisoes"][0]["aceita"] is True, aceita["decisoes"]
    assert aceita["decisoes"][0]["edicao"]["verbete"] == ouro_primeiro, aceita["decisoes"]
    assert aceita["acertou_diagnostico"] is True, aceita
    assert aceita["teto_tokens"] == 700, aceita
    assert ouro_primeiro in aceita["ids_visiveis"], aceita
    assert aceita["ids_visiveis"] == sorted(aceita["ids_visiveis"]), aceita
    nenhumas = [p for p in propostas if p["caso"] != primeiro["id"]]
    assert all(p["nenhuma"] is True and p["n_aceitas"] == 0 for p in nenhumas), nenhumas
    assert propostas[-1]["hash_biblioteca_apos"] == fech1["hash"], propostas[-1]


def teste_executor_retomada() -> None:
    """A mesma época, interrompida na 4ª inferência e relançada: o executor retoma pela
    chave (modelo, época, caso, tipo) lida dos JSONL, nenhum caso é gravado duas vezes e a
    época 1 é reconstruída do JSONL com o hash idêntico ao da execução sem interrupção.
    A segunda interrupção é dentro da PROPOSTA de um caso cujo diagnóstico já ficou
    gravado — a proposta órfã —, que é o estado em que a retomada tem de reaproveitar a
    resposta do JSONL em vez de diagnosticar o caso de novo."""
    casos = _casos_do_piloto(6)
    particao = evo.particionar(CASOS + CASOS_EXTRA)
    primeiro = [c for c in casos
                if evo.particao_de(particao, c["id"]) == "aprendizado"][0]
    propostas = {primeiro["id"]: _proposta_para(primeiro)}

    inteiro = _c3_temporario("fase3_inteiro")
    _rodar(inteiro, casos, particao, propostas)
    hash_referencia = json.loads(
        (inteiro["bibliotecas"] / _SLUG_DE_MENTIRA / "epoca-1" / "fechamento.json")
        .read_text(encoding="utf-8"))["hash"]

    partido = _c3_temporario("fase3_partido")
    try:
        _rodar(partido, casos, particao, propostas, parar_em=4)
        assert False, "o stub deveria ter interrompido a execução na 4ª inferência"
    except KeyboardInterrupt:
        pass
    pasta = partido["raiz"] / _SLUG_DE_MENTIRA
    parciais = executar_bateria.ler_jsonl(pasta / "diagnosticos__L0.jsonl")
    assert 0 < len(parciais) < 6, len(parciais)

    # Segunda interrupção, agora na 2ª inferência da retomada: o caso que estava pendente
    # tem o diagnóstico gravado e a proposta não — a proposta órfã.
    try:
        _rodar(partido, casos, particao, propostas, parar_em=2)
        assert False, "o stub deveria ter interrompido a retomada na 2ª inferência"
    except KeyboardInterrupt:
        pass
    com_diagnostico = [r["caso"] for r in
                       executar_bateria.ler_jsonl(pasta / "diagnosticos__L0.jsonl")]
    com_proposta = [r["caso"] for r in
                    executar_bateria.ler_jsonl(pasta / "propostas__E1.jsonl")]
    orfaos = [c["id"] for c in casos
              if evo.particao_de(particao, c["id"]) == "aprendizado"
              and c["id"] in com_diagnostico and c["id"] not in com_proposta]
    assert orfaos, (com_diagnostico, com_proposta)
    diagnosticos_antes = len(com_diagnostico)

    _rodar(partido, casos, particao, propostas)

    # O caso órfão não foi diagnosticado de novo: os 6 diagnósticos finais contêm os que já
    # estavam gravados, sem uma segunda linha para o órfão.
    depois_orfao = executar_bateria.ler_jsonl(pasta / "diagnosticos__L0.jsonl")
    assert len([r for r in depois_orfao if r["caso"] == orfaos[0]]) == 1, orfaos
    assert len(depois_orfao) >= diagnosticos_antes, (len(depois_orfao), diagnosticos_antes)

    for nome, esperado in (("diagnosticos__L0.jsonl", 6), ("diagnosticos__L1.jsonl", 6)):
        registros = executar_bateria.ler_jsonl(pasta / nome)
        ids = [r["caso"] for r in registros]
        assert len(ids) == esperado, (nome, ids)
        assert len(set(ids)) == len(ids), f"{nome} tem caso repetido: {ids}"
    ids_prop = [r["caso"] for r in
                executar_bateria.ler_jsonl(pasta / "propostas__E1.jsonl")]
    assert len(set(ids_prop)) == len(ids_prop), ids_prop

    # Nada regravado: as linhas que já estavam no JSONL antes da retomada continuam
    # idênticas (a retomada não refaz o que já foi medido).
    depois = executar_bateria.ler_jsonl(pasta / "diagnosticos__L0.jsonl")
    assert depois[:len(parciais)] == parciais, "a retomada regravou registros antigos"

    fechamento = json.loads(
        (partido["bibliotecas"] / _SLUG_DE_MENTIRA / "epoca-1" / "fechamento.json")
        .read_text(encoding="utf-8"))
    assert fechamento["hash"] == hash_referencia, (fechamento["hash"], hash_referencia)


def teste_projecao_tempo() -> None:
    """A projeção usa os ms/token de prefill e os tok/s de geração medidos na Fase 2-B;
    modelo fora da tabela cai no padrão (50 ms/token e 4 tok/s) em vez de somar zero, que
    faria a projeção mentir para baixo justamente no modelo que ninguém mediu."""
    p = executar_fase3.projecao_tempo(["qwen2.5-coder:3b"], 90, 54)
    assert "total_h" in p, p
    assert p["total_h"] > 0, p
    por_modelo = p["por_modelo"]["qwen2.5-coder:3b"]
    assert por_modelo["total_h"] > 0, por_modelo
    assert por_modelo["diagnosticos_h"] > 0 and por_modelo["propostas_h"] > 0, por_modelo
    assert abs(por_modelo["diagnosticos_h"] + por_modelo["propostas_h"]
               - por_modelo["total_h"]) < 0.01, por_modelo

    # Granite é o mais lento medido na 2-B e o 3b o mais rápido: a projeção tem de ordená-los
    # assim, senão a tabela de ms/token está trocada.
    dois = executar_fase3.projecao_tempo(["granite4.2:8b", "qwen2.5-coder:3b"], 90, 54)
    assert (dois["por_modelo"]["granite4.2:8b"]["total_h"]
            > dois["por_modelo"]["qwen2.5-coder:3b"]["total_h"]), dois
    assert abs(dois["total_h"] - sum(m["total_h"] for m in dois["por_modelo"].values())) < 0.01

    desconhecido = executar_fase3.projecao_tempo(["modelo:nunca-medido"], 90, 54)
    assert desconhecido["total_h"] > 0, desconhecido


# ! Alteração de IA - Revisar: testes do round 1 de revisão da Tarefa 7 — inferência que volta
# com erro de rede, conferência do contexto reconstruído na proposta órfã e conferência de
# cobertura de uma época já fechada.
# ! Motivo: os três são estados que só aparecem numa corrida de 60 horas e que, antes da
# correção, passavam em silêncio: o caso com erro de rede ficava gravado como feito para
# sempre (e a proposta saía de uma resposta vazia), a retomada de uma proposta órfã montava o
# contexto de novo sem conferir se era o mesmo do diagnóstico gravado, e uma época fechada com
# 3 casos era pulada inteira quando a execução pedia 90.


def teste_executor_repete_inferencia_com_erro() -> None:
    """Falha de rede não pode virar registro: o executor repete a inferência até três vezes e,
    se a última ainda voltar com erro, para com SystemExit SEM gravar nada — do contrário o
    caso ficaria marcado como feito para sempre, com resposta vazia, e a proposta daquele caso
    sairia de um diagnóstico que nunca aconteceu."""
    casos = _casos_do_piloto(2)
    particao = evo.particionar(CASOS + CASOS_EXTRA)

    # Duas falhas e acerto na terceira tentativa: o caso é gravado UMA vez, sem 'erro'.
    c3 = _c3_temporario("fase3_repete")
    chamadas = _rodar(c3, casos, particao, {}, falhas_iniciais=2)
    pasta = c3["raiz"] / _SLUG_DE_MENTIRA
    diag0 = executar_bateria.ler_jsonl(pasta / "diagnosticos__L0.jsonl")
    assert len(diag0) == 2, diag0
    assert all("erro" not in r for r in diag0), diag0
    assert list(diag0[0].keys()) == _CHAVES_DIAGNOSTICO, list(diag0[0].keys())
    # 2 falhas + 2 diagnósticos + 1 proposta + 2 diagnósticos da passada final.
    assert len(chamadas) == 7, len(chamadas)

    # Falha em todas as tentativas: SystemExit nomeando o caso e o tipo, e JSONL vazio.
    c3b = _c3_temporario("fase3_sem_ollama")
    try:
        _rodar(c3b, casos, particao, {}, falhar_sempre=True)
        assert False, "três tentativas falhas deveriam levantar SystemExit"
    except SystemExit as e:
        texto = str(e)
        assert casos[0]["id"] in texto, texto
        assert "diagnóstico" in texto, texto
        assert _ERRO_DE_MENTIRA in texto, texto
    vazio = executar_bateria.ler_jsonl(
        c3b["raiz"] / _SLUG_DE_MENTIRA / "diagnosticos__L0.jsonl")
    assert vazio == [], vazio


def teste_executor_confere_contexto_do_orfao() -> None:
    """A proposta órfã (diagnóstico gravado, proposta não) monta o prompt de novo a partir do
    snapshot; se o contexto reconstruído não for o mesmo que está no registro de diagnóstico —
    aqui provocado relançando com k=2 em vez de k=3 —, a proposta seria a continuação de um
    prompt que o modelo nunca viu. Tem de parar dizendo os dois lados."""
    casos = _casos_do_piloto(2)
    particao = evo.particionar(CASOS + CASOS_EXTRA)
    c3 = _c3_temporario("fase3_orfao")

    # 1: lex-1 diagnóstico, 2: lex-2 diagnóstico, 3: lex-2 proposta -> parar na 3ª deixa
    # lex-2 com diagnóstico gravado e sem proposta.
    try:
        _rodar(c3, casos, particao, {}, parar_em=3)
        assert False, "o stub deveria ter interrompido na 3ª inferência"
    except KeyboardInterrupt:
        pass
    pasta = c3["raiz"] / _SLUG_DE_MENTIRA
    com_diag = [r["caso"] for r in
                executar_bateria.ler_jsonl(pasta / "diagnosticos__L0.jsonl")]
    assert casos[1]["id"] in com_diag, com_diag
    assert not (pasta / "propostas__E1.jsonl").exists(), "não era para ter proposta ainda"

    try:
        _rodar(c3, casos, particao, {}, k=2)
        assert False, "k diferente do gravado deveria levantar SystemExit"
    except SystemExit as e:
        texto = str(e)
        assert casos[1]["id"] in texto, texto
        assert "k" in texto and "2" in texto and "3" in texto, texto


def teste_executor_epoca_fechada_confere_cobertura() -> None:
    """Época fechada só pode ser pulada se ela cobre TODOS os casos que esta execução pede.
    Fechar com --casos 3 e relançar com --casos 6 na mesma pasta pularia a época inteira e a
    passada final mediria 6 casos contra uma biblioteca construída com 3 — tem de parar."""
    particao = evo.particionar(CASOS + CASOS_EXTRA)
    tres = _casos_do_piloto(3)
    seis = _casos_do_piloto(6)
    c3 = _c3_temporario("fase3_cobertura")

    _rodar(c3, tres, particao, {})
    pasta_bib = c3["bibliotecas"] / _SLUG_DE_MENTIRA
    assert evo.snapshot_fechado(pasta_bib / "epoca-1"), "epoca-1 devia ter fechado"

    try:
        _rodar(c3, seis, particao, {})
        assert False, "época fechada com menos casos deveria levantar SystemExit"
    except SystemExit as e:
        texto = str(e)
        assert "epoca-1" in texto, texto
        assert "6" in texto, texto
        assert "--saida" in texto or "--casos" in texto, texto


# ----------------------------------------------------------------- Tarefa 8: avaliação

_MODELO_AVAL = "modelo:avaliado"
_SLUG_AVAL = "modelo_avaliado"

# Textos de nota escritos de propósito em prosa genérica: bib.validar recusa verbete cujo
# texto repita 30% dos 5-gramas de algum dos 90 casos (cópia do caso), e fechar_epoca roda
# essa validação sobre o banco inteiro antes de gravar o fechamento.json.
_TEXTOS_NOTA = (
    ("A resposta pode chegar inteira e ainda assim faltar a chave que a tela le para "
     "montar o rotulo do item",
     "o verbete nao dizia o que a tela faz quando a chave nao vem"),
    ("Vale conferir o corpo todo antes de concluir, porque o servidor devolve 200 mesmo "
     "quando o contrato mudou de forma",
     "o verbete nao lembrava de conferir o corpo mesmo com 200"),
)

_RESPOSTA_DIAGNOSTICO = ("CAUSA_RAIZ: {causa}\nCAMPO: nenhum\n"
                         "IMPACTO: a tela nao mostra o dado esperado.\nFONTE: [{ouro}]")

# Payload de teste do escaping do relatório da Tarefa 11 (gerar_relatorio_fase3.py): se o
# HTML gerado o deixasse cru dentro do <script> de dados embutidos, o navegador fecharia a
# tag ao encontrar "</script>" e o restante do JSON viraria texto solto na página.
_RESPOSTA_PROPOSTA_HOSTIL = "(resposta de mentira) <script>alert(1)</script>"


def _edicao_nota(raiz: Path, caso_id: str, verbete_id: str, texto: str,
                 motivo: str) -> dict:
    """A edição no formato que evolucao_biblioteca.validar_proposta devolve em ["edicao"]
    e que aplicar_edicao grava — montada à mão para o teste não pagar o laço de
    validar_proposta sobre os 90 casos (já coberto pelos testes da Tarefa 5)."""
    alvo = [v for v in bib.carregar(raiz) if v["id"] == verbete_id][0]
    return {"epoca": 1, "caso": caso_id, "numero": 1, "operacao": "nota",
            "verbete": verbete_id,
            "arquivo": alvo["caminho"].relative_to(raiz).as_posix(),
            "texto": texto, "motivo": motivo, "trecho": None,
            "palavras_chave_novas": [], "sintomas_novos": [], "novo": None,
            "modelo": _MODELO_AVAL}


def _diagnostico_sintetico(caso: dict, verbetes: list[dict], indice: recuperacao.Indice,
                           versao: str, epoca: int, particao: dict, acertou: bool,
                           k: int = 3) -> dict:
    """Um registro de diagnóstico no formato de executar_fase3.diagnosticar, com o
    contexto REAL recuperado do snapshot — é assim que contexto_sha256 fica igual ao que
    avaliar_fase3.reconstrucao_ok recalcula."""
    ctx = recuperacao.contexto(verbetes, indice, caso, "A2", k)
    certa = caso["gabarito"]["causa_raiz"]
    respondida = certa if acertou else next(
        c for c in ("campo_ausente", "corpo_vazio") if c != certa)
    por_id = {v["id"]: v for v in verbetes}
    recuperados = [por_id[i] for i in ctx["verbetes_ids"] if i in por_id]
    return {
        "modelo": _MODELO_AVAL, "digest": "deadbeef0000", "maquina": "teste",
        "caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"],
        "estrategia": "linear", "condicao": "A2",
        "fase": "3", "tipo": "diagnostico", "epoca": epoca,
        "biblioteca_epoca": epoca - 1, "biblioteca_versao": versao,
        "particao": evo.particao_de(particao, caso["id"]), "k": k,
        "contexto_sha256": executar_fase3._sha12(ctx["texto"]),
        "notas_no_contexto": sum(len(bib.notas(v)) for v in recuperados),
        "verbetes_novos_no_contexto": [v["id"] for v in recuperados
                                       if v["pasta"] == evo.PASTA_APRENDIDOS],
        "contexto_estourou": False,
        "verbetes_ids": ctx["verbetes_ids"], "verbete_ouro": ctx["verbete_ouro"],
        "causa_plantada": None, "chars_contexto": len(ctx["texto"]),
        "gabarito": caso["gabarito"], "teto_tokens": 600,
        "segundos": 40.0, "tokens_entrada": 1500, "tokens_saida": 60, "carga_ms": 0,
        "prefill_ms": 30000, "geracao_ms": 10000, "total_ms": 40000,
        "resposta": _RESPOSTA_DIAGNOSTICO.format(causa=respondida,
                                                 ouro=ctx["verbete_ouro"]),
        "somente_cpu": True, "modelos_residentes": 1, "memoria_mb": 1900,
    }


def _proposta_sintetica(caso: dict, particao: dict, versao: str, hash_apos: str,
                        decisoes: list[dict], nenhuma: bool, acertou: bool,
                        fim_ausente: bool = False,
                        resposta: str = "(resposta de mentira)") -> dict:
    """Um registro de proposta no formato de executar_fase3.propor, com os campos que a
    avaliação da documentação lê (decisões, motivos, blocos parseados e tempos). O parâmetro
    `resposta` tem um valor padrão inócuo e existe para o teste de escaping do relatório da
    Tarefa 11 poder passar um texto hostil (`<script>...</script>`) sem mexer no formato do
    registro nem nas contagens que teste_avaliar_fase3_sintetico já confere."""
    blocos = [{"numero": d["numero"], "campos": {"OPERACAO": d["operacao"] or ""},
               "malformado": None, "fim_ausente": fim_ausente} for d in decisoes]
    return {
        "modelo": _MODELO_AVAL, "digest": "deadbeef0000", "maquina": "teste",
        "fase": "3", "tipo": "proposta", "epoca": 1, "biblioteca_epoca": 0,
        "biblioteca_versao": versao, "caso": caso["id"], "classe": caso["classe"],
        "nivel": caso["nivel"], "particao": evo.particao_de(particao, caso["id"]),
        "k": 3, "verbetes_ids": [], "verbete_ouro": "campo_ausente",
        "ouro_no_contexto": True, "ids_visiveis": [],
        "causa_correta_mostrada": caso["gabarito"]["causa_raiz"], "campo_mostrado": None,
        "causa_respondida": caso["gabarito"]["causa_raiz"] if acertou else "corpo_vazio",
        "acertou_diagnostico": acertou, "prompt": "(prompt de mentira)",
        "teto_tokens": 700,
        "segundos": 60.0, "tokens_entrada": 2400, "tokens_saida": 180, "carga_ms": 0,
        "prefill_ms": 24000, "geracao_ms": 36000, "total_ms": 60000,
        "resposta": resposta,
        "contexto_estourou": False, "resposta_truncada": False, "nenhuma": nenhuma,
        "propostas_parseadas": blocos, "decisoes": decisoes,
        "n_propostas": len(blocos),
        "n_aceitas": sum(1 for d in decisoes if d["aceita"]),
        "motivos_rejeicao": [d["motivo"] for d in decisoes
                             if not d["aceita"] and d["motivo"]],
        "somente_cpu": True, "modelos_residentes": 1, "memoria_mb": 1900,
        "hash_biblioteca_apos": hash_apos,
    }


def _arvore_fase3_sintetica() -> dict:
    """Monta em pasta temporária a árvore mínima que avaliar_fase3 lê: particao.json, duas
    cópias de verdade da biblioteca (epoca-0 original e epoca-1 com duas notas aplicadas e
    fechada por fechar_epoca, que grava o diff__E1.json), 6 diagnósticos por versão (2 de
    avaliação e 4 de aprendizado, com os acertos escolhidos para dar b=2 e c=1 contra a L0)
    e as 4 propostas da época 1 (2 aceitas, 1 recusada por copia_do_caso e 1 NENHUMA)."""
    c3 = _c3_temporario("fase3_aval")
    particao = evo.particionar(CASOS + CASOS_EXTRA)
    c3["raiz"].mkdir(parents=True, exist_ok=True)
    evo.gravar_ou_conferir_particao(c3["particao"], particao)

    todos = CASOS + CASOS_EXTRA
    aprendizado = [c for c in todos
                   if evo.particao_de(particao, c["id"]) == "aprendizado"][:4]
    avaliacao = [c for c in todos
                 if evo.particao_de(particao, c["id"]) == "avaliacao"][:2]
    casos = aprendizado + avaliacao

    pasta = c3["raiz"] / _SLUG_AVAL
    pasta.mkdir(parents=True, exist_ok=True)
    pasta_bib = c3["bibliotecas"] / _SLUG_AVAL

    l0 = pasta_bib / "epoca-0"
    evo.copiar_biblioteca(bib.BASE, l0)
    validar_banco.escrever_indice(bib.carregar(l0), l0)
    fech0 = evo.fechar_snapshot(l0, 0, _MODELO_AVAL, 0)

    l1 = pasta_bib / "epoca-1"
    evo.copiar_biblioteca(l0, l1)
    # copiar_biblioteca clona a pasta inteira: sem apagar o fechamento.json da época 0, a
    # epoca-1 nasceria "já fechada" (é o mesmo que evo._limpar_gerados faz na retomada).
    (l1 / "fechamento.json").unlink()
    hashes, edicoes = [], []
    for ordem, (caso, (texto, motivo)) in enumerate(zip(aprendizado, _TEXTOS_NOTA), 1):
        ouro = recuperacao.verbete_ouro(bib.carregar(l1), caso)["id"]
        edicao = _edicao_nota(l1, caso["id"], ouro, texto, motivo)
        evo.aplicar_edicao(l1, edicao)
        depois = evo.hash_biblioteca(l1)
        evo.registrar_historico(pasta_bib, edicao, {
            "ordem": ordem, "acertou_diagnostico": True, "hash_apos": depois})
        edicoes.append(edicao)
        hashes.append(depois)
    fech1 = evo.fechar_epoca(pasta_bib, 1, _MODELO_AVAL, todos, 2)

    # (L0 errou, L1 acertou) nos dois primeiros casos de aprendizado dá b=2; o terceiro, ao
    # contrário, dá c=1; os outros três acertam ou erram nas duas versões.
    acertos = {aprendizado[0]["id"]: (False, True), aprendizado[1]["id"]: (False, True),
               aprendizado[2]["id"]: (True, False), aprendizado[3]["id"]: (True, True),
               avaliacao[0]["id"]: (False, False), avaliacao[1]["id"]: (True, True)}
    for versao_n, (raiz, versao) in enumerate([(l0, fech0["hash"]), (l1, fech1["hash"])]):
        verbetes = bib.carregar(raiz)
        indice = recuperacao.Indice(verbetes)
        linhas = [_diagnostico_sintetico(c, verbetes, indice, versao, versao_n + 1,
                                         particao, acertos[c["id"]][versao_n])
                  for c in casos]
        (pasta / f"diagnosticos__L{versao_n}.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in linhas),
            encoding="utf-8")

    def aceita(edicao: dict) -> dict:
        return {"numero": 1, "operacao": "nota", "verbete": edicao["verbete"],
                "aceita": True, "motivo": None,
                "detalhe": "nota em [" + edicao["verbete"] + "]", "edicao": edicao}

    propostas = [
        # A resposta desta proposta traz um payload hostil (usado por
        # teste_relatorio_fase3_sintetico, Tarefa 11) para confirmar que o relatório HTML
        # escapa texto de MODELO antes de embuti-lo no <script> da página -- e não só o que
        # o harness escreve. Não afeta nenhuma conta de teste_avaliar_fase3_sintetico, que
        # não lê o campo "resposta" das propostas.
        _proposta_sintetica(aprendizado[0], particao, fech0["hash"], hashes[0],
                            [aceita(edicoes[0])], False, True,
                            resposta=_RESPOSTA_PROPOSTA_HOSTIL),
        _proposta_sintetica(aprendizado[1], particao, fech0["hash"], hashes[1],
                            [aceita(edicoes[1])], False, True, fim_ausente=True),
        _proposta_sintetica(aprendizado[2], particao, fech0["hash"], hashes[1],
                            [{"numero": 1, "operacao": "nota", "verbete": "campo_ausente",
                              "aceita": False, "motivo": "copia_do_caso",
                              "detalhe": "5-gramas do caso", "edicao": None}],
                            False, False),
        _proposta_sintetica(aprendizado[3], particao, fech0["hash"], hashes[1],
                            [], True, False),
    ]
    (pasta / "propostas__E1.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in propostas),
        encoding="utf-8")
    return c3


def teste_cochran_holm_quiquadrado() -> None:
    """As quatro funções estatísticas escritas à mão, conferidas contra valores de tabela:
    Cochran Q de uma matriz 4x3 calculada à mão (Q=3, gl=2), os pontos de 5% e 1% da tabela
    do qui-quadrado com 1 a 4 graus de liberdade, o ajuste de Holm de três p e o g de Cohen
    (parcela das discordâncias a favor da versão nova, centrada em zero)."""
    q, gl, p = avaliar_fase3.cochran_q([[1, 1, 0], [1, 0, 0], [1, 1, 1], [0, 0, 0]])
    assert abs(q - 3.0) < 1e-3, q
    assert gl == 2, gl
    assert abs(p - 0.2231) < 1e-3, p

    for x, graus, esperado in ((7.815, 3, 0.05), (11.345, 3, 0.01), (3.841, 1, 0.05),
                               (5.991, 2, 0.05), (9.488, 4, 0.05)):
        obtido = avaliar_fase3.qui_quadrado_sf(x, graus)
        assert abs(obtido - esperado) < 5e-4, (x, graus, obtido, esperado)

    assert avaliar_fase3.holm([0.01, 0.04, 0.03]) == [0.03, 0.06, 0.06], \
        avaliar_fase3.holm([0.01, 0.04, 0.03])
    assert avaliar.mcnemar_exato(0, 0) == 1.0, avaliar.mcnemar_exato(0, 0)
    assert avaliar_fase3.g_cohen(6, 2) == 0.25, avaliar_fase3.g_cohen(6, 2)
    assert avaliar_fase3.g_cohen(0, 0) is None, avaliar_fase3.g_cohen(0, 0)

    # Denominador zero (todo caso acertou nas três versões, ou nenhum acertou): Q não é
    # calculável e a linha sai neutra, em vez de dividir por zero no meio do resumo.
    assert avaliar_fase3.cochran_q([[1, 1, 1], [0, 0, 0]]) == (0.0, 2, 1.0), \
        avaliar_fase3.cochran_q([[1, 1, 1], [0, 0, 0]])


def teste_acuracia_balanceada_e_distribuicao() -> None:
    """Acurácia balanceada (média do acerto POR causa esperada, não do acerto geral): com
    a causa A acertada 3 vezes em 3 e a causa B nenhuma vez em 3 dá 50,0; com 4 em 4 numa e
    0 em 2 na outra continua 50,0, enquanto o acerto geral seria 66,7 — é esse o número que
    a tabela precisa quando as causas aparecem em quantidades diferentes. E a distribuição
    dos rótulos respondidos, que é o que denuncia o modelo que responde sempre o mesmo."""
    pares = ([("campo_ausente", "campo_ausente")] * 3
             + [("tipo_divergente", "campo_ausente")] * 3)
    assert avaliar_fase3.acuracia_balanceada(pares) == 50.0, \
        avaliar_fase3.acuracia_balanceada(pares)

    desiguais = ([("campo_ausente", "campo_ausente")] * 4
                 + [("corpo_vazio", "campo_ausente")] * 2)
    assert avaliar_fase3.acuracia_balanceada(desiguais) == 50.0, \
        avaliar_fase3.acuracia_balanceada(desiguais)
    assert avaliar_fase3.acuracia_balanceada([]) == 0.0

    rotulo, parcela, distintos = avaliar_fase3.distribuicao_de_rotulos(
        ["campo_ausente", "campo_ausente", "tipo_divergente", None])
    assert rotulo == "campo_ausente", rotulo
    assert parcela == 50.0, parcela
    # "(sem resposta)" conta como rótulo próprio: não responder nada é comportamento
    # diferente de responder sempre o mesmo rótulo, e os dois precisam aparecer na conta.
    assert distintos == 3, distintos
    vazio = avaliar_fase3.distribuicao_de_rotulos([])
    assert vazio == (None, 0.0, 0), vazio


def teste_avaliar_fase3_sintetico() -> None:
    """A avaliação inteira sobre a árvore sintética: o Δ pareado contra a L0 conta b=2 e
    c=1 nos 6 casos, o histograma de rejeições fecha com a única recusa por copia_do_caso,
    a recuperação é medida nas duas versões da biblioteca, o contexto gravado em cada
    diagnóstico é reconstruído do snapshot e bate, e a planilha de revisão humana sai com
    uma linha por edição aceita e não é sobrescrita numa segunda execução."""
    c3 = _arvore_fase3_sintetica()
    avaliados, resumo = avaliar_fase3.avaliar_saida(c3, gerar_revisao=True)

    assert len(avaliados) == 12, len(avaliados)
    assert resumo["metadados"]["n_diagnosticos"] == 12, resumo["metadados"]
    assert resumo["metadados"]["n_propostas"] == 4, resumo["metadados"]
    assert resumo["metadados"]["modelos"] == [_MODELO_AVAL], resumo["metadados"]

    pareado = [p for p in resumo["pareado_vs_L0"]
               if p["modelo"] == _MODELO_AVAL and p["biblioteca_epoca"] == 1
               and p["particao"] == "todos"]
    assert len(pareado) == 1, pareado
    assert pareado[0]["b"] == 2 and pareado[0]["c"] == 1, pareado[0]
    assert pareado[0]["n_pares"] == 6, pareado[0]
    assert pareado[0]["acerto_L0_pct"] == 50.0, pareado[0]
    assert pareado[0]["acerto_pct"] == round(100 * 4 / 6, 1), pareado[0]
    assert pareado[0]["razao_bc"] == 2.0, pareado[0]
    assert pareado[0]["g_cohen"] == round(2 / 3 - 0.5, 3), pareado[0]

    doc = [d for d in resumo["documentacao"] if d["epoca"] == 1][0]
    assert doc["motivos_rejeicao"]["copia_do_caso"] == 1, doc["motivos_rejeicao"]
    assert doc["n_casos_aprendizado"] == 4, doc
    assert doc["n_propostas"] == 3 and doc["n_aceitas"] == 2, doc
    assert doc["n_nenhuma"] == 1, doc
    assert doc["n_fim_ausente"] == 1, doc
    assert doc["tentativas_de_decorar"] == 1, doc
    assert doc["por_operacao"]["nota"] == {"propostas": 3, "aceitas": 2}, \
        doc["por_operacao"]
    assert doc["biblioteca"]["n_notas"] == 2, doc["biblioteca"]
    # Bytes crus dos .md (do diff__E1.json) levam 'md' no nome, para não serem lidos como
    # o tamanho renderizado (chars/tokens_estimados do fechamento) da figura 15.
    assert doc["chars_md_acrescentados"] > 0, doc
    assert doc["tokens_md_estimados_acrescentados"] > 0, doc
    assert "chars_acrescentados" not in doc and "tokens_estimados_acrescentados" not in doc
    assert doc["quando_acertou"]["aceitas"] == 2, doc["quando_acertou"]

    versoes = [r["biblioteca_epoca"] for r in resumo["recuperacao"]]
    assert versoes == [0, 1], versoes
    # O tamanho RENDERIZADO de cada versão (o que entra no prompt) vem do fechamento.json e
    # é o que a figura 15 plota, L0 inclusive.
    fech0 = json.loads((c3["bibliotecas"] / _SLUG_AVAL / "epoca-0" / "fechamento.json")
                       .read_text(encoding="utf-8"))
    assert resumo["recuperacao"][0]["tokens_estimados"] == fech0["tokens_estimados"], \
        resumo["recuperacao"][0]
    assert resumo["recuperacao"][0]["chars"] == fech0["chars"], resumo["recuperacao"][0]
    assert resumo["recuperacao"][1]["tokens_estimados"] > fech0["tokens_estimados"], \
        resumo["recuperacao"][1]
    assert all(0 <= r["todos"]["hit@3"] <= 100 for r in resumo["recuperacao"]), \
        resumo["recuperacao"]
    assert resumo["recuperacao"][0]["ouro_recuperavel_apos_edicao"] is None, \
        resumo["recuperacao"][0]
    assert resumo["recuperacao"][1]["ouro_recuperavel_apos_edicao"] is not None, \
        resumo["recuperacao"][1]

    rec_ok = resumo["reconstrucao_ok"][0]
    assert rec_ok["conferidos"] == 6 and rec_ok["ok"] == 6, rec_ok

    cochran = [c for c in resumo["cochran_q"] if c["particao"] == "todos"][0]
    assert cochran["n_casos"] == 6, cochran
    flips = [f for f in resumo["flips"]
             if f["transicao"] == "L0→L1" and f["particao"] == "todos"][0]
    assert flips["certo_para_errado"] == 1, flips
    assert flips["errado_para_certo"] == 2, flips

    minimo = {e["n"]: e for e in resumo["efeito_minimo_detectavel"]}
    assert sorted(minimo) == [36, 54, 90], sorted(minimo)
    assert minimo[90]["discordantes"] == 18 and minimo[90]["b_min"] == 14, minimo[90]

    planilha = c3["raiz"] / ("revisao_edicoes__" + _SLUG_AVAL + ".md")
    assert planilha.exists(), planilha
    linhas = [linha for linha in planilha.read_text(encoding="utf-8").splitlines()
              if linha.startswith("| ") and not linha.startswith("| #")]
    assert len(linhas) == 2, linhas
    antes = planilha.stat().st_mtime_ns
    avaliar_fase3.avaliar_saida(c3, gerar_revisao=True)
    assert planilha.stat().st_mtime_ns == antes, "a planilha de revisão foi sobrescrita"

    assert c3["avaliacao"].exists() and c3["resumo"].exists(), c3
    gravado = json.loads(c3["resumo"].read_text(encoding="utf-8"))
    assert list(gravado) == list(resumo), (list(gravado), list(resumo))


def _reg_avaliado(modelo: str, caso: str, estrategia: str, condicao: str, correta: bool,
                  segundos: float = 40.0, tokens_saida: int = 60,
                  citou_verbete: bool = False, ouro_no_contexto: bool = False,
                  causa_plantada: str | None = None, seguiu_causa_plantada: bool = False,
                  causa_esperada: str = "campo_ausente", **extra) -> dict:
    """Um registro no formato de avaliar.avaliar_registro (2-A/2-B) ou de
    avaliar_fase3.avaliar_registro_fase3 (Fase 3, via **extra com biblioteca_epoca/
    particao) -- só os campos que comparar_fases.py lê, montados à mão para o teste da
    Tarefa 9 não depender do banco de 90 casos nem de um Ollama de mentira."""
    respondida = causa_esperada if correta else "corpo_vazio"
    return {
        "modelo": modelo, "caso": caso, "classe": 1, "nivel": 1, "estrategia": estrategia,
        "segundos": segundos, "tokens_saida": tokens_saida, "condicao": condicao,
        "causa_correta": correta, "causa_respondida": respondida,
        "causa_esperada": causa_esperada, "fora_do_conjunto": False,
        "formato_valido_conteudo_errado": not correta,
        "citou_verbete": citou_verbete, "ouro_no_contexto": ouro_no_contexto,
        "causa_plantada": causa_plantada, "seguiu_causa_plantada": seguiu_causa_plantada,
        **extra,
    }


def _arvore_comparar_fases_sintetica() -> dict:
    """! Alteração de IA - Revisar: monta em pasta temporária os arquivos que
    comparar_fases.py lê -- avaliacao.json da Fase 2-A e da Fase 2-B (mesmo modelo, 6 casos no
    braço linear; A5 com 3) e uma saída de Fase 3 (particao.json, avaliacao_fase3.json,
    resumo_fase3.json) com biblioteca_epoca 0 e 3 para os mesmos 6 casos. Um dos ids é
    'sin-1', um dos 4 que a Tarefa 1 corrigiu no banco de casos antes da Fase 3 (achado 4.20
    do Memorial: sin-1/sin-2/semt-13 descreviam 'R$ NaN' e efe-13 cartões duplicados, sintomas
    que produtos_api.php não produz) -- é o que permite ao teste conferir que o pareamento
    2B_A2 x F3_L0 exclui esse id do conjunto '86'.
    ! Motivo: comparar_fases.py não reavalia nada, só relê os avaliacao.json/
    avaliacao_fase3.json/resumo_fase3.json que os avaliadores das três fases já gravam --
    montar esses três arquivos à mão é mais direto e determinístico que rodar avaliar.py/
    avaliar_fase3.py inteiros (que exigiriam o banco de 90 casos reais e um Ollama de mentira
    só para produzir seis linhas de cada). Os ids de caso (fora 'sin-1') são inventados
    porque o que está sob teste é a junção dos três arquivos, não o cálculo de nenhum deles."""
    ids = ["sin-1", "c2", "c3", "c4", "c5", "c6"]

    pasta = _pasta_temporaria()
    caminho_2a = pasta / "avaliacao_2a.json"
    caminho_2b = pasta / "avaliacao_2b.json"

    # 2-A (Ryzen), A0/linear: 4 de 6 corretos (66,7%).
    corretos_2a = dict(zip(ids, (True, True, False, True, False, True)))
    # 2-B A0: 3 de 6 (50,0%); 2-B A2: 4 de 6 (66,7%) -- o número que o teste confere.
    corretos_2b_a0 = dict(zip(ids, (True, False, False, True, False, True)))
    corretos_2b_a2 = dict(zip(ids, (True, True, True, True, False, False)))

    # Segundos/tokens diferentes por fase (mesmo valor nos 6 casos da fase, para a mediana
    # e a média saírem exatas) -- de propósito, o s/caso mais baixo (30,0, em F3 L0) e o
    # tokens mais baixo (50, em 2B A2) NÃO caem na primeira coluna da Tabela 3: é o que
    # confere que o negrito da Tarefa 9 (Fix round 1, item 1) acha o mínimo onde ele estiver,
    # não só quando calha de ser a 2-A.
    reg_2a = [_reg_avaliado(_MODELO_AVAL, cid, "linear", "A0", corretos_2a[cid],
                            segundos=50.0, tokens_saida=100)
             for cid in ids]
    reg_2b = [_reg_avaliado(_MODELO_AVAL, cid, "linear", "A0", corretos_2b_a0[cid],
                            segundos=45.0, tokens_saida=90)
             for cid in ids]
    reg_2b += [_reg_avaliado(_MODELO_AVAL, cid, "linear", "A2", corretos_2b_a2[cid],
                             citou_verbete=True, ouro_no_contexto=corretos_2b_a2[cid],
                             segundos=42.0, tokens_saida=50)
              for cid in ids]
    # A5 (adesão cega): só 3 casos, com a causa plantada no contexto -- 2 de 3 seguem a
    # causa plantada em vez do gabarito.
    seguiu_a5 = dict(zip(ids[1:4], (True, True, False)))
    reg_2b += [_reg_avaliado(_MODELO_AVAL, cid, "linear", "A5", False,
                             causa_plantada="corpo_vazio",
                             seguiu_causa_plantada=seguiu_a5[cid])
              for cid in ids[1:4]]

    caminho_2a.write_text(json.dumps(reg_2a, ensure_ascii=False), encoding="utf-8")
    caminho_2b.write_text(json.dumps(reg_2b, ensure_ascii=False), encoding="utf-8")

    c3 = _c3_temporario("fase3_comparacao")
    c3["raiz"].mkdir(parents=True, exist_ok=True)
    # partição de mentira: os 4 primeiros ids (inclusive sin-1) em aprendizado, os 2
    # últimos em avaliação -- não precisa bater com a partição real de 90 casos, porque o
    # que está sob teste é como comparar_fases.py CONSOME particao.json, não o sorteio dela.
    particao = {
        "regra": "de mentira, só para o teste", "semente": "teste",
        "n_aprendizado": 4, "n_avaliacao": 2,
        "casos": {cid: {"particao": "aprendizado" if cid in ids[:4] else "avaliacao",
                       "classe": 1, "nivel": 1, "hash": "x"} for cid in ids},
    }
    c3["particao"].write_text(json.dumps(particao, ensure_ascii=False), encoding="utf-8")

    # F3 L0: 4 de 6 corretos excluindo sin-1 (80% nos 5 restantes); F3 L3: mistura diferente,
    # só para os pareamentos L0 x L3 não saírem triviais.
    corretos_l0 = dict(zip(ids, (True, True, True, False, True, True)))
    corretos_l3 = dict(zip(ids, (False, True, False, True, True, False)))
    # F3 L0 leva o menor s/caso (30,0) de toda a linha; F3 L3 fica no meio (35,0) -- nenhum
    # dos dois é a primeira coluna (2-A, 50,0).
    segundos_por_epoca = {0: 30.0, 3: 35.0}
    tokens_por_epoca = {0: 70, 3: 80}
    fase3 = []
    for epoca, corretos in ((0, corretos_l0), (3, corretos_l3)):
        for cid in ids:
            fase3.append(_reg_avaliado(
                _MODELO_AVAL, cid, "linear", "A2", corretos[cid],
                citou_verbete=True, ouro_no_contexto=corretos[cid],
                biblioteca_epoca=epoca, particao=particao["casos"][cid]["particao"],
                segundos=segundos_por_epoca[epoca], tokens_saida=tokens_por_epoca[epoca]))
    c3["avaliacao"].write_text(json.dumps(fase3, ensure_ascii=False), encoding="utf-8")

    # resumo_fase3.json mínimo: só os dois blocos que comparar_fases.py lê de lá
    # (documentacao para tentativas_de_decorar_F3, flips para autoenvenenamento_F3).
    resumo_f3 = {
        "documentacao": [
            {"modelo": _MODELO_AVAL, "epoca": 1, "tentativas_de_decorar": 1},
            {"modelo": _MODELO_AVAL, "epoca": 2, "tentativas_de_decorar": 0},
            {"modelo": _MODELO_AVAL, "epoca": 3, "tentativas_de_decorar": 2},
        ],
        "flips": [
            {"modelo": _MODELO_AVAL, "transicao": "L0→L1", "particao": "avaliacao",
             "autoenvenenamento_pct": 0.0},
            {"modelo": _MODELO_AVAL, "transicao": "L1→L2", "particao": "avaliacao",
             "autoenvenenamento_pct": 50.0},
            {"modelo": _MODELO_AVAL, "transicao": "L2→L3", "particao": "avaliacao",
             "autoenvenenamento_pct": 0.0},
        ],
    }
    c3["resumo"].write_text(json.dumps(resumo_f3, ensure_ascii=False), encoding="utf-8")
    return {"c3": c3, "caminho_2a": caminho_2a, "caminho_2b": caminho_2b}


def teste_comparar_fases_sintetico() -> None:
    """A comparação inteira sobre os avaliacao.json/avaliacao_fase3.json/resumo_fase3.json
    sintéticos: o acerto de 2B_A2 sai 66,7% (4 de 6, n=6), o pareamento 2B_A2 x F3_L0 no
    conjunto '86' exclui 'sin-1' (n_comuns cai de 6 para 5) e o mesmo pareamento no conjunto
    '36' (a partição de avaliação, que já não inclui 'sin-1') sai idêntico, e o .md gerado tem
    as 5 tabelas (uma linha separadora '|---' por tabela) sem nenhum 'None' de Python
    vazando para o texto."""
    fixture = _arvore_comparar_fases_sintetica()
    c3 = fixture["c3"]
    comparacao = comparar_fases.gerar_comparacao(
        fixture["caminho_2a"], fixture["caminho_2b"], c3)

    assert list(comparacao["por_modelo"]) == [_MODELO_AVAL], comparacao["por_modelo"]
    bloco = comparacao["por_modelo"][_MODELO_AVAL]["nos_90"]
    assert bloco["2B_A2"]["n"] == 6, bloco["2B_A2"]
    assert bloco["2B_A2"]["acerto_pct"] == round(100 * 4 / 6, 1), bloco["2B_A2"]
    assert bloco["2A_linear_ryzen"]["acerto_pct"] == round(100 * 4 / 6, 1), \
        bloco["2A_linear_ryzen"]
    assert bloco["F3_L0"]["acerto_pct"] == round(100 * 5 / 6, 1), bloco["F3_L0"]

    pareamentos = comparacao["pareamentos"]
    assert len(pareamentos) == 6, pareamentos
    p86 = [p for p in pareamentos
          if p["a"] == "2B_A2" and p["b"] == "F3_L0" and p["conjunto"] == "86"][0]
    assert p86["n_comuns"] == 5, p86
    p36 = [p for p in pareamentos
          if p["a"] == "2B_A2" and p["b"] == "F3_L0" and p["conjunto"] == "36"][0]
    assert p36["n_comuns"] == 2, p36

    adesao = comparacao["por_modelo"][_MODELO_AVAL]["adesao_cega_2B_A5_pct"]
    assert adesao == round(100 * 2 / 3, 1), adesao

    assert c3["comparacao"].exists() and c3["comparacao_md"].exists(), c3
    gravado = json.loads(c3["comparacao"].read_text(encoding="utf-8"))
    assert gravado == comparacao, "o JSON gravado difere do dicionário devolvido"

    texto_md = c3["comparacao_md"].read_text(encoding="utf-8")
    separadores = [linha for linha in texto_md.splitlines() if linha.startswith("|---")]
    # 5 tabelas do briefing + as 2 de acurácia balanceada (90 e 36) da onda final.
    assert len(separadores) == 7, separadores
    assert "None" not in texto_md, "valor ausente vazou como 'None' em vez de '—'"

    # Fix round 1, item 1: a Tabela 3 (Custo e prolixidade) negrita o MENOR s/caso e o MENOR
    # tokens de saída da linha -- aqui nenhum dos dois está na primeira coluna (2-A), então a
    # linha só sai certa se o negrito acompanhar o valor, não a posição.
    linha_custo = [linha for linha in texto_md.splitlines()
                  if linha.startswith(f"| {_MODELO_AVAL} |") and " s / " in linha][0]
    assert "**30,0** s" in linha_custo, linha_custo
    assert "**50** tok" in linha_custo, linha_custo
    assert "**50,0** s" not in linha_custo, linha_custo  # 2-A (50,0 s) não é o menor
    assert "**100** tok" not in linha_custo, linha_custo  # 2-A (100 tok) não é o menor


def teste_comparar_fases_negrito_e_p() -> None:
    """Fix round 1 da Tarefa 9 (itens 1-3): _com_negrito com direção 'menor' acha o mínimo
    onde ele estiver na lista, não só na primeira posição; _p formata p-valor com 4 casas e
    '*' colado quando p < 0,05 (a mesma convenção de avaliar.py); e _melhor_f3 desempata
    escolhendo a MENOR época quando duas têm o mesmo acerto (a ordem de iteração é 0..3 e
    max() preserva o primeiro máximo)."""
    textos = comparar_fases._com_negrito(
        [("10,0", 10.0), ("2,0", 2.0), ("5,0", 5.0)], direcao="menor")
    assert textos == ["10,0", "**2,0**", "5,0"], textos
    textos_maior = comparar_fases._com_negrito(
        [("10,0", 10.0), ("2,0", 2.0), ("5,0", 5.0)], direcao="maior")
    assert textos_maior == ["**10,0**", "2,0", "5,0"], textos_maior
    # empate: os dois lados do empate saem em negrito.
    empate = comparar_fases._com_negrito([("1", 1.0), ("1", 1.0), ("2", 2.0)],
                                         direcao="menor")
    assert empate == ["**1**", "**1**", "2"], empate

    assert comparar_fases._p(0.002) == "0,0020*", comparar_fases._p(0.002)
    assert comparar_fases._p(0.1221) == "0,1221", comparar_fases._p(0.1221)
    assert comparar_fases._p(0.05) == "0,0500", comparar_fases._p(0.05)  # não < 0,05: sem *
    assert comparar_fases._p(None) == "—", comparar_fases._p(None)

    # O desempate é sobre a acurácia balanceada (critério de 'F3 melhor' desde a onda final).
    melhor = comparar_fases._melhor_f3(
        {0: {"acerto_pct": 70.0, "acuracia_balanceada_pct": 60.0},
         1: {"acerto_pct": 70.0, "acuracia_balanceada_pct": 60.0},
         2: {"acerto_pct": 50.0, "acuracia_balanceada_pct": 40.0}})
    assert melhor["biblioteca_epoca"] == 0, melhor


def _resumo_fase3_grafico_sintetico(modelos: list[str]) -> dict:
    """resumo_fase3.json mínimo para exercitar as figuras 12-15 da Tarefa 10 -- 2 modelos, 4
    versões de biblioteca (L0..L3): acerto crescente por época nas duas partições,
    recuperação (hit@3/mrr) subindo devagar e uma proposta por época com uma rejeição e um
    acréscimo de tokens. Só os três blocos que gerar_graficos_fase3 lê
    (por_modelo_biblioteca_particao, recuperacao, documentacao) -- os demais blocos de
    resumo_fase3.json (pareado_vs_L0, cochran_q etc.) não têm figura nesta tarefa."""
    por_modelo_biblioteca_particao, recuperacao, documentacao = [], [], []
    for i, modelo in enumerate(modelos):
        # tokens começa igual para todos (a cópia de L0 é idêntica em toda a corrida -- ver
        # docstring de fig_15) e só o CRESCIMENTO por época varia por modelo. O tamanho
        # renderizado de cada versão (tokens_estimados/chars, do fechamento.json) vai no
        # bloco 'recuperacao', que tem uma linha por versão L0..L3 -- é de lá que a figura
        # 15 lê, e não do acréscimo em bytes crus do diff.
        tokens = 4000
        for epoca in range(4):
            if epoca:
                tokens += 300 + epoca * 50 + i * 20
            por_modelo_biblioteca_particao.append({
                "modelo": modelo, "biblioteca_epoca": epoca, "particao": "avaliacao",
                "causa_correta_pct": round(50.0 + epoca * 8 + i * 2, 1)})
            por_modelo_biblioteca_particao.append({
                "modelo": modelo, "biblioteca_epoca": epoca, "particao": "aprendizado",
                "causa_correta_pct": round(55.0 + epoca * 5 - i * 3, 1)})
            recuperacao.append({
                "modelo": modelo, "biblioteca_epoca": epoca,
                "tokens_estimados": tokens, "chars": round(tokens * 2.6),
                "avaliacao": {"hit@3": round(60.0 + epoca * 6 + i * 1.5, 1),
                             "mrr": round(0.50 + epoca * 0.05 + i * 0.01, 2)},
                "todos": {"hit@3": round(58.0 + epoca * 6 + i * 1.5, 1),
                         "mrr": round(0.48 + epoca * 0.05 + i * 0.01, 2)}})
        for epoca in (1, 2, 3):
            documentacao.append({
                "modelo": modelo, "epoca": epoca, "n_propostas": 18, "n_aceitas": 12,
                "n_nenhuma": 2,
                "motivos_rejeicao": {"sem_bloco": 1 if epoca == 1 else 0,
                                    "copia_do_caso": 2 if epoca == 2 else 0,
                                    "texto_curto": 0},
                "tokens_md_estimados_acrescentados": round((300 + epoca * 50 + i * 20) * 2.5)})
    return {"por_modelo_biblioteca_particao": por_modelo_biblioteca_particao,
            "recuperacao": recuperacao, "documentacao": documentacao}


def _comparacao_fases_grafico_sintetica(modelos: list[str]) -> dict:
    """comparacao_fases.json mínimo para as figuras 16-17 da Tarefa 10 -- 2 modelos, as 5
    colunas de nos_90 que a Tabela de comparação usa (2A_linear_ryzen, 2B_A0, 2B_A2, F3_L0,
    F3_L3), com a coluna 2A_linear_ryzen do segundo modelo ausente (None) de propósito, para
    exercitar o 'sem dado' que a figura 16 precisa desenhar quando um modelo não tem aquela
    fase."""
    por_modelo = {}
    for i, modelo in enumerate(modelos):
        colunas = {
            "2A_linear_ryzen": {"acerto_pct": 40.0 + i * 2, "segundos_mediana": 50.0 + i * 5},
            "2B_A0": {"acerto_pct": 45.0 + i * 2, "segundos_mediana": 42.0 + i * 4},
            "2B_A2": {"acerto_pct": 60.0 + i * 2, "segundos_mediana": 38.0 + i * 3},
            "F3_L0": {"acerto_pct": 58.0 + i * 2, "segundos_mediana": 36.0 + i * 3},
            "F3_L3": {"acerto_pct": 70.0 + i * 2, "segundos_mediana": 34.0 + i * 2},
        }
        if i == 1:
            colunas["2A_linear_ryzen"] = None
        por_modelo[modelo] = {"nos_90": colunas}
    return {"por_modelo": por_modelo}


def _gerar_e_conferir_graficos(gg, gg3, resumo: dict, comparacao: dict, pasta: Path) -> None:
    """Gera as 6 figuras (fig_12..fig_17) numa pasta temporária e confere que os 12 arquivos
    (PNG + SVG) saem em disco com tamanho > 0 -- usada duas vezes por teste_graficos_fase3,
    uma com 2 modelos (grade 1x2 nas figuras 12/14) e outra com 4 (grade 2x2), para as duas
    formas de _grade_paineis serem exercitadas."""
    destino = pasta / "graficos"
    gg.GRAFICOS = destino
    gg3.fig_12(resumo)
    gg3.fig_13(resumo)
    gg3.fig_14(resumo)
    gg3.fig_15(resumo)
    gg3.fig_16(comparacao)
    gg3.fig_17(comparacao)

    arquivos = sorted(destino.iterdir()) if destino.exists() else []
    assert len(arquivos) == 12, arquivos
    for arquivo in arquivos:
        assert arquivo.stat().st_size > 0, arquivo


def teste_graficos_fase3() -> None:
    """Gera as 6 figuras da Fase 3 (12-17) sobre dados sintéticos de 4 versões de biblioteca,
    uma vez com 2 modelos e outra com os 4 da corrida oficial, e confere que os 12 arquivos
    (PNG + SVG) de cada corrida saem em disco com tamanho > 0. O import de matplotlib e do
    módulo gerar_graficos_fase3 fica DENTRO do teste, depois do try/except -- o Python padrão
    do PATH não tem matplotlib instalado (só a venv ..\\.venv\\Scripts\\python.exe tem), e um
    import de topo do módulo quebraria o runner inteiro (ImportError antes de qualquer teste
    rodar) para quem executa `python testar_fase3.py` sem a venv. Quando falta o pacote, o
    teste imprime o aviso e passa em vez de falhar -- é o comportamento descrito no briefing
    da Tarefa 10.

    Fix round 1 (revisão da Tarefa 10): a corrida com 2 modelos sozinha não bastava -- ela só
    exercita _grade_paineis com 1 linha de painéis (as figuras 12 e 14), e o defeito de
    título/subtítulo da figura colidindo com o título do painel (_titular_fig calculava a
    margem do topo numa fração FIXA da figura, e a altura da figura muda com o número de
    linhas de _grade_paineis) só aparecia com 2 linhas, isto é, com os 4 modelos da corrida
    oficial. A segunda chamada, com esses 4 modelos, cobre o caminho que faltava."""
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        print("teste_graficos_fase3: pulado (sem matplotlib nesta venv)")
        return

    import gerar_graficos as gg
    import gerar_graficos_fase3 as gg3

    modelos_2 = ["modelo-zero", "modelo-um"]
    _gerar_e_conferir_graficos(gg, gg3, _resumo_fase3_grafico_sintetico(modelos_2),
                              _comparacao_fases_grafico_sintetica(modelos_2),
                              _pasta_temporaria())

    modelos_4 = ["qwen2.5-coder:3b", "qwen2.5:7b", "qwen2.5-coder:7b", "granite4.2:8b"]
    _gerar_e_conferir_graficos(gg, gg3, _resumo_fase3_grafico_sintetico(modelos_4),
                              _comparacao_fases_grafico_sintetica(modelos_4),
                              _pasta_temporaria())


# --------------------------------------------------------- Tarefa 11: relatório HTML

def teste_relatorio_fase3_sintetico() -> None:
    """Gera relatorio_fase3.html sobre a MESMA árvore sintética de
    teste_avaliar_fase3_sintetico (avaliacao_fase3.json e resumo_fase3.json precisam existir
    antes -- é o que avaliar_fase3.avaliar_saida grava) e confere: o arquivo existe; a seção
    de propostas e o id de um caso de aprendizado aparecem; o código de rejeição
    copia_do_caso (a única recusa da árvore sintética, no terceiro caso de aprendizado)
    aparece; o diff__E1 (gerado por evolucao_biblioteca.fechar_epoca, irmão de epoca-1/)
    aparece; e a resposta hostil (_RESPOSTA_PROPOSTA_HOSTIL, injetada na primeira proposta por
    _arvore_fase3_sintetica) aparece ESCAPADA -- comparada com html.escape() do próprio texto,
    não digitada à mão -- e NUNCA crua, porque o JSON embutido no <script> do relatório
    quebraria no meio ao encontrar um "</script>" literal vindo de dados."""
    c3 = _arvore_fase3_sintetica()
    avaliar_fase3.avaliar_saida(c3)
    destino = gerar_relatorio_fase3.gerar_relatorio(c3)

    assert destino is not None and destino.exists(), destino
    texto = destino.read_text(encoding="utf-8")
    assert "Propostas" in texto

    particao = evo.particionar(CASOS + CASOS_EXTRA)
    caso_aprendizado = next(c for c in CASOS + CASOS_EXTRA
                            if evo.particao_de(particao, c["id"]) == "aprendizado")
    assert caso_aprendizado["id"] in texto, caso_aprendizado["id"]

    assert "copia_do_caso" in texto
    assert "diff__E1" in texto

    escapado = html.escape(_RESPOSTA_PROPOSTA_HOSTIL)
    assert escapado in texto, "resposta hostil não apareceu escapada no relatório"
    assert "<script>alert(1)</script>" not in texto, \
        "a resposta hostil apareceu CRUA no relatório -- o <script> de dados quebraria"


# ------------------------------------------ onda final de correções (12/09/2026)
# ! Alteração de IA - Revisar: testes da onda final de correções da Fase 3 — os itens do
# livro-razão adiados (tags, truncada por bloco, arquivo novo qualquer, is_file, guarda no
# finally, campo_mostrado, amostra de revisão por época, placeholders do relatório, média
# por coluna) e os achados da revisão final de código (TRECHO entre aspas, índice de arquivos
# fora de resultados*/base_conhecimento, endpoint com query string, unidades da figura 15,
# versão do Ollama em todo registro, acurácia balanceada no Markdown, TITULO entre colchetes,
# tbody, SISTEMA com os dois sistemas, gravação atômica, projeção por número de épocas e os
# rótulos da figura 17).
# ! Motivo: cada teste abaixo reproduz primeiro o defeito visto no piloto de 10 casos ou
# apontado pela revisão (ex.: as duas retificações do qwen2.5-coder:3b recusadas como
# trecho_nao_encontrado só por causa das aspas; um bloco completo recusado como "sem FIM"
# porque o bloco SEGUINTE foi cortado; pagina-produtos-api.md resolvido como "ambíguo: 3
# arquivos" porque o índice de nomes varria as cópias de resultados_alvo/) e só depois a
# correção entra — a regra de TDD do harness. Os textos de TRECHO são os exatos do piloto
# (resultados_alvo/fase3_piloto/qwen2.5-coder_3b/propostas__E1.jsonl, casos lex-2 e lex-5).

def teste_notas_malformadas_e_secoes_base() -> None:
    """bib.notas_malformadas devolve o número (entre as linhas não vazias da seção) de cada
    nota que não casa com NOTA_RE -- é a mesma contagem que validar() imprime em 'nota
    malformada na linha N', agora num lugar só; e _SECOES_BASE é a tupla explícita das
    quatro seções escritas à mão, sem depender de filtrar bib.SECOES em tempo de import."""
    ok = _campo_ausente_com(_NOTAS_EXEMPLO)
    assert bib.notas_malformadas(ok) == [], bib.notas_malformadas(ok)
    ruim = _campo_ausente_com(_NOTAS_EXEMPLO + "\n- nota solta sem formato\n")
    assert bib.notas_malformadas(ruim) == [3], bib.notas_malformadas(ruim)
    probs = [p for p in bib.validar([ruim], [], teto_global=None)
             if "nota malformada" in p]
    assert probs == ["erros/campo_ausente.md: nota malformada na linha 3 da seção "
                     "'Notas do modelo'"], probs
    sem_secao = _campo_ausente_com("")
    assert bib.notas_malformadas(sem_secao) == []

    assert recuperacao._SECOES_BASE == ("Resumo", "Sinais", "Causa", "Como confirmar"), \
        recuperacao._SECOES_BASE
    assert isinstance(recuperacao._SECOES_BASE, tuple)


def teste_parser_truncada_so_no_ultimo_bloco() -> None:
    """A resposta cortada pelo teto de tokens só invalida o ÚLTIMO bloco sem FIM: um bloco
    fechado pela PROPOSTA seguinte está completo, aconteça o que acontecer depois dele."""
    resposta = (
        "PROPOSTA 1\n"
        "OPERACAO: nota\n"
        "VERBETE: x\n"
        "TEXTO: bloco completo que esqueceu o FIM\n"
        "MOTIVO: motivo do bloco 1\n"
        "PROPOSTA 2\n"
        "OPERACAO: nota\n"
        "VERBETE: y\n"
        "TEXTO: bloco cort"
    )
    r = evo.parsear_propostas(resposta, tokens_saida=700, max_tokens=700)
    assert r["truncada"] is True, r
    assert len(r["blocos"]) == 2, r["blocos"]
    assert r["blocos"][0]["malformado"] is None, r["blocos"][0]
    assert r["blocos"][0]["fim_ausente"] is True, r["blocos"][0]
    assert r["blocos"][1]["malformado"] == "sem FIM", r["blocos"][1]
    assert r["blocos"][1]["fim_ausente"] is True, r["blocos"][1]

    # Sem corte, os dois blocos passam pela conferência de campos: o segundo falta MOTIVO.
    r2 = evo.parsear_propostas(resposta, tokens_saida=200, max_tokens=700)
    assert r2["blocos"][0]["malformado"] is None, r2["blocos"][0]
    assert r2["blocos"][1]["malformado"] == "falta MOTIVO", r2["blocos"][1]


def teste_somente_acrescimo_arquivo_novo_qualquer() -> None:
    """Qualquer arquivo novo fora de aprendidos/ (não só .md) é violação do invariante de
    somente-acréscimo; dentro de aprendidos/ só entra verbete .md; INDICE.md,
    fechamento.json e os diff__* gerados pelo próprio fechamento não contam."""
    tmp, ctx = _ambiente_proposta()
    raiz, antiga = ctx["raiz"], tmp / "epoca-0"

    (raiz / "erros" / "intruso.txt").write_text("x", encoding="utf-8")
    violacoes = evo.conferir_somente_acrescimo(antiga, raiz)
    assert "erros/intruso.txt: arquivo novo fora de aprendidos/" in violacoes, violacoes

    (raiz / "erros" / "intruso.txt").unlink()
    (raiz / "aprendidos").mkdir(exist_ok=True)
    (raiz / "aprendidos" / "solto.txt").write_text("x", encoding="utf-8")
    violacoes = evo.conferir_somente_acrescimo(antiga, raiz)
    assert any(v.startswith("aprendidos/solto.txt:") for v in violacoes), violacoes

    (raiz / "aprendidos" / "solto.txt").unlink()
    (raiz / "INDICE.md").write_text("# indice\n", encoding="utf-8")
    (raiz / "fechamento.json").write_text("{}", encoding="utf-8")
    (raiz / "diff__E1.md").write_text("# diff\n", encoding="utf-8")
    assert evo.conferir_somente_acrescimo(antiga, raiz) == [], \
        evo.conferir_somente_acrescimo(antiga, raiz)


def teste_resolver_arquivo_exige_arquivo_e_ignora_resultados() -> None:
    """_resolver_arquivo só aceita caminho completo que seja ARQUIVO (uma pasta como
    'Programacao' não é referência de código), e o índice de nomes não varre as cópias da
    biblioteca em resultados*/ (os snapshots epoca-* de cada modelo), nem graficos/,
    .superpowers/ e base_conhecimento/ (verbete não é código): no piloto,
    pagina-produtos-api.md resolvia como 'ambíguo: 3 arquivos' e o veredito dependia de
    quantas pastas epoca-* existiam quando o processo começou."""
    resolvido, erro = evo._resolver_arquivo("Programacao")
    assert resolvido is None, (resolvido, erro)

    raiz_falsa = _pasta_temporaria()
    for rel in ("Programacao/CobaiaFront/conn/connect.php",
                "Programacao/AgenteCore/experimentos/resultados_alvo/fase3/bibliotecas/m/"
                "epoca-0/x/connect.php",
                "Programacao/AgenteCore/experimentos/resultados/fase3/y/connect.php",
                "Programacao/AgenteCore/experimentos/resultados_piloto/z/connect.php",
                "Programacao/AgenteCore/experimentos/graficos/connect.php",
                "Programacao/AgenteCore/base_conhecimento/negocio/pagina-produtos-api.md",
                "Programacao/AgenteCore/experimentos/resultados_alvo/fase3/bibliotecas/m/"
                "epoca-1/negocio/pagina-produtos-api.md"):
        (raiz_falsa / rel).parent.mkdir(parents=True, exist_ok=True)
        (raiz_falsa / rel).write_text("x", encoding="utf-8")
    raiz_original, cache_original = bib.RAIZ_REPO, evo._basenames_repo
    try:
        bib.RAIZ_REPO = raiz_falsa
        evo._basenames_repo = None
        assert evo._resolver_arquivo("connect.php") == \
            ("Programacao/CobaiaFront/conn/connect.php", ""), evo._resolver_arquivo("connect.php")
        resolvido, erro = evo._resolver_arquivo("pagina-produtos-api.md")
        assert resolvido is None and "não existe" in erro, (resolvido, erro)
        resolvido, erro = evo._resolver_arquivo("Programacao/CobaiaFront/conn")
        assert resolvido is None, (resolvido, erro)
    finally:
        bib.RAIZ_REPO = raiz_original
        evo._basenames_repo = cache_original
    for pasta in ("resultados", "resultados_alvo", "resultados_piloto", ".superpowers",
                  "graficos", "base_conhecimento"):
        assert pasta in evo.PASTAS_IGNORADAS_REPO, pasta


# Os dois TRECHO exatos que o qwen2.5-coder:3b escreveu no piloto (propostas__E1.jsonl,
# casos lex-2 e lex-5), recusados como trecho_nao_encontrado só por causa das aspas.
_TRECHOS_DO_PILOTO = (
    ("corpo_nao_e_json", '"o parse falha no primeiro caractere"'),
    ("resposta_truncada", '"o modo malformed_json devolve corpo cortado de propósito"'),
)
_TEXTO_RETIFICACAO = ("Quando o corpo comeca com uma tag ou um aviso em texto, o parse do "
                      "JSON para logo no primeiro caractere e a tela nao recebe dado nenhum")
_MOTIVO_RETIFICACAO = "o verbete falava do parse sem dizer o que a tela mostra nesse caso"


def teste_trecho_com_aspas_delimitadoras() -> None:
    """TRECHO entre aspas (\" \", ' ', “ ”, « ») é comparado SEM as aspas delimitadoras: as
    duas retificações do piloto passam a ser aceitas e o trecho guardado sai sem elas. O
    mínimo de 15 caracteres vale para o trecho já sem aspas."""
    _tmp, ctx = _ambiente_proposta()
    ctx["ids_visiveis"] = set(ctx["ids_visiveis"]) | {"corpo_nao_e_json", "resposta_truncada"}
    for verbete, trecho in _TRECHOS_DO_PILOTO:
        r = evo.validar_proposta(_bloco(OPERACAO="retificacao", VERBETE=verbete,
                                        TRECHO=trecho, TEXTO=_TEXTO_RETIFICACAO,
                                        MOTIVO=_MOTIVO_RETIFICACAO), ctx)
        assert r["aceita"] is True, (verbete, r)
        assert r["edicao"]["trecho"] == trecho.strip('"'), r["edicao"]

    for aspas in ("“%s”", "'%s'", "«%s»"):
        r = evo.validar_proposta(_bloco(
            OPERACAO="retificacao", VERBETE="corpo_nao_e_json",
            TRECHO=aspas % "o parse falha no primeiro caractere",
            TEXTO=_TEXTO_RETIFICACAO, MOTIVO=_MOTIVO_RETIFICACAO), ctx)
        assert r["aceita"] is True, (aspas, r)
        assert r["edicao"]["trecho"] == "o parse falha no primeiro caractere", r["edicao"]

    # 16 caracteres com as aspas, 14 sem: continua curto demais.
    r = evo.validar_proposta(_bloco(OPERACAO="retificacao", VERBETE="corpo_nao_e_json",
                                    TRECHO='"parse falha no"', TEXTO=_TEXTO_RETIFICACAO,
                                    MOTIVO=_MOTIVO_RETIFICACAO), ctx)
    assert r["motivo"] == "retificacao_sem_trecho", r


def teste_endpoint_citado_com_query_string() -> None:
    """Endpoint citado no TEXTO com query string (GET /api/pedidos?login=...) ou entre
    parênteses é comparado só pela rota, do mesmo jeito que recuperacao.sinais_do_caso lê a
    requisição do caso; rota inexistente continua recusada, sem a query no detalhe."""
    _tmp, ctx = _ambiente_proposta()
    r = evo.validar_proposta(_bloco(
        TEXTO="A chamada GET /api/pedidos?login=11122233344 devolve a lista do usuario e a "
              "tela (GET /api/produtos/7) imprime undefined quando o preco nao vem"), ctx)
    assert r["aceita"] is True, r

    r2 = evo.validar_proposta(_bloco(
        TEXTO="A chamada GET /api/clientes?login=11122233344 devolve a lista do usuario e "
              "o botao de detalhe imprime undefined quando o preco nao vem"), ctx)
    assert r2["motivo"] == "endpoint_inexistente", r2
    assert "GET /api/clientes" in r2["detalhe"] and "?" not in r2["detalhe"], r2["detalhe"]


def teste_titulo_sistema_e_tbody_do_piloto() -> None:
    """Três formas vistas no piloto: TITULO entre colchetes ('[Campo ausente]', que viraria
    lista no frontmatter e derrubaria bib.validar), SISTEMA com os dois sistemas
    ('CobaiaFront, CobaiaAPI', que é 'Ambos') e a palavra tbody no TEXTO (elemento HTML,
    não tabela do banco). SINTOMAS com apóstrofo continua palavra_chave_invalida — de
    propósito: o item vira nome de arquivo/lista do frontmatter. ORCAMENTO_PROMPT_PROP
    (nunca lido) deixa de existir."""
    _tmp, ctx = _ambiente_proposta()
    novo = {"OPERACAO": "novo_verbete", "VERBETE": "campo-ausente-no-botao",
            "CAUSAS": "campo_ausente"}
    r = evo.validar_proposta(_bloco(**novo, TITULO="[Campo ausente]"), ctx)
    assert r["aceita"] is True, r
    assert r["edicao"]["novo"]["titulo"] == "Campo ausente", r["edicao"]["novo"]
    # Dois pares ('[[Campo ausente]]'): a re-revisão da onda final mostrou que tirar um par
    # só deixava 'titulo: [Campo ausente]' no frontmatter, relido como lista por
    # bib._parse_frontmatter e derrubando bib.validar com TypeError na época seguinte.
    r1b = evo.validar_proposta(_bloco(**novo, TITULO="[[Campo ausente]]"), ctx)
    assert r1b["aceita"] is True, r1b
    assert r1b["edicao"]["novo"]["titulo"] == "Campo ausente", r1b["edicao"]["novo"]
    # Só colchetes ('[]'): título vazio nunca chega ao frontmatter.
    r1c = evo.validar_proposta(_bloco(**novo, TITULO="[]"), ctx)
    assert r1c["aceita"] is False, r1c

    r2 = evo.validar_proposta(_bloco(**novo, TITULO="Campo ausente",
                                     SISTEMA="CobaiaFront, CobaiaAPI"), ctx)
    assert r2["aceita"] is True, r2
    assert r2["edicao"]["novo"]["sistema"] == "Ambos", r2["edicao"]["novo"]
    r3 = evo.validar_proposta(_bloco(**novo, TITULO="Campo ausente",
                                     SISTEMA="CobaiaFront, Mainframe"), ctx)
    assert r3["motivo"] == "vocabulario", r3
    r4 = evo.validar_proposta(_bloco(**novo, TITULO="Campo ausente", SISTEMA="CobaiaAPI"),
                              ctx)
    assert r4["edicao"]["novo"]["sistema"] == "CobaiaAPI", r4

    r5 = evo.validar_proposta(_bloco(
        TEXTO="O cartao e montado dentro do tbody da tabela da tela inicial e, quando o "
              "preco nao vem, o botao de detalhe imprime undefined"), ctx)
    assert r5["aceita"] is True, r5
    assert "tbody" in evo.TABELAS_EXCECOES, evo.TABELAS_EXCECOES
    r6 = evo.validar_proposta(_bloco(
        TEXTO="O preco sai da tabela tbclientes da tela inicial e, quando ele nao vem, o "
              "botao de detalhe imprime undefined na tela"), ctx)
    assert r6["motivo"] == "tabela_inexistente", r6

    r7 = evo.validar_proposta(
        _bloco(SINTOMAS="A página fica em 'Carregando produtos' indefinidamente."), ctx)
    assert r7["motivo"] == "palavra_chave_invalida", r7

    assert not hasattr(evo, "ORCAMENTO_PROMPT_PROP"), "constante morta ainda existe"


def teste_gravacao_atomica_e_versao_no_fechamento() -> None:
    """fechamento.json (e maquina.json, via a mesma função) é gravado num .tmp e trocado
    com os.replace: uma queda no meio da gravação deixa o arquivo antigo inteiro, nunca um
    JSON pela metade que snapshot_fechado() tomaria por época fechada. E o fechamento passa
    a registrar a versão do Ollama que produziu a época."""
    tmp = _pasta_temporaria()
    destino = tmp / "x.json"
    evo._gravar_json_atomico(destino, {"a": "é"})
    assert json.loads(destino.read_text(encoding="utf-8")) == {"a": "é"}
    evo._gravar_json_atomico(destino, {"a": 2})
    assert json.loads(destino.read_text(encoding="utf-8")) == {"a": 2}
    assert sorted(p.name for p in tmp.iterdir()) == ["x.json"], sorted(tmp.iterdir())

    raiz = evo.copiar_biblioteca(bib.BASE, tmp / "b")
    fech = evo.fechar_snapshot(raiz, 1, "modelo-x", 0, versao_ollama="0.34.0")
    assert fech["versao_ollama"] == "0.34.0", fech
    gravado = json.loads((raiz / "fechamento.json").read_text(encoding="utf-8"))
    assert gravado["versao_ollama"] == "0.34.0", gravado
    assert not any(p.suffix == ".tmp" for p in raiz.iterdir()), sorted(raiz.iterdir())
    sem_versao = evo.fechar_snapshot(raiz, 1, "modelo-x", 0)
    assert sem_versao["versao_ollama"] is None, sem_versao


def teste_executor_finally_nao_mascara_a_parada() -> None:
    """Se o Ollama caiu, o descarregamento e a conferência de residentes no finally de
    rodar_modelo_fase3 também falham — e essa segunda falha não pode substituir o SystemExit
    das três tentativas esgotadas, que é o que main() captura para imprimir '!! modelo
    parou' e seguir para o próximo modelo."""
    casos = _casos_do_piloto(2)
    particao = evo.particionar(CASOS + CASOS_EXTRA)
    c3 = _c3_temporario("fase3_finally")
    chamadas: list = []
    stubs = _ollama_de_mentira(casos, {}, chamadas, falhar_sempre=True)

    def _caiu(*args, **kwargs):
        raise ConnectionError("Ollama fora do ar (de mentira)")

    stubs["descarregar"] = _caiu
    stubs["um_modelo_por_vez"] = _caiu
    try:
        _com_stubs(stubs, lambda: executar_fase3.rodar_modelo_fase3(
            _MODELO_DE_MENTIRA, casos, particao, 1, 3, 600, 700, c3))
        assert False, "três tentativas falhas deveriam levantar SystemExit"
    except SystemExit as e:
        assert casos[0]["id"] in str(e), str(e)
    except ConnectionError as e:
        assert False, f"o finally mascarou o SystemExit com {e!r}"


def teste_executor_campo_mostrado_e_versao_ollama() -> None:
    """campo_mostrado guarda o que o prompt de proposta MOSTROU ('nenhum' quando o gabarito
    não tem campo afetado, igual a estrategias.proposta_de_edicao); todo registro e todo
    fechamento.json levam versao_ollama; e relançar com o Ollama noutra versão da gravada em
    maquina.json para o modelo antes de qualquer inferência, dizendo as duas versões."""
    casos = _casos_do_piloto(6)
    particao = evo.particionar(CASOS + CASOS_EXTRA)
    c3 = _c3_temporario("fase3_versao")
    _rodar(c3, casos, particao, {})
    pasta = c3["raiz"] / _SLUG_DE_MENTIRA
    pasta_bib = c3["bibliotecas"] / _SLUG_DE_MENTIRA
    por_id = {c["id"]: c for c in casos}

    propostas = executar_bateria.ler_jsonl(pasta / "propostas__E1.jsonl")
    assert propostas, "os 6 primeiros casos precisam ter ao menos um de aprendizado"
    for p in propostas:
        esperado = por_id[p["caso"]]["gabarito"]["campo_afetado"] or "nenhum"
        assert p["campo_mostrado"] == esperado, (p["caso"], p["campo_mostrado"], esperado)
        assert f"CAMPO AFETADO: {esperado}" in p["prompt"], p["caso"]
    assert any(p["campo_mostrado"] == "nenhum" for p in propostas), \
        [p["campo_mostrado"] for p in propostas]

    for nome in ("diagnosticos__L0.jsonl", "propostas__E1.jsonl", "diagnosticos__L1.jsonl"):
        registros = executar_bateria.ler_jsonl(pasta / nome)
        assert registros, nome
        for r in registros:
            assert r["versao_ollama"] == "0.0.0-teste", (nome, r.get("versao_ollama"))
    for epoca in (0, 1):
        fech = json.loads((pasta_bib / f"epoca-{epoca}" / "fechamento.json").read_text(
            encoding="utf-8"))
        assert fech["versao_ollama"] == "0.0.0-teste", (epoca, fech)

    c3["maquina"].write_text(json.dumps({"ollama": "9.9.9", "inicio": "2026-09-12T00:00:00"}),
                             encoding="utf-8")
    chamadas_antes = None
    try:
        chamadas_antes = _rodar(c3, casos, particao, {})
        assert False, "Ollama noutra versão da de maquina.json deveria levantar SystemExit"
    except SystemExit as e:
        assert "9.9.9" in str(e) and "0.0.0-teste" in str(e), str(e)
    assert chamadas_antes is None


def teste_atualizar_maquina_preserva_inicio() -> None:
    """maquina.json guarda o início e a versão do Ollama da PRIMEIRA execução; cada relance
    entra em 'relances' (início e versão de cada um), sem sobrescrever os originais."""
    tmp = _pasta_temporaria()
    caminho = tmp / "maquina.json"
    primeiro = executar_fase3.atualizar_maquina(caminho, {
        "hostname": "h", "ollama": "0.33.3", "inicio": "2026-09-12T10:00:00", "saida": "f"})
    assert primeiro["inicio"] == "2026-09-12T10:00:00" and "relances" not in primeiro, primeiro
    segundo = executar_fase3.atualizar_maquina(caminho, {
        "hostname": "h", "ollama": "0.34.0", "inicio": "2026-09-13T08:00:00", "saida": "f"})
    assert segundo["inicio"] == "2026-09-12T10:00:00", segundo
    assert segundo["ollama"] == "0.33.3", segundo
    assert segundo["relances"] == [{"inicio": "2026-09-13T08:00:00", "ollama": "0.34.0"}], \
        segundo
    terceiro = executar_fase3.atualizar_maquina(caminho, {
        "hostname": "h", "ollama": "0.34.0", "inicio": "2026-09-14T08:00:00", "saida": "f"})
    assert len(terceiro["relances"]) == 2, terceiro
    assert json.loads(caminho.read_text(encoding="utf-8")) == terceiro
    assert sorted(p.name for p in tmp.iterdir()) == ["maquina.json"], sorted(tmp.iterdir())
    # Primeira execução sem versão (GET /api/version falhou no instante de maquina_atual,
    # _versao_ollama devolve None): o relance preenche a versão e o início originais em vez
    # de manter null para sempre — senão _conferir_versao_ollama nunca teria base.
    tmp2 = _pasta_temporaria()
    caminho2 = tmp2 / "maquina.json"
    executar_fase3.atualizar_maquina(caminho2, {"hostname": "h", "ollama": None,
                                                "inicio": None, "saida": "f"})
    depois = executar_fase3.atualizar_maquina(caminho2, {
        "hostname": "h", "ollama": "0.34.0", "inicio": "2026-09-13T08:00:00", "saida": "f"})
    assert depois["ollama"] == "0.34.0", depois
    assert depois["inicio"] == "2026-09-13T08:00:00", depois


def teste_projecao_por_epocas() -> None:
    """A projeção de tempo conta epocas+1 passadas de diagnóstico e epocas de proposta —
    o piloto (1 época) não pode ser projetado como se fossem 3."""
    tres = executar_fase3.projecao_tempo(["qwen2.5-coder:3b"], 10, 6, epocas=3)
    uma = executar_fase3.projecao_tempo(["qwen2.5-coder:3b"], 10, 6, epocas=1)
    assert tres["passadas_diagnostico"] == 4 and tres["passadas_proposta"] == 3, tres
    assert uma["passadas_diagnostico"] == 2 and uma["passadas_proposta"] == 1, uma
    assert uma["total_h"] < tres["total_h"], (uma, tres)
    padrao = executar_fase3.projecao_tempo(["qwen2.5-coder:3b"], 10, 6)
    assert padrao["total_h"] == tres["total_h"], (padrao, tres)


def teste_amostra_revisao_por_epoca_e_holm() -> None:
    """A amostra da planilha de revisão continua determinística, mas a chave inclui a época:
    a ordem de aceitação recomeça em 1 a cada época, então sem a época as três épocas
    sorteariam sempre as MESMAS posições. E holm arredonda só na saída."""
    historico = [{"epoca": e, "ordem": o, "operacao": "nota", "caso": f"c{o}",
                  "verbete": "v", "texto": "t", "motivo": "m"}
                 for e in (1, 2) for o in range(1, 21)]
    escolhidas = avaliar_fase3.amostrar_edicoes(historico, "modelo:x", por_epoca=10)
    assert len(escolhidas) == 20, len(escolhidas)
    assert escolhidas == avaliar_fase3.amostrar_edicoes(historico, "modelo:x", por_epoca=10)
    ordens = {e: sorted(l["ordem"] for l in escolhidas if l["epoca"] == e) for e in (1, 2)}
    assert len(ordens[1]) == 10 and len(ordens[2]) == 10, ordens
    assert ordens[1] != ordens[2], ordens
    outro = avaliar_fase3.amostrar_edicoes(historico, "modelo:y", por_epoca=10)
    assert sorted(l["ordem"] for l in outro if l["epoca"] == 1) != ordens[1]

    assert avaliar_fase3.holm([0.00004, 0.00004, 0.00004]) == [0.0001, 0.0001, 0.0001], \
        avaliar_fase3.holm([0.00004, 0.00004, 0.00004])
    assert avaliar_fase3.holm([0.012345, 0.012346, 0.5]) == [0.037, 0.037, 0.5], \
        avaliar_fase3.holm([0.012345, 0.012346, 0.5])


def teste_avaliar_versao_sem_snapshot_e_conferidos() -> None:
    """Registro cujo biblioteca_versao não tem snapshot fechado deixa de cair em silêncio no
    sem snapshot: o resumo lista as versões sem snapshot (e o console avisa). E
    reconstrucao_ok só conta como 'conferido' o registro que foi de fato conferido."""
    c3 = _arvore_fase3_sintetica()
    arquivo = c3["raiz"] / _SLUG_AVAL / "diagnosticos__L1.jsonl"
    linhas = executar_bateria.ler_jsonl(arquivo)
    linhas[0]["biblioteca_versao"] = "000000000000"
    linhas[1]["caso"] = "caso-que-nao-existe"
    arquivo.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in linhas),
                       encoding="utf-8")
    _avaliados, resumo = avaliar_fase3.avaliar_saida(c3)
    assert resumo["metadados"]["versoes_sem_snapshot"] == ["000000000000"], \
        resumo["metadados"]
    rec_ok = resumo["reconstrucao_ok"][0]
    assert rec_ok["conferidos"] == 5 and rec_ok["ok"] == 5, rec_ok

    limpo = _arvore_fase3_sintetica()
    _avaliados, resumo_limpo = avaliar_fase3.avaliar_saida(limpo)
    assert resumo_limpo["metadados"]["versoes_sem_snapshot"] == [], resumo_limpo["metadados"]
    assert avaliar_fase3._mais_chars(None) == "—", avaliar_fase3._mais_chars(None)
    assert avaliar_fase3._mais_chars(12) == "+12 chars", avaliar_fase3._mais_chars(12)


def teste_relatorio_placeholder_literal_no_texto_do_modelo() -> None:
    """Texto do modelo que contenha um placeholder literal do template (__DADOS_DIAGNOSTICOS__,
    __DIFFS__) não pode ser substituído de novo: a troca dos placeholders é numa passada só,
    sobre o template, e nunca sobre o que já foi inserido."""
    c3 = _arvore_fase3_sintetica()
    arquivo = c3["raiz"] / _SLUG_AVAL / "propostas__E1.jsonl"
    linhas = executar_bateria.ler_jsonl(arquivo)
    linhas[0]["resposta"] = "texto do modelo com __DADOS_DIAGNOSTICOS__ e __DIFFS__ dentro"
    arquivo.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in linhas),
                       encoding="utf-8")
    avaliar_fase3.avaliar_saida(c3)
    texto = gerar_relatorio_fase3.gerar_relatorio(c3).read_text(encoding="utf-8")
    assert texto.count("__DADOS_DIAGNOSTICOS__") == 1, texto.count("__DADOS_DIAGNOSTICOS__")
    assert texto.count("__DIFFS__") == 1, texto.count("__DIFFS__")
    assert texto.count("var DADOS_DIAGNOSTICOS = ") == 1
    assert texto.count('"notas_no_contexto":') == 12, texto.count('"notas_no_contexto":')
    assert "__RAIZ__" not in texto and "__TABELA_RESUMO__" not in texto


def _col(v: float) -> dict:
    """Uma COL de comparar_fases._coluna reduzida ao que _tabela_acerto lê."""
    return {"acerto_pct": v, "ic95": [v - 5.0, v + 5.0], "acuracia_balanceada_pct": v - 10.0}


def teste_comparar_fases_media_por_coluna_e_balanceada() -> None:
    """O rodapé de média diz o N de cada coluna quando ele difere entre colunas (a média
    de 2-A/2-B inclui modelos sem Fase 3); a acurácia balanceada — a métrica primária —
    aparece no Markdown em tabelas próprias; e 'F3 melhor' é a época de maior acurácia
    balanceada, não de maior acerto."""
    vazio = {"biblioteca_epoca": None}
    por_modelo = {
        "a": {"nos_90": {"2A_linear_ryzen": _col(50.0), "2B_A0": _col(40.0),
                         "2B_A2": _col(60.0), "2B_A3": None, "F3_L0": _col(55.0),
                         "F3_L1": None, "F3_L2": None, "F3_L3": _col(65.0),
                         "F3_melhor": {"biblioteca_epoca": 3, **_col(65.0)}}},
        "b": {"nos_90": {"2A_linear_ryzen": None, "2B_A0": _col(30.0), "2B_A2": _col(50.0),
                         "2B_A3": None, "F3_L0": None, "F3_L1": None, "F3_L2": None,
                         "F3_L3": None, "F3_melhor": vazio}},
    }
    linhas = comparar_fases._tabela_acerto("t", por_modelo, "nos_90")
    rodape = linhas[-2]
    assert rodape.startswith("| **Média** |"), rodape
    assert "50,0% (1 modelo)" in rodape and "35,0% (2 modelos)" in rodape, rodape
    assert "55,0% (2 modelos)" in rodape, rodape

    so_a = {"a": por_modelo["a"]}
    rodape_igual = comparar_fases._tabela_acerto("t", so_a, "nos_90")[-2]
    assert rodape_igual.startswith("| **Média (1 modelo)** |"), rodape_igual
    assert "(1 modelo)" not in rodape_igual.split("|", 2)[2], rodape_igual

    balanceada = comparar_fases._tabela_acerto("t", por_modelo, "nos_90",
                                               metrica="acuracia_balanceada_pct")
    assert any("**55,0%**" in l or "55,0%" in l for l in balanceada), balanceada
    assert "IC" not in "".join(balanceada[2:]), balanceada

    melhor = comparar_fases._melhor_f3(
        {0: {"acerto_pct": 70.0, "acuracia_balanceada_pct": 40.0},
         3: {"acerto_pct": 60.0, "acuracia_balanceada_pct": 55.0}})
    assert melhor["biblioteca_epoca"] == 3, melhor

    fixture = _arvore_comparar_fases_sintetica()
    c3 = fixture["c3"]
    comparar_fases.gerar_comparacao(fixture["caminho_2a"], fixture["caminho_2b"], c3)
    texto_md = c3["comparacao_md"].read_text(encoding="utf-8")
    assert "balanceada" in texto_md, texto_md[:600]
    assert "Acurácia balanceada por modelo e fase (90 casos)" in texto_md
    assert "Acurácia balanceada por modelo e fase (36 casos de avaliação)" in texto_md


def _caixas_de(gg3, ancoras, larguras, altura):
    deslocamentos = gg3._espalhar_rotulos(ancoras, larguras, altura)
    return [gg3._caixa_rotulo(a, dx, dy, w, altura)
            for a, (dx, dy), w in zip(ancoras, deslocamentos, larguras)], deslocamentos


def teste_graficos_rotulos_fig17_nao_se_sobrepoem() -> None:
    """Os rótulos da figura 17 são posicionados um a um (em pontos tipográficos) escolhendo,
    entre os candidatos de deslocamento, o primeiro cuja caixa não cruza nenhuma caixa já
    posta nem nenhum marcador — no piloto, 'q2.5:7b · 2-B A0' saía por cima de
    'q2.5-coder:3b · F3 L0' e o aglomerado dos 1.5b ficava ilegível. Ponto isolado fica com o
    primeiro candidato (acima e à direita)."""
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        print("teste_graficos_rotulos_fig17_nao_se_sobrepoem: pulado (sem matplotlib)")
        return
    import gerar_graficos_fase3 as gg3

    ancoras = [(100.0, 100.0), (103.0, 101.0), (101.0, 97.0), (99.0, 103.0), (400.0, 400.0)]
    larguras = [80.0] * len(ancoras)
    caixas, deslocamentos = _caixas_de(gg3, ancoras, larguras, 9.0)
    assert len(caixas) == len(ancoras), caixas
    for i in range(len(caixas)):
        for j in range(i + 1, len(caixas)):
            assert not gg3._caixas_se_cruzam(caixas[i], caixas[j]), (i, j, caixas)
        for a in ancoras:
            marcador = (a[0] - 5.0, a[1] - 5.0, a[0] + 5.0, a[1] + 5.0)
            assert not gg3._caixas_se_cruzam(caixas[i], marcador), (i, a, caixas[i])
    assert deslocamentos[-1] == gg3.DESLOCAMENTOS_ROTULO[0], deslocamentos

    a, b = (0.0, 0.0, 10.0, 10.0), (5.0, 5.0, 15.0, 15.0)
    assert gg3._caixas_se_cruzam(a, b) and not gg3._caixas_se_cruzam(a, (10.0, 0.0, 20.0, 10.0))


def teste_graficos_fig15_le_tamanho_renderizado() -> None:
    """A figura 15 lê o tamanho RENDERIZADO de cada versão (tokens_estimados do
    fechamento.json, uma linha por versão em resumo['recuperacao']) -- L0 inclusive, sem
    subtrair o acréscimo em bytes crus do diff, que está noutra unidade."""
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        print("teste_graficos_fig15_le_tamanho_renderizado: pulado (sem matplotlib)")
        return
    import gerar_graficos_fase3 as gg3

    resumo = _resumo_fase3_grafico_sintetico(["modelo-zero", "modelo-um"])
    series = gg3._series_fig_15(resumo)
    assert sorted(series) == ["modelo-um", "modelo-zero"], series
    assert [e for e, _ in series["modelo-zero"]] == [0, 1, 2, 3], series["modelo-zero"]
    assert series["modelo-zero"][0][1] == 4000 and series["modelo-um"][0][1] == 4000, series
    assert series["modelo-zero"][3][1] > series["modelo-zero"][0][1], series["modelo-zero"]
    assert series["modelo-um"][3][1] > series["modelo-zero"][3][1], series
    so_documentacao = {"documentacao": [{"modelo": "x", "epoca": 1,
                                         "tokens_md_estimados_acrescentados": 5}]}
    assert gg3._series_fig_15(so_documentacao) == {}, gg3._series_fig_15(so_documentacao)


def main() -> None:
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj)
              and obj.__module__ == modulo.__name__]
    # ! Alteração de IA - Revisar: o laço dos testes passa a rodar dentro de try/finally que
    # apaga as pastas criadas por _pasta_temporaria().
    # ! Motivo: os testes novos gravam bibliotecas de mentira em %TEMP% e, sem essa limpeza,
    # uma falha (que sai por sys.exit(1) no meio do laço) deixaria as pastas para trás a cada
    # execução; o finally roda também no SystemExit.
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
