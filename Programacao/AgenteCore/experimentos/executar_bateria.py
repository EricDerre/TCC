#!/usr/bin/env python3
# ! Alteração de IA - Revisar: executor da bateria — roda os casos de um modelo por vez,
# nas três estratégias, gravando cada resultado assim que termina.
# ! Motivo: são centenas de inferências em CPU, de horas de duração. Gravar em JSONL a cada
# caso é o que permite interromper e retomar sem repetir o que já rodou (uma execução que
# perdesse tudo ao ser interrompida seria inviável na prática). O descarregamento explícito
# entre modelos atende à exigência de não ter dois modelos disputando memória — sem isso, o
# Ollama mantém o anterior residente e as medições de memória e latência ficam contaminadas.
import argparse
import json
import platform
import time
from pathlib import Path

import biblioteca as bib
import caminhos
import cliente_ollama as oll
import recuperacao as rec
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from estrategias import ESTRATEGIAS, linear_com_biblioteca

AQUI = Path(__file__).resolve().parent
# Pasta de saída decidida por caminhos.py (RESULTADOS_DIR): a máquina-alvo grava em
# resultados_alvo/ sem sobrescrever os resultados do Ryzen em resultados/.
SAIDA = caminhos.RESULTADOS
TODOS_OS_CASOS = CASOS + CASOS_EXTRA


def ler_jsonl(arquivo: Path) -> list[dict]:
    """! Alteração de IA - Revisar: leitura linha a linha do JSONL extraída de _ja_feitos
    para função de módulo (Tarefa 3), reutilizável pelo executor da Fase 3
    (executar_fase3.py, tarefa futura).
    ! Motivo: _ja_feitos já ignorava a linha que não parseia (json.JSONDecodeError) — a
    linha truncada por uma interrupção no meio da gravação, que fica incompleta no
    arquivo — e devolvia set()/[] quando o arquivo não existe. Duplicar esse laço em
    executar_fase3.py faria as duas leituras de JSONL divergirem com o tempo."""
    if not arquivo.exists():
        return []
    registros = []
    with open(arquivo, encoding="utf-8") as f:
        for linha in f:
            try:
                registros.append(json.loads(linha))
            except json.JSONDecodeError:
                continue  # linha truncada por interrupção: será refeita
    return registros


def _ja_feitos(arquivo: Path, condicao: str) -> set[tuple[str, str]]:
    """Chaves (caso, estratégia) já gravadas NESTA condição, para retomar de onde parou.
    Registros da Fase 2-A não têm o campo 'condicao' e contam como A0.

    ! Alteração de IA - Revisar: passa a ler com ler_jsonl() em vez de repetir o laço
    linha a linha aqui.
    ! Motivo: mesma regra de antes — aqui só sobra o KeyError de r["caso"]/r["estrategia"]
    (linha sem esses campos é ignorada); o parseio malformado já foi filtrado dentro de
    ler_jsonl()."""
    feitos = set()
    for r in ler_jsonl(arquivo):
        try:
            if r.get("condicao", "A0") == condicao:
                feitos.add((r["caso"], r["estrategia"]))
        except KeyError:
            continue  # linha sem 'caso'/'estrategia': será refeita
    return feitos


def _arquivo_saida(modelo: str, condicao: str) -> Path:
    """! Alteração de IA - Revisar: um arquivo por (modelo, condição); A0 mantém o nome
    antigo para os resultados da Fase 2-A continuarem válidos sem conversão.
    ! Motivo: a retomada é por arquivo. Se as condições fossem gravadas juntas, uma
    execução interrompida de A2 poderia ser confundida com A1 já feita, e o Δ contra a
    linha de base sairia de registros misturados."""
    nome = modelo.replace(":", "_")
    return SAIDA / (f"{nome}.jsonl" if condicao == "A0" else f"{nome}__{condicao}.jsonl")


def guarda_estimativa(maior_chars: int, max_tokens: int, rotulo: str) -> int:
    """! Alteração de IA - Revisar: guarda estimada por chars/token extraída de
    rodar_modelo para função de módulo (Tarefa 3), reutilizável pelo executor da Fase 3
    (executar_fase3.py, tarefa futura).
    ! Motivo: confere ANTES de inferir que o maior prompt cabe no num_ctx junto com a
    resposta, usando o pior chars/token medido na Fase 2-A (bib.CHARS_POR_TOKEN) — quando
    o prompt excede num_ctx o Ollama descarta em silêncio os tokens do COMEÇO, que é
    justamente a biblioteca; o caso rodaria "com biblioteca" no registro e sem biblioteca
    de fato, sem nenhum erro para acusar. Repetir a conta em dois arquivos faria as duas
    guardas divergirem com o tempo."""
    estimado = round(maior_chars / bib.CHARS_POR_TOKEN) + max_tokens
    if estimado > oll.NUM_CTX:
        raise SystemExit(f"maior prompt de {rotulo} estimado em {estimado} tokens "
                         f"(com resposta) > num_ctx {oll.NUM_CTX} — encurtar a biblioteca")
    print(f"maior prompt estimado: {estimado - max_tokens} tokens + {max_tokens} de resposta")
    return estimado


def guarda_tokens_reais(tokens_entrada: int, max_tokens: int, rotulo: str) -> None:
    """! Alteração de IA - Revisar: guarda com a contagem real do tokenizador extraída de
    rodar_modelo para função de módulo (Tarefa 3), reutilizável pelo executor da Fase 3.
    ! Motivo: a estimativa por chars/token (guarda_estimativa) é aproximada; só depois da
    primeira inferência de cada condição a contagem REAL do tokenizador do modelo confirma
    se o prompt encostou em num_ctx — e o Ollama pode já ter descartado o começo (a
    biblioteca) sem avisar. `rotulo` (a condição) é recebido para manter a mesma
    assinatura de guarda_estimativa, mesmo não entrando na mensagem: a mensagem abaixo é a
    mesma de antes da extração, que já não citava a condição."""
    if tokens_entrada and tokens_entrada + max_tokens >= oll.NUM_CTX - 16:
        raise SystemExit(
            f"prompt avaliado em {tokens_entrada} tokens + {max_tokens} de resposta "
            f"encosta em num_ctx {oll.NUM_CTX}: provável truncamento do prefixo — "
            "encurtar a biblioteca ou reduzir --max-tokens (registro NÃO gravado)")


def ambiente_residente() -> dict:
    """! Alteração de IA - Revisar: resumo dos modelos residentes no Ollama extraído de
    rodar_modelo para função de módulo (Tarefa 3), reutilizável pelo executor da Fase 3.
    ! Motivo: são as mesmas três chaves finais que rodar_modelo grava em todo registro
    (somente_cpu, modelos_residentes, memoria_mb) — servem para descartar da análise
    qualquer registro medido com GPU ou com mais de um modelo residente disputando
    memória."""
    residentes = oll.residentes()
    return {
        "somente_cpu": all(m["vram_mb"] == 0 for m in residentes),
        "modelos_residentes": len(residentes),
        "memoria_mb": residentes[0]["memoria_mb"] if residentes else None,
    }


def inferir_seguro(modelo: str, prompt: str, max_tokens: int) -> dict:
    """! Alteração de IA - Revisar: o try/except em torno de oll.gerar extraído de
    rodar_modelo para função de módulo (Tarefa 3), reutilizável pelo executor da Fase 3.
    ! Motivo: falha de rede/timeout do Ollama não pode derrubar a bateria inteira — são
    centenas de inferências, de horas de duração; o executor da Fase 3 precisa do mesmo
    dicionário de erro para gravar o caso como falho e seguir para o próximo."""
    try:
        return oll.gerar(modelo, prompt, max_tokens=max_tokens)
    except Exception as e:  # falha de rede/timeout não deve derrubar a bateria
        return {"segundos": None, "tokens_entrada": 0, "tokens_saida": 0,
                "resposta": "", "erro": f"{type(e).__name__}: {e}"}


def rodar_modelo(modelo: str, casos: list[dict], estrategias: list[str],
                 max_tokens: int = 900, condicao: str = "A0", k: int = 3) -> None:
    SAIDA.mkdir(exist_ok=True)
    arquivo = _arquivo_saida(modelo, condicao)
    feitos = _ja_feitos(arquivo, condicao)

    # A biblioteca só é carregada quando a condição usa; em A0 o prompt é o mesmo da
    # Fase 2-A, byte a byte, para a linha de base continuar comparável.
    verbetes = indice = None
    if condicao != "A0":
        verbetes = bib.carregar()
        problemas = bib.validar(verbetes, TODOS_OS_CASOS)
        if problemas:
            raise SystemExit("biblioteca inválida — rode validar_banco.py:\n  " +
                             "\n  ".join(problemas))
        indice = rec.Indice(verbetes)
        print(f"biblioteca: {bib.resumo(verbetes)}")

    digest = oll.instalados().get(modelo, "?")
    pendentes = [(c, e) for c in casos for e in estrategias if (c["id"], e) not in feitos]
    print(f"\n=== {modelo} (digest {digest}) — condição {condicao} ===")
    print(f"{len(feitos)} já feitos, {len(pendentes)} pendentes")
    if not pendentes:
        return

    # ! Alteração de IA - Revisar (Tarefa 3): a guarda passa a chamar guarda_estimativa()
    # (extraída para função de módulo), em vez de repetir a conta e o SystemExit aqui.
    # ! Motivo: confere ANTES de inferir que o maior prompt cabe no num_ctx junto com a
    # resposta, usando o pior chars/token medido na Fase 2-A — quando o prompt excede
    # num_ctx o Ollama descarta os tokens do COMEÇO em silêncio, e o começo é justamente a
    # biblioteca. Mesma conta e mesma mensagem de antes; ver guarda_estimativa() acima.
    if condicao != "A0":
        maior = max(len(linear_com_biblioteca(c, rec.contexto(verbetes, indice, c,
                                                                condicao, k)["texto"]))
                    for c, _ in pendentes)
        guarda_estimativa(maior, max_tokens, condicao)

    inicio_lote = time.time()
    with open(arquivo, "a", encoding="utf-8") as f:
        for i, (caso, nome_estrategia) in enumerate(pendentes, 1):
            if condicao == "A0":
                ctx = {"texto": "", "verbetes_ids": [], "verbete_ouro": None,
                       "causa_plantada": None}
                prompt = ESTRATEGIAS[nome_estrategia](caso)
            else:
                ctx = rec.contexto(verbetes, indice, caso, condicao, k)
                prompt = linear_com_biblioteca(caso, ctx["texto"])
            # ! Alteração de IA - Revisar (Tarefa 3): a inferência passa a chamar
            # inferir_seguro() (extraída para função de módulo), que já embute o
            # try/except abaixo.
            # ! Motivo: mesmo comportamento de antes — falha de rede/timeout não deve
            # derrubar a bateria — reaproveitado sem duplicar o try/except; ver
            # inferir_seguro() acima.
            r = inferir_seguro(modelo, prompt, max_tokens)

            # ! Alteração de IA - Revisar (Tarefa 3): a segunda guarda passa a chamar
            # guarda_tokens_reais() (extraída para função de módulo).
            # ! Motivo: mesma checagem de antes, agora com a contagem REAL do tokenizador
            # do modelo: se o prompt encostou em num_ctx menos a resposta, o Ollama já pode
            # ter descartado o começo (a biblioteca) sem avisar. Só a primeira inferência
            # de cada condição decide; não vale gastar horas para descobrir no fim.
            if condicao != "A0" and i == 1:
                guarda_tokens_reais(r.get("tokens_entrada", 0), max_tokens, condicao)

            registro = {
                "modelo": modelo, "digest": digest,
                # nome da máquina em cada registro: os resultados de máquinas diferentes
                # não podem ser comparados em tempo nem pareados por caso.
                "maquina": platform.node(),
                "caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"],
                "estrategia": nome_estrategia,
                "condicao": condicao,
                "verbetes_ids": ctx["verbetes_ids"],
                "verbete_ouro": ctx["verbete_ouro"],
                "causa_plantada": ctx["causa_plantada"],
                "chars_contexto": len(ctx["texto"]),
                "gabarito": caso["gabarito"],
                "teto_tokens": max_tokens,
                **r,
                # ! Alteração de IA - Revisar (Tarefa 3): as três chaves finais passam a
                # vir de ambiente_residente() (extraída para função de módulo), em vez de
                # montar o dicionário com oll.residentes() aqui.
                # ! Motivo: mesmas três chaves e mesmos valores de antes (somente_cpu,
                # modelos_residentes, memoria_mb); ver ambiente_residente() acima.
                **ambiente_residente(),
            }
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
            f.flush()  # grava já: interromper aqui não perde o caso

            if i % 10 == 0 or i == len(pendentes):
                decorrido = time.time() - inicio_lote
                resta = decorrido / i * (len(pendentes) - i)
                print(f"  {i}/{len(pendentes)} — {decorrido/60:.1f} min decorridos, "
                      f"~{resta/60:.1f} min restantes")

    oll.descarregar(modelo)
    time.sleep(2)
    ok, nomes = oll.um_modelo_por_vez()
    if nomes:
        print(f"  aviso: ainda residente após descarregar: {nomes}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", nargs="+", required=True)
    ap.add_argument("--estrategias", nargs="+", default=list(ESTRATEGIAS))
    # ! Alteração de IA - Revisar: o teto de resposta passa a depender da condição — 900 em
    # A0 (igual à Fase 2-A) e 600 nos braços com biblioteca, salvo valor explícito.
    # ! Motivo: com num_ctx fixo em 8192, prompt e resposta dividem o mesmo orçamento; a
    # biblioteca inteira (~6,5 mil tokens no pior tokenizador medido) mais o maior caso
    # não deixam 900 para a resposta. Na Fase 2-A nenhuma resposta linear passou de
    # 600 tokens (ver Memorial §4.18), e o avaliar.py acusa qualquer resposta cortada
    # sem CAUSA_RAIZ — o caso não passa despercebido.
    ap.add_argument("--max-tokens", type=int, default=None,
                    help="teto de tokens por resposta (padrao: 900 em A0, 600 com biblioteca); "
                         "respostas no teto sao truncadas e invalidam o caso (ver avaliar.py)")
    ap.add_argument("--casos", type=int, default=0,
                    help="usar apenas os N primeiros casos (0 = todos os 90)")
    # ! Alteração de IA - Revisar: condição de biblioteca da Fase 2-B (A0 = sem biblioteca,
    # igual à Fase 2-A; A1 inteira; A2 recuperada top-k; A3 só o verbete certo; A4
    # distratores plausíveis; A5 verbete errado + registro falso).
    # ! Motivo: são os braços do desenho experimental aprovado; fora de A0 a estratégia é
    # forçada para 'linear' porque foi a vencedora da Fase 2-A e cruzar as três com as
    # condições triplicaria o custo sem responder nada novo.
    ap.add_argument("--condicao", choices=rec.CONDICOES, default="A0")
    ap.add_argument("--k", type=int, default=3, help="verbetes recuperados em A2/A4")
    args = ap.parse_args()

    print(caminhos.descricao())
    casos = TODOS_OS_CASOS[:args.casos] if args.casos else TODOS_OS_CASOS
    max_tokens = args.max_tokens or (900 if args.condicao == "A0" else 600)
    estrategias = args.estrategias
    if args.condicao != "A0" and estrategias != ["linear"]:
        print("condição com biblioteca: estratégia fixada em 'linear' (vencedora da Fase 2-A)")
        estrategias = ["linear"]
    instalados = oll.instalados()

    print(f"{len(casos)} casos x {len(estrategias)} estratégias "
          f"= {len(casos) * len(estrategias)} inferências por modelo")

    for modelo in args.modelos:
        if modelo not in instalados:
            print(f"\n!! {modelo} não está baixado — pulando.")
            continue
        ok, nomes = oll.um_modelo_por_vez()
        if not ok:
            print(f"!! há {len(nomes)} modelos residentes antes de começar: {nomes}")
        rodar_modelo(modelo, casos, estrategias, max_tokens, args.condicao, args.k)

    print(f"\nResultados em {SAIDA}")


if __name__ == "__main__":
    main()
