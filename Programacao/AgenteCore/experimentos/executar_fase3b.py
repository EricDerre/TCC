#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria executar_fase3b.py — a Fase 3-B, cinco modos de
# diagnóstico complementares à Fase 3 oficial (ponte, cruzada, texto_max, a5, ineditos), todos
# rodando SÓ a passada final (lê uma biblioteca fechada, grava diagnosticos__L<n>.jsonl, não
# propõe edição — exceto texto_max, que roda uma época real) sobre CÓPIAS dos snapshots da
# Fase 3 em pastas de saída novas, sem alterar executar_fase3.py nem
# resultados_alvo/fase3/.
# ! Motivo: a Fase 3 oficial mede 4 modelos x 3 épocas de aprendizado sobre os MESMOS 90 casos
# que geraram a biblioteca de cada um; isso não responde perguntas que misturariam dois
# efeitos na mesma medição — o Ollama 0.34.1 (instalado depois da corrida oficial em 0.34.0)
# reproduz os números (ponte)? o que um modelo escreve ajuda outro modelo, ou só ajuda quem
# escreveu (cruzada)? o teto de 280 caracteres por nota (evolucao_biblioteca.TEXTO_MAX) é o
# gargalo, ou o modelo já para sozinho antes disso (texto_max)? o ganho da condição A2
# (top-k recuperado) sobrevive com a biblioteca inteira no contexto, condição A5 (a5)? o ganho
# sobrevive em casos que nunca entraram em banco_casos.py/banco_casos_extra.py, nem para
# calibrar o banco (ineditos)? Cada modo chama executar_fase3.rodar_epoca com n = versão+1 e
# epocas = versão — o suficiente para cair sempre no ramo 'passada final' (ultima=True), que
# NUNCA escreve em pasta_bib — e sempre contra uma CÓPIA do snapshot oficial (_preparar_copia),
# nunca a pasta bibliotecas/<slug>/ de resultados_alvo/fase3/ direto: um erro de conta em
# 'ultima' não arrisca gravar por cima de uma época fechada da corrida oficial.
"""Executor da Fase 3-B: ponte, cruzada, texto_max, a5 e ineditos — todos sobre cópias dos
snapshots fechados da Fase 3 oficial (resultados_alvo/fase3/), em pastas de saída próprias."""
import argparse
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import caminhos
import cliente_ollama as oll
import evolucao_biblioteca as evo
import executar_fase3
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# executar_fase3.py:44-53/biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa os símbolos usados
# nas mensagens daqui (·, →) — sem isso o executor aborta com UnicodeEncodeError no meio da
# corrida, depois de inferências já gravadas.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- constantes

TODOS_OS_CASOS = CASOS + CASOS_EXTRA
MODOS = ("ponte", "cruzada", "texto_max", "a5", "ineditos")

# A Fase 3 oficial só roda a ablação de texto_max no granite (o modelo com a biblioteca mais
# lenta de crescer na corrida oficial — ver o relatório da Fase 3); fixo aqui em vez de vir de
# --modelos para o modo nunca rodar em duplicidade sobre outro modelo por engano.
GRANITE = "granite4.2:8b"


# ------------------------------------------------------------------------ auxiliares

def _oficial() -> dict:
    """! Alteração de IA - Revisar: caminhos da corrida oficial da Fase 3
    (caminhos.fase3('fase3'), que resolve para resultados_alvo/fase3/ quando RESULTADOS_DIR
    aponta para resultados_alvo — o de sempre).
    ! Motivo: nenhuma função deste módulo GRAVA nesta árvore, só lê dela (particao.json e as
    pastas bibliotecas/<slug>/epoca-N fechadas); uma função própria em vez de repetir
    caminhos.fase3('fase3') em cada modo deixa esse contrato de só-leitura num lugar só."""
    return caminhos.fase3("fase3")


def _particao_oficial(c3_oficial: dict) -> dict:
    """! Alteração de IA - Revisar: lê a partição 54/36 gravada pela corrida oficial em vez de
    recalculá-la (Fase 3-B, 21/09/2026).
    ! Motivo: evo.gravar_ou_conferir_particao já garantiu que ela é a MESMA para os 4 modelos;
    recalcular a partir de banco_casos.py deixaria a 3-B vulnerável a qualquer mudança futura
    no banco, e os 36 de avaliação precisam ser byte a byte os mesmos da Fase 3 para o
    pareamento valer."""
    if not c3_oficial["particao"].exists():
        raise SystemExit(f"sem particao.json em {c3_oficial['particao']} — rode "
                         "executar_fase3.py primeiro (a Fase 3-B só lê a corrida oficial)")
    return json.loads(c3_oficial["particao"].read_text(encoding="utf-8"))


def _casos_avaliacao(particao: dict) -> list[dict]:
    """! Alteração de IA - Revisar: os casos com particao == 'avaliacao' na partição
    informada, na ordem de TODOS_OS_CASOS.
    ! Motivo: quatro dos cinco modos da Fase 3-B medem só nos 36 casos que NUNCA entraram na
    biblioteca de nenhum modelo (a partição de avaliação da Fase 3 oficial); nenhum precisa
    reavaliar os 54 de aprendizado, que já são o que a Fase 3 oficial mede época a época."""
    return [c for c in TODOS_OS_CASOS if evo.particao_de(particao, c["id"]) == "avaliacao"]


def _particao_tudo_avaliacao(casos: list[dict]) -> dict:
    """! Alteração de IA - Revisar: uma partição sintética (mesmo formato de
    evolucao_biblioteca.particionar) em que TODO caso é 'avaliacao' — usada pelo modo
    'ineditos', que nunca gera proposta de edição.
    ! Motivo: rodar_epoca e avaliar_registro_fase3 leem particao_de(particao, caso_id) para
    gravar o campo 'particao' de cada registro; os casos de banco_casos_ineditos nunca
    participaram de uma época de aprendizado (é o ponto do modo), então a única resposta
    correta para os 90 casos originais em pastas alheias, o hash por caso, fica None — nada
    aqui recalcula a partição oficial de 90 nem depende dela."""
    return {"regra": "Fase 3-B (ineditos): casos que nunca entraram em banco_casos.py nem "
                     "banco_casos_extra.py; todos ficam em 'avaliacao' porque nenhum "
                     "participa de época de aprendizado.",
            "semente": None, "n_aprendizado": 0, "n_avaliacao": len(casos),
            "casos": {c["id"]: {"particao": "avaliacao", "classe": c["classe"],
                                "nivel": c["nivel"], "hash": None} for c in casos}}


def _preparar_copia(origem: Path, destino: Path) -> str:
    """! Alteração de IA - Revisar: copia um snapshot fechado (epoca-N com fechamento.json) de
    origem para destino só se destino ainda não existir; se já existir (relance depois de
    queda no meio de um modo da 3-B), confere que o hash bate em vez de tentar copiar de novo.
    Devolve o hash da cópia (evolucao_biblioteca.hash_biblioteca).
    ! Motivo: evo.copiar_biblioteca recusa destino existente (FileExistsError) mesmo quando o
    destino é exatamente a cópia que uma execução anterior já tinha deixado pronta — sem esta
    checagem, relançar qualquer modo da Fase 3-B depois de uma interrupção pararia na primeira
    pasta já copiada em vez de continuar do modelo que faltou. O hash comparado é o mesmo
    campo que fechar_snapshot grava, então uma cópia corrompida é acusada em vez de seguir."""
    if destino.exists():
        if not evo.snapshot_fechado(destino):
            raise SystemExit(f"{destino} existe mas não está fechada (sem fechamento.json) "
                             "— apague a pasta e relance")
    else:
        evo.copiar_biblioteca(origem, destino)
    h_origem, h_destino = evo.hash_biblioteca(origem), evo.hash_biblioteca(destino)
    if h_origem != h_destino:
        raise SystemExit(f"cópia em {destino} tem hash {h_destino}, mas a origem {origem} "
                         f"tem {h_origem} — apague {destino} e relance")
    return h_destino


def preparar_saida(nome_saida: str, particao: dict) -> dict:
    """! Alteração de IA - Revisar: cria <RESULTADOS>/<nome_saida> (nunca 'fase3', a pasta da
    corrida oficial), grava/confere particao.json e atualiza maquina.json com
    executar_fase3.maquina_atual/atualizar_maquina — os mesmos três passos que
    executar_fase3.main faz para a corrida oficial, reaproveitados sem alterar o módulo
    original.
    ! Motivo: os cinco modos da Fase 3-B gravam um particao.json (oficial copiado, ou próprio
    no modo 'ineditos') e um maquina.json (mesmo formato da Fase 3, para o Memorial poder
    citar em que máquina cada corrida rodou); repetir os três passos em cada modo faria as
    cinco saídas divergirem de formato aos poucos."""
    if nome_saida == "fase3":
        raise SystemExit("--saida não pode ser 'fase3' — é a pasta da corrida oficial, que "
                         "nenhum script novo pode escrever")
    c3b = caminhos.fase3(nome_saida)
    c3b["raiz"].mkdir(parents=True, exist_ok=True)
    evo.gravar_ou_conferir_particao(c3b["particao"], particao)
    executar_fase3.atualizar_maquina(c3b["maquina"], executar_fase3.maquina_atual(nome_saida))
    return c3b


def _gravar_condicoes(c3b: dict, *, modo: str, doador: str | None, versoes: list[int],
                      texto_max: int | None, condicao: str, modelos: list[str] | None,
                      versao_ollama: str | None) -> None:
    """! Alteração de IA - Revisar: grava condicoes_3b.json na raiz da saída — formato fechado
    do brief da Tarefa P3.1: {modo, doador, versoes, texto_max, condicao, modelos,
    versao_ollama, origem, criado_em}.
    ! Motivo: é o arquivo que diz, para qualquer pasta de saída da Fase 3-B, qual das cinco
    perguntas ela responde sem reabrir o script que a gerou — avaliar_fase3b.py lê o campo
    'modo' daqui para decidir se agrega pela via simples (avaliar_saida) ou pela via própria
    do modo 'ineditos'."""
    dado = {"modo": modo, "doador": doador, "versoes": list(versoes), "texto_max": texto_max,
            "condicao": condicao, "modelos": modelos, "versao_ollama": versao_ollama,
            "origem": "resultados_alvo/fase3",
            "criado_em": datetime.now().isoformat(timespec="seconds")}
    (c3b["raiz"] / "condicoes_3b.json").write_text(
        json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")


def _diagnosticar_versao(modelo: str, versao: int, casos: list[dict], particao: dict,
                         pasta: Path, pasta_bib: Path, k: int, mt_diag: int, mt_prop: int,
                         digest: str, versao_ollama: str | None) -> None:
    """! Alteração de IA - Revisar: roda só a passada final de executar_fase3.rodar_epoca
    (n = versão+1, epocas = versão, o que força ultima=True) — lê pasta_bib/epoca-<versão>
    (uma CÓPIA fechada) e grava diagnosticos__L<versão>.jsonl em pasta, sem propor edição nem
    escrever em pasta_bib.
    ! Motivo: é o único ponto do módulo que chama rodar_epoca — concentrar a conta de n/epocas
    aqui evita que um dos quatro modos que só diagnosticam (ponte/cruzada/a5/ineditos) passe
    epocas errado por engano e acabe caindo no ramo que ESCREVE época (só texto_max faz
    isso, e faz direto, com dois n consecutivos — ver modo_texto_max)."""
    executar_fase3.rodar_epoca(modelo, versao + 1, casos, particao, versao, k, mt_diag,
                               mt_prop, pasta, pasta_bib, digest, versao_ollama)


def _com_modelo_descarregado(modelo: str, funcao):
    """! Alteração de IA - Revisar: roda funcao() e, no finally, descarrega o modelo e confere
    que ele saiu da memória — cópia do padrão de executar_fase3.rodar_modelo_fase3
    (oll.descarregar + PAUSA_DESCARGA + um_modelo_por_vez dentro de um try/except próprio).
    ! Motivo: mesma razão do original — uma parada no meio (SystemExit de rodar_epoca, Ctrl+C)
    não pode deixar o modelo residente ocupando RAM para o próximo modelo da fila, e uma falha
    ao descarregar (Ollama fora do ar) não pode SUBSTITUIR a exceção que estava em voo (por
    isso o descarregamento tem o próprio try/except, sem propagar)."""
    try:
        return funcao()
    finally:
        try:
            oll.descarregar(modelo)
            time.sleep(executar_fase3.PAUSA_DESCARGA)
            ok, nomes = oll.um_modelo_por_vez()
            if nomes:
                print(f"  aviso: ainda residente após descarregar: {nomes}")
        except Exception as e:
            print(f"  aviso: não deu para descarregar/conferir o modelo residente "
                  f"({type(e).__name__}: {e}) — confira 'ollama ps' antes do próximo modelo")


def _preparar_modelo(modelo: str) -> tuple[str, str | None]:
    """! Alteração de IA - Revisar: confere 'um modelo por vez' e lê digest e versão do Ollama uma
    vez por modelo (Fase 3-B, 21/09/2026).
    ! Motivo: mesma política de executar_fase3.main (avisa se há residente, não aborta); digest e
    versão vão em todo registro para o pareamento com a Fase 3 (decisões 44 e 47) — lidos uma
    vez porque um GET a cada caso só acrescentaria latência sem informação nova."""
    ok, nomes = oll.um_modelo_por_vez()
    if not ok:
        print(f"!! há {len(nomes)} modelo(s) residente(s) antes de começar: {nomes}")
    return oll.instalados().get(modelo, "?"), executar_fase3._versao_ollama()


def _conferir_versao_ollama_uniforme(c3b: dict) -> str | None:
    """! Alteração de IA - Revisar: lê 'versao_ollama' de TODOS os diagnosticos__L*.jsonl
    gravados na saída e devolve a mensagem de aviso se houver mais de um valor distinto (None
    quando uniforme); quem chama junta a mensagem à das falhas e decide o código de saída.
    Antes (21/09/2026, revisão da P3.1) a função abortava sozinha e main() só a chamava quando
    não havia falha — o aviso sumia justo quando um modelo caía no meio da corrida.
    ! Motivo: a Fase 3-B roda vários modelos (e, no modo 'cruzada', vários LEITORES da mesma
    biblioteca) numa única invocação de --saida; se o servidor Ollama atualizar sozinho no
    meio da corrida (já aconteceu entre a 2-B e a Fase 3 — 0.33.3 para 0.34.0, sem aviso, numa
    máquina corporativa com atualização automática), parte dos diagnósticos da mesma pasta
    sairia de um runtime e parte de outro sem nada acusar no console, e o modo 'ponte' — que
    existe justamente para medir se um runtime reproduz o outro — mediria os dois runtimes
    misturados."""
    versoes = set()
    for arq in sorted(c3b["raiz"].glob("*/diagnosticos__L*.jsonl")):
        for linha in arq.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            versoes.add(json.loads(linha).get("versao_ollama"))
    if len(versoes) > 1:
        return (f"versao_ollama não é uniforme em {c3b['raiz']}: "
                f"{sorted(versoes, key=str)} — a saída mistura runtimes do Ollama; "
                "confira se o servidor atualizou no meio da corrida")
    return None


def _casos_ineditos() -> list[dict]:
    """! Alteração de IA - Revisar: importa banco_casos_ineditos.CASOS_INEDITOS só quando o
    modo 'ineditos' roda, e converte a ausência do módulo (ele ainda não existe neste
    repositório — é preparado numa tarefa futura) num SystemExit de código 2 com mensagem
    clara impressa no stderr, em vez de um ImportError cru.
    ! Motivo: um ImportError no TOPO do arquivo derrubaria os outros quatro modos, que não
    precisam deste módulo; capturar aqui, só quando 'ineditos' é de fato escolhido, é o que
    deixa ponte/cruzada/texto_max/a5 funcionarem hoje, antes do banco de casos inéditos
    existir. O código 2 (em vez do 1 genérico das outras paradas) é o que diferencia, para
    quem lê o código de saída de rodar_fase3b.ps1, 'faltou preparar o ambiente' de 'um modelo
    falhou durante a corrida'."""
    try:
        from banco_casos_ineditos import CASOS_INEDITOS
    except ImportError as e:
        print(f"!! banco_casos_ineditos.py não existe ou não expõe CASOS_INEDITOS ({e}) — "
              "crie o módulo (mesma forma de banco_casos.CASOS: id/classe/nivel/entrada/"
              "gabarito) antes de rodar --modo ineditos", file=sys.stderr)
        raise SystemExit(2) from e
    if not CASOS_INEDITOS:
        print("!! banco_casos_ineditos.CASOS_INEDITOS está vazio", file=sys.stderr)
        raise SystemExit(2)
    return CASOS_INEDITOS


# ------------------------------------------------------------------------------ modos

def modo_ponte(args: argparse.Namespace) -> list[str]:
    """! Alteração de IA - Revisar: modo 'ponte' — cada modelo lê a MESMA L0 oficial (cópia de
    resultados_alvo/fase3/bibliotecas/<slug>/epoca-0) nos 36 casos de avaliação; mede se o
    Ollama 0.34.1 reproduz os números da Fase 3, medidos na 0.34.0.
    ! Motivo: ver o cabeçalho do módulo — comparar direto contra os diagnosticos__L0.jsonl
    oficiais misturaria o efeito da versão do servidor com o de rodar noutro dia/noutra carga
    de máquina; aqui os modelos rodam de novo, na versão atual, sobre a MESMA biblioteca (L0
    nunca muda) e os mesmos 36 casos que nunca entraram em biblioteca nenhuma."""
    if not args.modelos:
        raise SystemExit("modo ponte exige --modelos")
    c3_of = _oficial()
    particao = _particao_oficial(c3_of)
    casos = _casos_avaliacao(particao)
    if args.casos:
        casos = casos[:args.casos]
    c3b = preparar_saida(args.saida, particao)
    _gravar_condicoes(c3b, modo="ponte", doador=None, versoes=[0], texto_max=None,
                      condicao=executar_fase3.CONDICAO, modelos=args.modelos,
                      versao_ollama=executar_fase3._versao_ollama())

    falhas: list[str] = []
    for modelo in args.modelos:
        slug = executar_fase3._slug(modelo)
        pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
        origem = c3_of["bibliotecas"] / slug / "epoca-0"
        if not origem.exists():
            print(f"\n!! {modelo}: sem epoca-0 oficial em {origem} — pulando.")
            falhas.append(modelo)
            continue
        try:
            digest, versao_ollama = _preparar_modelo(modelo)
            _preparar_copia(origem, pasta_bib / "epoca-0")
            _com_modelo_descarregado(modelo, lambda modelo=modelo, pasta=pasta,
                                     pasta_bib=pasta_bib, digest=digest,
                                     versao_ollama=versao_ollama: _diagnosticar_versao(
                modelo, 0, casos, particao, pasta, pasta_bib, args.k,
                args.max_tokens_diagnostico, args.max_tokens_proposta, digest, versao_ollama))
        except SystemExit as e:
            print(f"\n!! {modelo} parou: {e}")
            falhas.append(modelo)
    return falhas


def modo_cruzada(args: argparse.Namespace) -> list[str]:
    """! Alteração de IA - Revisar: modo 'cruzada' — a biblioteca do --doador (nas --versoes,
    oficialmente L1 e L3) lida pelos OUTROS modelos (--modelos), nos 36 casos de avaliação;
    mede se a documentação escrita por um modelo ajuda outro, ou só ajuda quem escreveu.
    ! Motivo: a Fase 3 oficial só mostra cada modelo lendo a PRÓPRIA biblioteca; sem trocar as
    bibliotecas entre modelos não dá para separar 'a edição ajuda porque documenta o produto
    de verdade' de 'a edição ajuda porque está na forma que só quem a escreveu explora bem'."""
    if not args.doador:
        raise SystemExit("modo cruzada exige --doador")
    if not args.modelos:
        raise SystemExit("modo cruzada exige --modelos (os leitores, sem o doador)")
    if args.doador in args.modelos:
        raise SystemExit(f"--doador {args.doador} não pode estar em --modelos — ele já é "
                         "medido pela Fase 3 oficial lendo a própria biblioteca")
    versoes = args.versoes or [1, 3]

    c3_of = _oficial()
    particao = _particao_oficial(c3_of)
    casos = _casos_avaliacao(particao)
    if args.casos:
        casos = casos[:args.casos]
    c3b = preparar_saida(args.saida, particao)
    _gravar_condicoes(c3b, modo="cruzada", doador=args.doador, versoes=versoes,
                      texto_max=None, condicao=executar_fase3.CONDICAO,
                      modelos=args.modelos, versao_ollama=executar_fase3._versao_ollama())

    slug_doador = executar_fase3._slug(args.doador)
    falhas: list[str] = []
    for modelo in args.modelos:
        slug = executar_fase3._slug(modelo)
        pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
        try:
            digest, versao_ollama = _preparar_modelo(modelo)

            def _rodar(modelo=modelo, pasta=pasta, pasta_bib=pasta_bib, digest=digest,
                      versao_ollama=versao_ollama) -> None:
                for versao in versoes:
                    origem = c3_of["bibliotecas"] / slug_doador / f"epoca-{versao}"
                    if not origem.exists():
                        raise SystemExit(f"sem epoca-{versao} do doador {args.doador} em "
                                         f"{origem}")
                    _preparar_copia(origem, pasta_bib / f"epoca-{versao}")
                    _diagnosticar_versao(modelo, versao, casos, particao, pasta, pasta_bib,
                                         args.k, args.max_tokens_diagnostico,
                                         args.max_tokens_proposta, digest, versao_ollama)

            _com_modelo_descarregado(modelo, _rodar)
        except SystemExit as e:
            print(f"\n!! {modelo} parou: {e}")
            falhas.append(modelo)
    return falhas


def modo_texto_max(args: argparse.Namespace) -> list[str]:
    """! Alteração de IA - Revisar: modo 'texto_max' — só granite4.2:8b; copia a L0 oficial
    (biblioteca e os 90 diagnósticos oficiais) e roda a época 1 COMPLETA (diagnóstico já
    gravado é pulado por rodar_epoca; só as 54 propostas de aprendizado rodam de novo) com
    evo.TEXTO_MAX trocado por --texto-max — o prompt continua pedindo 60-280 caracteres, é
    ablação do VALIDADOR, não do prompt — e a passada final com a L1 resultante. Restaura
    evo.TEXTO_MAX no finally.
    ! Motivo: a Fase 3 oficial recusa toda nota acima de 280 caracteres
    (evolucao_biblioteca.TEXTO_MAX); sem esta ablação não dá para saber se o teto é o que
    barra os modelos de escrever uma explicação melhor, ou se eles já param sozinhos bem antes
    disso."""
    c3_of = _oficial()
    particao = _particao_oficial(c3_of)
    casos = list(TODOS_OS_CASOS)
    if args.casos:
        casos = casos[:args.casos]
    c3b = preparar_saida(args.saida, particao)
    _gravar_condicoes(c3b, modo="texto_max", doador=None, versoes=[0, 1],
                      texto_max=args.texto_max, condicao=executar_fase3.CONDICAO,
                      modelos=[GRANITE], versao_ollama=executar_fase3._versao_ollama())

    slug = executar_fase3._slug(GRANITE)
    pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
    pasta.mkdir(parents=True, exist_ok=True)
    origem_bib = c3_of["bibliotecas"] / slug / "epoca-0"
    origem_diag = c3_of["raiz"] / slug / "diagnosticos__L0.jsonl"
    if not origem_bib.exists() or not origem_diag.exists():
        raise SystemExit(f"faltam os oficiais do granite em {origem_bib} e/ou {origem_diag}")
    _preparar_copia(origem_bib, pasta_bib / "epoca-0")
    destino_diag = pasta / "diagnosticos__L0.jsonl"
    if not destino_diag.exists():
        shutil.copy2(origem_diag, destino_diag)

    falhas: list[str] = []
    digest, versao_ollama = _preparar_modelo(GRANITE)
    original = evo.TEXTO_MAX
    try:
        evo.TEXTO_MAX = args.texto_max

        def _rodar() -> None:
            # época 1 completa (ultima=False: n=1 <= epocas=1) e a passada final com a L1
            # fechada por ela (ultima=True: n=2 > epocas=1).
            executar_fase3.rodar_epoca(GRANITE, 1, casos, particao, 1, args.k,
                                       args.max_tokens_diagnostico, args.max_tokens_proposta,
                                       pasta, pasta_bib, digest, versao_ollama)
            executar_fase3.rodar_epoca(GRANITE, 2, casos, particao, 1, args.k,
                                       args.max_tokens_diagnostico, args.max_tokens_proposta,
                                       pasta, pasta_bib, digest, versao_ollama)

        _com_modelo_descarregado(GRANITE, _rodar)
    except SystemExit as e:
        print(f"\n!! {GRANITE} parou: {e}")
        falhas.append(GRANITE)
    finally:
        evo.TEXTO_MAX = original
    return falhas


def modo_a5(args: argparse.Namespace) -> list[str]:
    """! Alteração de IA - Revisar: modo 'a5' — executar_fase3.CONDICAO = 'A5' (biblioteca
    inteira no contexto, sem recuperação top-k) em tempo de execução, restaurada no finally;
    L3 de cada --modelos, nos 36 casos de avaliação.
    ! Motivo: a Fase 3 oficial roda sempre A2 (top-k); sem esta ablação não dá para saber se o
    ganho da biblioteca editada sobrevive quando o modelo vê a biblioteca inteira, em vez de
    só os k verbetes recuperados para o caso."""
    if not args.modelos:
        raise SystemExit("modo a5 exige --modelos")
    c3_of = _oficial()
    particao = _particao_oficial(c3_of)
    casos = _casos_avaliacao(particao)
    if args.casos:
        casos = casos[:args.casos]
    c3b = preparar_saida(args.saida, particao)
    _gravar_condicoes(c3b, modo="a5", doador=None, versoes=[3], texto_max=None,
                      condicao="A5", modelos=args.modelos,
                      versao_ollama=executar_fase3._versao_ollama())

    falhas: list[str] = []
    original = executar_fase3.CONDICAO
    try:
        executar_fase3.CONDICAO = "A5"
        for modelo in args.modelos:
            slug = executar_fase3._slug(modelo)
            pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
            origem = c3_of["bibliotecas"] / slug / "epoca-3"
            if not origem.exists():
                print(f"\n!! {modelo}: sem epoca-3 oficial em {origem} — pulando.")
                falhas.append(modelo)
                continue
            try:
                digest, versao_ollama = _preparar_modelo(modelo)
                _preparar_copia(origem, pasta_bib / "epoca-3")
                _com_modelo_descarregado(modelo, lambda modelo=modelo, pasta=pasta,
                                         pasta_bib=pasta_bib, digest=digest,
                                         versao_ollama=versao_ollama: _diagnosticar_versao(
                    modelo, 3, casos, particao, pasta, pasta_bib, args.k,
                    args.max_tokens_diagnostico, args.max_tokens_proposta, digest,
                    versao_ollama))
            except SystemExit as e:
                print(f"\n!! {modelo} parou: {e}")
                falhas.append(modelo)
    finally:
        executar_fase3.CONDICAO = original
    return falhas


def modo_ineditos(args: argparse.Namespace) -> list[str]:
    """! Alteração de IA - Revisar: modo 'ineditos' — casos de banco_casos_ineditos.
    CASOS_INEDITOS (nunca entraram em banco_casos.py/banco_casos_extra.py) nas --versoes
    (oficialmente L0, L1, L3) de cada --modelos; particao.json própria com TODOS os casos em
    'avaliacao' (nenhum participou de época de aprendizado nenhuma).
    ! Motivo: os 36 casos de 'avaliação' da Fase 3 oficial nunca viraram nota, mas ajudaram a
    calibrar o banco de 90 em conjunto (achado 4.20 do Memorial); medir sobre casos que o
    processo de construção da biblioteca nunca viu de jeito nenhum é o teste mais rigoroso de
    que o ganho é generalização, e não uma forma sutil de decorar o banco de 90."""
    if not args.modelos:
        raise SystemExit("modo ineditos exige --modelos")
    casos = _casos_ineditos()
    if args.casos:
        casos = casos[:args.casos]
    versoes = args.versoes or [0, 1, 3]
    particao = _particao_tudo_avaliacao(casos)

    c3_of = _oficial()
    c3b = preparar_saida(args.saida, particao)
    _gravar_condicoes(c3b, modo="ineditos", doador=None, versoes=versoes, texto_max=None,
                      condicao=executar_fase3.CONDICAO, modelos=args.modelos,
                      versao_ollama=executar_fase3._versao_ollama())

    falhas: list[str] = []
    for modelo in args.modelos:
        slug = executar_fase3._slug(modelo)
        pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
        try:
            digest, versao_ollama = _preparar_modelo(modelo)

            def _rodar(modelo=modelo, pasta=pasta, pasta_bib=pasta_bib, digest=digest,
                      versao_ollama=versao_ollama) -> None:
                for versao in versoes:
                    origem = c3_of["bibliotecas"] / slug / f"epoca-{versao}"
                    if not origem.exists():
                        raise SystemExit(f"sem epoca-{versao} oficial de {modelo} em "
                                         f"{origem}")
                    _preparar_copia(origem, pasta_bib / f"epoca-{versao}")
                    _diagnosticar_versao(modelo, versao, casos, particao, pasta, pasta_bib,
                                         args.k, args.max_tokens_diagnostico,
                                         args.max_tokens_proposta, digest, versao_ollama)

            _com_modelo_descarregado(modelo, _rodar)
        except SystemExit as e:
            print(f"\n!! {modelo} parou: {e}")
            falhas.append(modelo)
    return falhas


_FUNCOES_POR_MODO = {"ponte": modo_ponte, "cruzada": modo_cruzada,
                     "texto_max": modo_texto_max, "a5": modo_a5, "ineditos": modo_ineditos}


# --------------------------------------------------------------------------- linha de comando

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Executor da Fase 3-B: diagnósticos complementares (ponte, cruzada, "
                    "texto_max, a5, ineditos) sobre cópias dos snapshots da Fase 3 oficial.")
    ap.add_argument("--modo", required=True, choices=MODOS)
    ap.add_argument("--saida", required=True,
                    help="subpasta nova dos resultados (nunca 'fase3', a corrida oficial)")
    ap.add_argument("--modelos", nargs="+", default=None,
                    help="modelos a rodar (ignorado no modo texto_max, que é só granite)")
    ap.add_argument("--doador", default=None, help="modelo doador da biblioteca (modo cruzada)")
    ap.add_argument("--versoes", type=int, nargs="+", default=None,
                    help="versões de biblioteca a ler (padrão por modo: cruzada 1 3, "
                    "ineditos 0 1 3)")
    ap.add_argument("--texto-max", type=int, default=600, dest="texto_max",
                    help="teto de TEXTO em caracteres, ablação de evolucao_biblioteca."
                    "TEXTO_MAX (padrão da Fase 3 oficial: 280) — só no modo texto_max")
    ap.add_argument("--k", type=int, default=3, help="verbetes recuperados (condição A2)")
    ap.add_argument("--max-tokens-diagnostico", type=int, default=600)
    ap.add_argument("--max-tokens-proposta", type=int, default=700)
    ap.add_argument("--casos", type=int, default=0,
                    help="recorta para os N primeiros casos do modo (0 = todos) — só para "
                    "teste de fumaça; a corrida de verdade usa todos")
    args = ap.parse_args()

    print(caminhos.descricao())
    falhas = _FUNCOES_POR_MODO[args.modo](args)

    c3b = caminhos.fase3(args.saida)
    print(f"\nResultados em {c3b['raiz']}")
    # a conferência de versão roda SEMPRE, antes de decidir o código de saída: com um modelo
    # caído no meio e outro rodado noutra versão do Ollama, as duas mensagens precisam aparecer
    problemas = []
    if falhas:
        problemas.append(f"{len(falhas)} modelo(s)/passo(s) pararam antes do fim: "
                         f"{', '.join(falhas)} — veja as mensagens acima")
    aviso_versao = _conferir_versao_ollama_uniforme(c3b)
    if aviso_versao:
        print(f"!! {aviso_versao}")
        problemas.append(aviso_versao)
    if problemas:
        raise SystemExit(" | ".join(problemas))


if __name__ == "__main__":
    main()
