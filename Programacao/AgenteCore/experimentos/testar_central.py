#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, ficha 109, decisão 170): os testes do hub como central aberta pelo `Cobaia.exe`, no mesmo
# formato sem pytest de `testar_hub.py`, de quem este arquivo reaproveita os ajudantes. Cobrem: o `run.py` subindo o hub com o Python da venv
# do AgenteCore e encerrando os três processos; o `Cobaia.py` abrindo uma aba só, no hub, e voltando ao site e à API quando o hub não sobe; a
# opção `--cobaias-no-ar` do executor, desligada por padrão; a corrida lançada pelo hub aberto pelo `.exe` (o executor chamado direto, com as
# cobaias já no ar e o Ollama conferido antes); a conferência do Ollama, com a sonda, a procura do programa e o início dele de mentira; a
# descoberta da corrida lançada pelo hub na lista de casos; o estado dos serviços e os atalhos (`/api/central`); as métricas por corrida
# lidas dos registros (`/api/metricas`), com o tempo de reparo da 28b e da 21d conferido contra as leituras gravadas da Fase 5 e da Fase 4;
# e, na página, a tela "Início" e a vista "Métricas".
# Escritos ANTES do código: a primeira rodada falhou por AttributeError em `run.comando_do_hub` e, feito o `run.py`, em `hub.comando_direto`.
# ! Motivo: o Eric pediu que o hub seja a central de tudo, aberta pelo `.exe`, de onde se rodam os testes e se veem as métricas. Os testes
# ficam num arquivo próprio para a contagem de `testar_hub.py`, que `resultados_alvo/fase4/hub.json` e os textos do pacote Q6 citam, não mudar.
# Nenhum deles sobe o site, a API, o banco, o Ollama ou o modelo: os processos, a sonda das portas e o Ollama são de mentira.
"""Testes do hub como central aberta pelo Cobaia.exe (ficha 109), sem pytest. Uso (em Programacao/AgenteCore/experimentos):
  PYTHONIOENCODING=utf-8 ../.venv/Scripts/python.exe testar_central.py     # todos, com o Chromium do Playwright sem janela
  PYTHONIOENCODING=utf-8 python testar_central.py                          # os da página são pulados com aviso
"""
import argparse
import inspect
import json
import shutil
import statistics
import sys
import traceback
from pathlib import Path

EXP = Path(__file__).resolve().parent
RAIZ = EXP.parent.parent.parent
RA = EXP / "resultados_alvo"
for pasta in (str(EXP), str(RAIZ)):
    if pasta not in sys.path:
        sys.path.insert(0, pasta)

import hub
import hub_dados as hd
import testar_hub as th
import testar_pos_fase4 as tp4

_TEMPORARIOS = tp4._TEMPORARIOS
_erro, _json, _http, _hub_no_ar, _navegador, _acervo_de_teste, _esperar_texto, _ate = (th._erro, th._json, th._http, th._hub_no_ar, th._navegador, th._acervo_de_teste,
                                                                                  th._esperar_texto, th._ate)


class ProcessoDeMentira:
    """Um processo que já terminou (ou não), para os testes do `run.py` e do `Cobaia.py` não subirem nada."""

    def __init__(self, vivo: bool = True) -> None:
        self.vivo, self.encerrado = vivo, False

    def poll(self):
        return None if self.vivo else 0

    def terminate(self) -> None:
        self.encerrado, self.vivo = True, False


def _acervo_que_descobre() -> tuple[hd.Acervo, Path]:
    """As duas corridas de mentira de `testar_hub`, num acervo que também procura as corridas lançadas pelo hub (o padrão de `python hub.py`)."""
    fixo, raiz = _acervo_de_teste()
    return hd.Acervo(raiz, corridas=("c1", "c2"), leituras=fixo.leituras), raiz


def _corrida_do_hub(raiz: Path, nome: str = "hub_20261125_230000") -> Path:
    """Uma corrida como a que o botão do hub lança: a trilha de `c2` com o nome da pasta nova nos identificadores (como o executor grava) e
    um `cenarios.jsonl` de duas execuções, uma de cada cenário."""
    pasta = raiz / nome
    pasta.mkdir()
    trilha_de_c2 = (raiz / "c2" / "trilha_tela.jsonl").read_text(encoding="utf-8")
    assert '"c2/qwen2.5_7b/' in trilha_de_c2
    (pasta / "trilha_tela.jsonl").write_text(trilha_de_c2.replace('"c2/qwen2.5_7b/', f'"{nome}/qwen2.5_7b/'), encoding="utf-8")
    shutil.copy(raiz / "c2" / "condicoes_fase4.json", pasta / "condicoes_fase4.json")
    linhas = [{"cenario": "contrato-field_missing", "repeticao": 1, "task_success": True, "detectou": True, "mttr_s": 60.0, "tipo": "contrato"},
              {"cenario": "localizador-front-busca", "repeticao": 1, "task_success": False, "detectou": True, "mttr_s": 80.0, "tipo": "localizador"}]
    (pasta / "cenarios.jsonl").write_text("".join(json.dumps(l) + "\n" for l in linhas), encoding="utf-8")
    return pasta


# ------------------------------------------------------------------ o run.py e o Cobaia.py

def teste_run_sobe_o_hub_com_o_python_da_venv_do_agente_e_encerra_os_tres():
    import run
    agente = tp4._temp() / "AgenteCore"
    assert run.comando_do_hub(agente=agente) is None, "sem a venv do AgenteCore não há como subir o hub"
    python = agente / ".venv" / ("Scripts/python.exe" if run.OS_NAME == "Windows" else "bin/python")
    python.parent.mkdir(parents=True)
    python.write_text("", encoding="utf-8")
    assert run.comando_do_hub(agente=agente) is None, "sem o hub.py também não"
    (agente / "experimentos").mkdir()
    (agente / "experimentos" / "hub.py").write_text("", encoding="utf-8")
    comando = run.comando_do_hub(agente=agente)
    assert comando == [str(python), str(agente / "experimentos" / "hub.py"), "--sem-abrir", "--porta", str(run.HUB_PORT), "--pelo-exe"], comando
    assert run.HUB_PORT == hub.PORTA_PADRAO == 8765 and run.HUB_PORT not in (run.FRONT_PORT, run.API_PORT)
    chamadas = []
    antigos = run.subprocess.Popen, run.stop_managed_mariadbd
    try:
        run.subprocess.Popen = lambda cmd, **k: chamadas.append((cmd, k)) or ProcessoDeMentira()
        run.stop_managed_mariadbd = lambda: chamadas.append("banco parado")
        assert run.start_hub(agente=tp4._temp()) is None and chamadas == [], "sem o que subir, nada é lançado"
        proc = run.start_hub(agente=agente)
        assert isinstance(proc, ProcessoDeMentira) and chamadas[0][0] == comando and chamadas[0][1]["cwd"] == str(agente / "experimentos")
        front, api, do_hub = ProcessoDeMentira(vivo=False), ProcessoDeMentira(), ProcessoDeMentira()
        run.wait_and_cleanup(front, api, do_hub)
        assert api.encerrado and do_hub.encerrado and chamadas[-1] == "banco parado", "o site caiu: a API, o hub e o banco são encerrados"
        front2, api2 = ProcessoDeMentira(vivo=False), ProcessoDeMentira()
        run.wait_and_cleanup(front2, api2, None)
        assert api2.encerrado, "sem hub (None), o encerramento é o de antes"
    finally:
        run.subprocess.Popen, run.stop_managed_mariadbd = antigos


def teste_cobaia_abre_so_o_hub_e_volta_ao_site_e_a_api_quando_o_hub_nao_sobe():
    import Cobaia
    import install
    import run
    abertos, limpeza = [], []
    guardados = {(m, n): getattr(m, n) for m, n in ((install, "main"), (run, "start_services"), (run, "start_hub"), (run, "wait_until_ready"), (run, "wait_for_port"),
                                                    (run, "wait_and_cleanup"), (Cobaia.webbrowser, "open"))}
    front, api, do_hub = ProcessoDeMentira(), ProcessoDeMentira(), ProcessoDeMentira()
    try:
        install.main = lambda: 0
        run.start_services = lambda: (front, api)
        run.wait_until_ready = lambda *a, **k: True
        run.wait_and_cleanup = lambda *procs: limpeza.append(procs)
        Cobaia.webbrowser.open = lambda url: abertos.append(url)
        run.start_hub = lambda: do_hub
        run.wait_for_port = lambda porta, timeout_s=30: porta == run.HUB_PORT
        Cobaia.main()
        assert abertos == [f"http://127.0.0.1:{run.HUB_PORT}/"], abertos
        assert limpeza == [(front, api, do_hub)], "fechar a janela encerra os três"
        for caso in ("o hub não foi lançado", "o hub foi lançado e a porta não respondeu"):
            abertos.clear()
            limpeza.clear()
            run.start_hub = (lambda: None) if caso.startswith("o hub não foi") else (lambda: do_hub)
            run.wait_for_port = lambda porta, timeout_s=30: False
            Cobaia.main()
            assert abertos == [f"http://localhost:{run.FRONT_PORT}", f"http://localhost:{run.API_PORT}/docs"], (caso, abertos)
            assert len(limpeza) == 1 and limpeza[0][:2] == (front, api), caso
    finally:
        for (modulo, nome), valor in guardados.items():
            setattr(modulo, nome, valor)


# ------------------------------------------------------------------ o executor com as cobaias já no ar

def teste_executor_cobaias_no_ar_vem_desligado_e_nao_sobe_nem_derruba_nada():
    import executar_fase4 as ex
    padrao = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "qualquer"])
    assert padrao.cobaias_no_ar is False, "desligado por padrão: a corrida de sempre sobe e derruba o site, a API e o banco"
    ligado = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "qualquer", "--cobaias-no-ar"])
    chamadas = []
    assert ex.subir_cobaias(padrao, iniciar=lambda: chamadas.append("subiu") or ("front", "api")) == ("front", "api") and chamadas == ["subiu"]
    assert ex.subir_cobaias(ligado, iniciar=lambda: chamadas.append("subiu de novo")) == (None, None) and chamadas == ["subiu"], "com as cobaias já no ar, nada é lançado"
    import _env_common as env
    antigos = ex.ligar_modo, env.stop_managed_mariadbd
    try:
        ex.ligar_modo = lambda modo, campo, token: chamadas.append(("modo", modo))
        env.stop_managed_mariadbd = lambda: chamadas.append("banco parado")
        ex.derrubar_cobaias(None, None, "token", parar_banco=False)
        assert chamadas[-1] == ("modo", "normal") and "banco parado" not in chamadas, "a API volta ao modo normal, e o banco do site que está no ar continua de pé"
        ex.derrubar_cobaias(None, None, "token")
        assert chamadas[-1] == "banco parado", "sem a opção, o fim da corrida é o de sempre"
    finally:
        ex.ligar_modo, env.stop_managed_mariadbd = antigos
    fonte = inspect.getsource(ex.rodar_cenarios)
    assert "front, api = subir_cobaias(args)" in fonte and "derrubar_cobaias(front, api, args.token, parar_banco=not args.cobaias_no_ar)" in fonte


# ------------------------------------------------------------------ a corrida lançada pelo hub aberto pelo .exe

def teste_hub_pelo_exe_chama_o_executor_direto_com_as_cobaias_no_ar_e_confere_o_ollama_antes():
    direto = hub.comando_direto("hub_x", {"repeticoes": 2, "selecao": "todos", "desde": None}, python="py")
    assert direto == ["py", "executar_fase4.py", "--modo", "cenarios", "--saida", "hub_x", "--casos", "10", "--repeticoes", "2", "--cobaias-no-ar", "--etapas-ao-vivo"], direto
    assert hub.comando_direto("hub_x", {"repeticoes": 1, "selecao": "git", "desde": "abc1234"}, python="py")[-4:] == ["--selecao", "git", "--desde", "abc1234"]
    acervo, raiz = _acervo_de_teste()
    passos = []

    def lancador(saida, opcoes):
        passos.append("lançou")
        return [sys.executable, "-c", "import os; print('RESULTADOS_DIR=' + os.environ.get('RESULTADOS_DIR', '(vazio)') + ' fim')"]

    assert hub.pasta_dos_resultados(hub.RESULTADOS) == "resultados_alvo", "a pasta padrão vai pelo nome, como o `rodar_fase4.ps1` manda"
    assert hub.pasta_dos_resultados(raiz) == str(raiz), "outra pasta de resultados vai pelo caminho inteiro, para a corrida cair onde o hub lê"
    with _hub_no_ar(acervo, pelo_exe=True, comando_da_corrida=lancador, garantir_ollama=lambda: passos.append("ollama") and None) as (base, _, _srv):
        e = _json(base, "GET", "/api/execucao")[1]
        assert e["permitida"] is True and e["pelo_exe"] is True, "aberto pelo .exe, o botão vem liberado"
        assert "executar_fase4.py" in e["comando_sugerido"] and "--cobaias-no-ar" in e["comando_sugerido"] and "rodar_fase4.ps1" not in e["comando_sugerido"], e["comando_sugerido"]
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1})[0] == 200 and passos == ["ollama", "lançou"], passos
        fim = _ate(lambda: _json(base, "GET", "/api/execucao")[1], lambda d: d["terminou"])
        assert fim["codigo"] == 0 and f"RESULTADOS_DIR={raiz} fim" in fim["log"], fim["log"]
    with _hub_no_ar(acervo, pelo_exe=True, comando_da_corrida=lancador, garantir_ollama=lambda: "o Ollama não respondeu em 30 s") as (base, _, _srv):
        passos.clear()
        status, r = _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1})
        assert status == 409 and "Ollama" in r["erro"] and passos == [], "sem o Ollama no ar, a corrida nem é lançada, e a página diz por quê"
    with _hub_no_ar(acervo) as (base, _, _srv):
        e = _json(base, "GET", "/api/execucao")[1]
        assert e["permitida"] is False and e["pelo_exe"] is False and "rodar_fase4.ps1" in e["comando_sugerido"], "`python hub.py` sozinho continua só mostrando o comando"
    args = hub.argumentos(["--pelo-exe", "--sem-abrir"])
    assert args.pelo_exe is True and hub.argumentos([]).pelo_exe is False


def teste_garantir_ollama_so_inicia_o_que_nao_responde_e_diz_por_que_nao_deu():
    lancados = []
    lancar = lambda programa: lancados.append(programa)
    assert hub.garantir_ollama_no_ar(espera_s=1, sonda=lambda porta: True, achar=lambda: "ollama.exe", lancar=lancar) is None and lancados == [], "já no ar: nada é iniciado"
    falta = hub.garantir_ollama_no_ar(espera_s=1, sonda=lambda porta: False, achar=lambda: None, lancar=lancar)
    assert "Ollama" in falta and "instalador" in falta and lancados == [], falta
    respostas = iter([False, False, True])
    assert hub.garantir_ollama_no_ar(espera_s=5, sonda=lambda porta: next(respostas), achar=lambda: "ollama.exe", lancar=lancar, pausa_s=0.01) is None
    assert lancados == ["ollama.exe"], "fora do ar e instalado: o hub inicia o servidor do Ollama e espera a porta responder"
    portas = []
    mudo = hub.garantir_ollama_no_ar(espera_s=0.05, sonda=lambda porta: portas.append(porta) and False, achar=lambda: "ollama.exe", lancar=lancar, pausa_s=0.01)
    assert "Ollama" in mudo and "não respondeu" in mudo and set(portas) == {hub.PORTA_DO_OLLAMA} and hub.PORTA_DO_OLLAMA == 11434, mudo

    def quebra(programa):
        raise OSError("acesso negado")

    assert "acesso negado" in hub.garantir_ollama_no_ar(espera_s=1, sonda=lambda porta: False, achar=lambda: "ollama.exe", lancar=quebra)


def teste_acervo_descobre_a_corrida_lancada_pelo_hub():
    acervo, raiz = _acervo_que_descobre()
    assert [c["pasta"] for c in acervo.corridas()] == ["c1", "c2"] and len(acervo.indice()) == 3
    _corrida_do_hub(raiz)
    (raiz / "hub_sem_trilha").mkdir()
    (raiz / "outra_pasta").mkdir()
    shutil.copy(raiz / "c2" / "trilha_tela.jsonl", raiz / "outra_pasta" / "trilha_tela.jsonl")
    corridas = acervo.corridas()
    assert [c["pasta"] for c in corridas] == ["c1", "c2", "hub_20261125_230000"], "só entra a pasta `hub_...` que tem trilha"
    assert "pelo hub" in corridas[-1]["rotulo"] and corridas[-1]["casos"] == 2 and len(acervo.indice()) == 5
    nova = next(l for l in acervo.indice() if l["corrida"] == "hub_20261125_230000")
    assert acervo.caso(nova["tid"])["corrida"]["pasta"] == "hub_20261125_230000", "o caso da corrida nova abre como os outros"
    fixo = hd.Acervo(raiz, corridas=("c1",), descobrir=False)
    assert [c["pasta"] for c in fixo.corridas()] == ["c1"], "quem pede corridas fixas pode desligar a descoberta"


# ------------------------------------------------------------------ o início e as métricas

def teste_central_diz_o_estado_dos_servicos_e_da_os_atalhos():
    acervo, _ = _acervo_de_teste()
    with _hub_no_ar(acervo, sonda=lambda porta: porta == 8080, ollama_no_ar=lambda: False) as (base, _, _srv):
        status, c = _json(base, "GET", "/api/central")
        por = {s["id"]: s for s in c["servicos"]}
        assert status == 200 and list(por) == ["site", "api", "ollama", "hub"], list(por)
        assert por["site"] == {"id": "site", "nome": por["site"]["nome"], "url": "http://localhost:8080", "no_ar": True} and por["api"]["no_ar"] is False
        assert por["api"]["url"] == "http://localhost:8000/docs" and por["ollama"]["no_ar"] is False and por["ollama"]["url"] is None and por["hub"]["no_ar"] is True
        assert c["painel"]["url"] == "/painel" and c["pelo_exe"] is False and c["execucao_permitida"] is False
        assert c["casos"] == 3 and c["corridas"] == 2
    with _hub_no_ar(acervo, pelo_exe=True, sonda=lambda porta: True, ollama_no_ar=lambda: True, garantir_ollama=lambda: None) as (base, _, _srv):
        c = _json(base, "GET", "/api/central")[1]
        assert c["pelo_exe"] is True and c["execucao_permitida"] is True and all(s["no_ar"] for s in c["servicos"])


def teste_metricas_por_corrida_saem_dos_registros_e_o_alto_do_resultado_da_fase_5():
    m = hd.metricas(hd.Acervo(RA))
    por = {c["pasta"]: c for c in m["corridas"]}
    assert list(por) == [c["pasta"] for c in hd.CORRIDAS_PADRAO] + [p for p in por if p.startswith("hub_")]
    registros = [json.loads(l) for l in (RA / "fase5_agente_b" / "cenarios.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    b = por["fase5_agente_b"]
    por_cenario: dict[str, list[float]] = {}
    for r in registros:
        if r.get("mttr_s") is not None:
            por_cenario.setdefault(r["cenario"], []).append(r["mttr_s"])
    media_dos_cenarios = statistics.fmean(statistics.fmean(t) for t in por_cenario.values())
    assert b["execucoes"] == len(registros) and b["task_success"] == sum(1 for r in registros if r["task_success"]) and b["detectou"] == sum(1 for r in registros if r["detectou"])
    assert b["mttr_media_s"] == round(media_dos_cenarios, 1) and b["cenarios_com_tempo"] == len(por_cenario), b["mttr_media_s"]
    oficial = json.loads((RA / "fase5" / "medicao.json").read_text(encoding="utf-8"))["lados"]["agente"]["geral"]["tempo_media_s"]
    assert b["mttr_media_s"] == round(oficial, 1), "o tempo de reparo da 28b no hub é o da leitura da Fase 5: a média dos cenários, não a das execuções"
    assert len(b["por_cenario"]) == len({r["cenario"] for r in registros}) and sum(x["execucoes"] for x in b["por_cenario"]) == len(registros)
    assert b["casos"] == b["execucoes"] and b["vale_como_medida"] is True and por["fase4_ensaio_v4"]["execucoes"] == 10
    ensaio = json.loads((RA / "fase4" / "cenarios_v4.json").read_text(encoding="utf-8"))["geral"]
    assert por["fase4_ensaio_v4"]["mttr_media_s"] == round(ensaio["mttr_media_s"], 1) and por["fase4_ensaio_v4"]["task_success"] == ensaio["sucessos"], "a 21d bate com a leitura da Fase 4"
    t = por["fase4_ineditos"]
    assert t["execucoes"] is None and t["task_success"] is None and t["casos"] == 36 and sum(t["confianca"].values()) == 36, "corrida em texto: só os casos e a confiança"
    assert list(t["confianca"]) == [n for n in ("alta", "média", "baixa") if n in t["confianca"]], "a confiança sai sempre na mesma ordem: alta, média, baixa"
    medicao = json.loads((RA / "fase5" / "medicao.json").read_text(encoding="utf-8"))
    f5 = m["fase5"]
    assert f5["tempo"] == medicao["tempo"]["geral"]["frase"] and f5["task_success"] == medicao["task_success"]["frase"]
    assert f5["agente"] == {"sucessos": medicao["task_success"]["agente"]["sucessos"], "n": medicao["task_success"]["agente"]["n"]}
    assert f5["pessoas"] == {"sucessos": medicao["task_success"]["pessoas"]["sucessos"], "n": medicao["task_success"]["pessoas"]["n"]}
    assert f5["ressalva"] and "integrante" in f5["ressalva"], "o veredito do Task Success vai sempre com a ressalva (decisão 151)"
    acervo, raiz = _acervo_que_descobre()
    _corrida_do_hub(raiz)
    sintetica = {c["pasta"]: c for c in hd.metricas(acervo)["corridas"]}
    h = sintetica["hub_20261125_230000"]
    assert h["execucoes"] == 2 and h["task_success"] == 1 and h["mttr_media_s"] == 70.0 and h["vale_como_medida"] is False, h
    assert sintetica["c1"]["execucoes"] is None and sintetica["c1"]["vale_como_medida"] is None, "de uma pasta que o hub não conhece, ele não diz se é medida"
    assert hd.metricas(acervo)["fase5"] is None, "sem medicao.json não há resultado da Fase 5 a mostrar"
    with _hub_no_ar(acervo) as (base, _, _srv):
        status, dado = _json(base, "GET", "/api/metricas")
        assert status == 200 and [c["pasta"] for c in dado["corridas"]] == ["c1", "c2", "hub_20261125_230000"]


def teste_pagina_inicio_mostra_os_servicos_leva_as_metricas_e_a_rodar():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_que_descobre()
        _corrida_do_hub(raiz)
        with _hub_no_ar(acervo, pelo_exe=True, sonda=lambda porta: porta == 8080, ollama_no_ar=lambda: False, garantir_ollama=lambda: "sem Ollama no teste",
                        comando_da_corrida=lambda saida, opcoes: [sys.executable, "-c", "print('nunca roda')"]) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#inicio .servico")
            assert pagina.is_visible("#inicio") and pagina.is_hidden("#caso") and pagina.is_hidden("#metricas") and pagina.is_hidden("#ao-vivo")
            assert pagina.locator("#inicio .servico").count() == 4
            assert "no ar" in pagina.inner_text('#inicio .servico[data-servico="site"]') and "fora do ar" in pagina.inner_text('#inicio .servico[data-servico="api"]')
            assert pagina.get_attribute('#inicio .servico[data-servico="site"] a', "href") == "http://localhost:8080"
            assert pagina.get_attribute("#inicio a.painel", "href") == "/painel"
            assert "5 casos" in pagina.inner_text("#inicio")
            pagina.click("#ir-para-metricas")
            pagina.wait_for_selector("#metricas svg .barra-da-corrida")
            assert pagina.is_visible("#metricas") and pagina.is_hidden("#inicio") and pagina.locator("#metricas tr.corrida").count() == 3
            barra = pagina.locator('#grafico-do-reparo svg .barra-da-corrida[data-corrida="hub_20261125_230000"]').text_content()
            assert "1 de 2" in barra and "70,0" in barra, barra
            linha = pagina.locator('#metricas tr.corrida[data-corrida="hub_20261125_230000"]').text_content()
            assert "1 de 2" in linha and "70,0" in linha and "não" in linha, "a tabela recolhida traz os mesmos números do gráfico: " + linha
            pagina.click("#abrir-inicio")
            pagina.wait_for_selector("#inicio:visible")
            pagina.click("#ir-para-rodar")
            pagina.wait_for_selector("#rodar-cenarios:visible")
            assert pagina.is_visible("#ao-vivo") and pagina.is_hidden("#inicio")
            pagina.click("#rodar-cenarios")
            _esperar_texto(pagina, "#erro", "Ollama")
            pagina.click("#lista-de-casos .item-caso >> nth=0")
            pagina.wait_for_selector("#caso section.bloco")
            assert pagina.is_hidden("#inicio") and pagina.is_hidden("#ao-vivo")
            pagina.click("#abrir-metricas")
            pagina.wait_for_selector("#metricas:visible")
            pagina.reload()
            pagina.wait_for_selector("#metricas svg .barra-da-corrida")
            assert pagina.is_visible("#metricas"), "o endereço guarda a vista"
        assert [e for e in erros if "status of 409" not in e] == [], erros


# ------------------------------------------------------------------ o molde visual (ficha 113): o processo do caso, a rede e a página
# ! Alteração de IA - Revisar: (26/11/2026, molde visual do hub) testes novos, escritos antes do código: `processo` (as seis etapas do caso com o
# tempo que a trilha grava, as três saídas e a rede que liga os sinais, os verbetes e as causas), o que a vista ao vivo diz da etapa em andamento, e
# a página (o diagrama dos espaços de trabalho, a lista de casos em grupos com a legenda, a linha de produção do caso com o cartão ampliado, a
# rede no lugar do texto corrido e os gráficos das métricas).
# ! Motivo: o Eric testou o hub e pediu menos texto, cada campo explicado e diagramas gerados por código, com o processo, o tempo de cada etapa e
# o resultado. Os tempos são conferidos contra os eventos da trilha da corrida curta (`fase4_fumaca_q7`); as etapas que a trilha não cronometra
# (detecção, poda, busca e conferência) têm de sair sem tempo e dizendo isso, nunca com tempo estimado.
ETAPAS_DO_PROCESSO = ["roteiro", "deteccao", "poda", "busca", "modelo", "selo"]


def _eventos_da_corrida_curta(parte: str) -> tuple[str, list[dict]]:
    import trilha
    eventos = trilha.ler(RA / "fase4_fumaca_q7" / "trilha_cenarios.jsonl")
    por = trilha.por_trilha(eventos)
    tid = next(t for t in por if t and parte in t)
    return tid, por[tid]


def teste_processo_do_caso_traz_as_seis_etapas_com_o_tempo_gravado_e_diz_o_que_nao_e_cronometrado():
    acervo = hd.Acervo(RA, corridas=("fase4_fumaca_q7", "fase4_ineditos"), descobrir=False)
    tid, eventos = _eventos_da_corrida_curta("contrato-field_missing")
    p = acervo.caso(tid)["processo"]
    etapas = {e["id"]: e for e in p["etapas"]}
    assert [e["id"] for e in p["etapas"]] == ETAPAS_DO_PROCESSO and [e["numero"] for e in p["etapas"]] == [1, 2, 3, 4, 5, 6] and p["tipo"] == "contrato"
    assert [e["feito_por"] for e in p["etapas"]] == ["codigo", "codigo", "codigo", "codigo", "modelo", "codigo"]
    acoes = [e["dados"] for e in eventos if e["tipo"] == "acao" and not e["dados"].get("reexecucao")]
    inferencia = next(e["dados"] for e in eventos if e["tipo"] == "inferencia")
    assert etapas["roteiro"]["tempo_s"] == round(sum(a["tempo_ms"] for a in acoes) / 1000, 2) and etapas["roteiro"]["tempo_gravado"] is True
    assert len(etapas["roteiro"]["detalhe"]["passos"]) == len(acoes) and etapas["roteiro"]["detalhe"]["chamadas"][0]["caminho"] == "/api/produtos"
    assert etapas["modelo"]["tempo_s"] == inferencia["segundos"] and etapas["modelo"]["tempo_gravado"] is True
    assert etapas["modelo"]["detalhe"]["prefill_s"] == round(inferencia["prefill_ms"] / 1000, 1) and etapas["modelo"]["detalhe"]["causa"] == "campo_ausente"
    assert sum(1 for a in etapas["modelo"]["detalhe"]["alternativas"] if a["escolhida"]) == 1
    for sem_tempo in ("deteccao", "poda", "busca", "selo"):
        assert etapas[sem_tempo]["tempo_s"] is None and etapas[sem_tempo]["tempo_gravado"] is False and etapas[sem_tempo]["estado"] == "feita", sem_tempo
    assert "não" in p["tempo_nao_gravado"] and "estim" not in p["tempo_nao_gravado"].lower().replace("sem estim", ""), "a página diz o que falta, não estima"
    poda = next(e["dados"] for e in eventos if e["tipo"] == "poda")
    assert etapas["poda"]["detalhe"]["itens"][0]["antes"] == poda["antes"] and etapas["poda"]["detalhe"]["itens"][0]["depois"] == poda["depois"]
    candidatos = next(e["dados"] for e in eventos if e["tipo"] == "candidatos")
    assert etapas["busca"]["detalhe"]["k"] == candidatos["k"] and sum(1 for v in etapas["busca"]["detalhe"]["verbetes"] if v["entregue"]) == candidatos["k"]
    depois = [e["dados"] for e in eventos if e["tipo"] == "verificacao" and e.get("pai") is not None]
    assert etapas["selo"]["detalhe"]["conferencias"]["total"] == len(depois) and etapas["selo"]["detalhe"]["confianca"] == "alta"
    saidas = {s["id"]: s for s in p["saidas"]}
    assert list(saidas) == ["contrato", "localizador", "aprendizado"] and saidas["contrato"]["estado"] == "saiu" and saidas["localizador"]["estado"] == "nao_se_aplica"
    assert p["trilha"]["eventos"] == len(eventos)
    registros = [json.loads(l) for l in (RA / "fase4_fumaca_q7" / "cenarios.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    registro = next(r for r in registros if r["cenario"] == "contrato-field_missing")
    assert p["cenario"]["mttr_s"] == registro["mttr_s"] and p["cenario"]["task_success"] is registro["task_success"]
    # o localizador: a saída é a cura, com o tempo de reparo que o evento da cura grava
    tid2, eventos2 = _eventos_da_corrida_curta("localizador-front-busca")
    p2 = acervo.caso(tid2)["processo"]
    cura = next(e["dados"] for e in eventos2 if e["tipo"] == "cura")
    s2 = {s["id"]: s for s in p2["saidas"]}
    assert p2["tipo"] == "localizador" and s2["localizador"]["estado"] == "saiu" and s2["localizador"]["tempo_s"] == cura["mttr_s"] and s2["localizador"]["detalhe"]["curado"] is True
    assert s2["contrato"]["estado"] == "nao_se_aplica" and {e["id"]: e for e in p2["etapas"]}["deteccao"]["detalhe"]["erro"]
    # caso em texto: não houve roteiro, detecção nem poda, e a página não inventa essas etapas
    texto = next(l["tid"] for l in acervo.indice() if l["corrida"] == "fase4_ineditos")
    p3 = acervo.caso(texto)["processo"]
    e3 = {e["id"]: e for e in p3["etapas"]}
    assert p3["tipo"] == "texto" and [e3[x]["estado"] for x in ("roteiro", "deteccao", "poda")] == ["nao_se_aplica"] * 3 and e3["modelo"]["estado"] == "feita" and p3["cenario"] is None


def teste_rede_do_caso_liga_os_sinais_os_verbetes_e_as_causas():
    acervo = hd.Acervo(RA, corridas=("fase4_fumaca_q7",), descobrir=False)
    tid, eventos = _eventos_da_corrida_curta("contrato-field_missing")
    caso = acervo.caso(tid)
    rede = caso["processo"]["rede"]
    assert [c["id"] for c in rede["camadas"]] == ["sinais", "verbetes", "causas", "resultado"]
    nos = {n["id"]: n for c in rede["camadas"] for n in c["nos"]}
    assert all(a["de"] in nos and a["para"] in nos and 0 <= a["peso"] <= 1 for a in rede["arestas"]) and len(rede["arestas"]) >= 5
    decisao_causa = next(d for d in caso["arvore"]["decisoes"] if d["chave"] == "causa")
    causas = next(c for c in rede["camadas"] if c["id"] == "causas")["nos"]
    assert [n["valor"] for n in causas] == [a["probabilidade"] for a in decisao_causa["alternativas"]][:len(causas)]
    assert [n["rotulo"] for n in causas if n["destaque"]] == ["campo_ausente"]
    verbetes = next(c for c in rede["camadas"] if c["id"] == "verbetes")["nos"]
    candidatos = next(e["dados"] for e in eventos if e["tipo"] == "candidatos")
    assert sum(1 for n in verbetes if n["destaque"]) == candidatos["k"], "os verbetes entregues ao modelo vêm destacados"
    assert any(a["de"] == "c-campo_ausente" and a["para"] == "r-causa" for a in rede["arestas"]), "a causa escolhida liga ao resultado"
    # o caso de teste (sem cura) também monta a rede, e o localizador curado ganha o nó da cura
    acervo_t, _ = _acervo_de_teste()
    for linha in acervo_t.indice():
        assert len(acervo_t.caso(linha["tid"])["processo"]["rede"]["camadas"]) == 4
    tid2, _ = _eventos_da_corrida_curta("localizador-front-busca")
    resultado = next(c for c in acervo.caso(tid2)["processo"]["rede"]["camadas"] if c["id"] == "resultado")["nos"]
    assert [n["id"] for n in resultado] == ["r-causa", "r-cura"]


def teste_ao_vivo_diz_a_etapa_em_andamento_e_traz_o_processo_do_ultimo_caso():
    acervo, raiz = _acervo_de_teste()
    th._estado_da_barra(raiz / "c2", estado="determinado", fracao=0.4)
    with _hub_no_ar(acervo) as (base, _, _srv):
        v = _json(base, "GET", "/api/ao-vivo")[1]
        assert v["em_andamento"] is True and v["etapa_agora"] == "modelo" and v["caso_agora"] == "lex-4@tela", (v["etapa_agora"], v.get("caso_agora"))
        assert [e["id"] for e in v["ultimo_diagnostico"]["processo"]["etapas"]] == ETAPAS_DO_PROCESSO
        th._estado_da_barra(raiz / "c2", estado="concluido", fracao=1.0)
        v = _json(base, "GET", "/api/ao-vivo")[1]
        assert v["em_andamento"] is False and v["etapa_agora"] is None, "fora da inferência a corrida não grava em que etapa está: a página não acende nenhuma"


def teste_pagina_molde_visual_mostra_os_diagramas_no_lugar_do_texto():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_de_teste()
        th._estado_da_barra(raiz / "c2", estado="determinado", fracao=0.4)
        with _hub_no_ar(acervo, sonda=lambda porta: porta == 8080, ollama_no_ar=lambda: True) as (base, _, _srv):
            pagina.goto(base + "/")
            # o início: o diagrama dos espaços de trabalho, com o que está no ar aceso
            pagina.wait_for_selector("#workspaces svg .no")
            assert pagina.locator("#workspaces svg .no").count() >= 8 and pagina.locator("#workspaces svg .ligacao").count() >= 7
            assert pagina.locator('#workspaces svg .no[data-no="site"].no-ar').count() == 1 and pagina.locator('#workspaces svg .no[data-no="api"].fora-do-ar').count() == 1
            assert pagina.locator('#workspaces svg .no[data-no="ollama"].no-ar').count() == 1
            # a lista: um grupo por corrida, com a legenda que explica cada campo
            assert pagina.locator("#lista-de-casos .grupo-de-casos").count() == 2 and pagina.locator("#lista-de-casos .item-caso:visible").count() == 3
            assert pagina.is_hidden("#legenda-da-lista")
            pagina.click("#abrir-legenda")
            legenda = pagina.inner_text("#legenda-da-lista").lower()
            assert all(palavra in legenda for palavra in ("corrida", "iteração", "confiança", "divergência", "cura", "veredito")), legenda
            pagina.click('#lista-de-casos .cabeca-do-grupo[data-corrida="c2"]')
            assert pagina.locator("#lista-de-casos .item-caso:visible").count() == 1, "fechar o grupo esconde os casos dele"
            pagina.click('#lista-de-casos .cabeca-do-grupo[data-corrida="c2"]')
            # o caso: a linha de produção dele, com o tempo de cada etapa e o cartão que amplia
            pagina.click('#lista-de-casos .item-caso[data-tid="c2/qwen2.5_7b/lex-4@tela"]')
            pagina.wait_for_selector("#processo-do-caso svg .etapa")
            assert pagina.locator("#processo-do-caso svg .etapa").count() == 6 and pagina.locator("#processo-do-caso svg .saida").count() == 3
            assert pagina.locator('#processo-do-caso svg .etapa[data-etapa="modelo"].feita').count() == 1
            assert " s" in pagina.locator('#processo-do-caso svg .etapa[data-etapa="modelo"] .tempo').text_content()
            assert "sem tempo" in pagina.locator('#processo-do-caso svg .etapa[data-etapa="poda"] .tempo').text_content()
            assert pagina.is_hidden("#zoom-da-etapa")
            pagina.click('#processo-do-caso svg .etapa[data-etapa="modelo"]')
            pagina.wait_for_selector("#zoom-da-etapa:visible")
            assert "resposta_truncada" in pagina.inner_text("#zoom-da-etapa") and pagina.locator("#zoom-da-etapa .barra-h").count() >= 2
            pagina.click("#fechar-zoom")
            assert pagina.is_hidden("#zoom-da-etapa")
            pagina.click('#processo-do-caso svg .etapa[data-etapa="busca"]')
            pagina.wait_for_selector("#zoom-da-etapa:visible")
            assert pagina.locator("#zoom-da-etapa .barra-h").count() >= 3, "os verbetes aparecem como barras da pontuação"
            pagina.keyboard.press("Escape")
            assert pagina.is_hidden("#zoom-da-etapa")
            # a árvore de decisão: a rede no lugar do texto corrido, que fica recolhido
            pagina.click('button[data-aba="arvore"]')
            pagina.wait_for_selector("#rede-da-decisao svg .no")
            assert pagina.locator("#rede-da-decisao svg .no").count() >= 6 and pagina.locator("#rede-da-decisao svg .aresta").count() >= 2
            assert pagina.locator("#rede-da-decisao svg .no.destaque").count() >= 2
            assert pagina.locator("#aba-arvore details.por-escrito").count() == 1 and pagina.locator("#aba-arvore .decisao").count() == 3
            assert pagina.locator("#aba-arvore .decisao:visible").count() == 0, "o texto corrido só aparece quando o analista pede"
            # a corrida ao vivo: a linha de produção com a etapa do modelo acesa
            pagina.click("#abrir-ao-vivo")
            pagina.wait_for_selector('#linha-de-producao svg .etapa[data-etapa="modelo"].em-andamento')
            assert pagina.locator("#linha-de-producao svg .etapa.em-andamento").count() == 1
            assert "lex-4@tela" in pagina.inner_text("#caso-ao-vivo")
            th._estado_da_barra(raiz / "c2", estado="concluido", fracao=1.0)
            pagina.wait_for_selector('#linha-de-producao svg .etapa[data-etapa="modelo"].feita', timeout=8000)
            assert pagina.locator("#linha-de-producao svg .etapa.em-andamento").count() == 0
        assert erros == [], erros


def teste_pagina_molde_visual_lista_longa_fica_em_grupos_e_metricas_em_graficos():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo = hd.Acervo(RA, descobrir=False)
        with _hub_no_ar(acervo) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#lista-de-casos .item-caso")
            total = len(acervo.indice())
            assert pagina.locator("#lista-de-casos .item-caso").count() == total and pagina.locator("#lista-de-casos .grupo-de-casos").count() == len(hd.CORRIDAS_PADRAO)
            visiveis = pagina.locator("#lista-de-casos .item-caso:visible").count()
            assert 0 < visiveis <= 15, f"sem filtro, a lista abre só um grupo e mostra poucos casos por vez ({visiveis} de {total})"
            pagina.click("#lista-de-casos .mostrar-mais:visible")
            assert visiveis < pagina.locator("#lista-de-casos .item-caso:visible").count() <= 30
            pagina.fill("#filtro-texto", "campo")
            achados = pagina.locator("#lista-de-casos .item-caso:visible").count()
            assert achados > 30, "com a busca, aparecem todos os que batem, de todos os grupos"
            pagina.fill("#filtro-texto", "")
            # as métricas: gráficos no lugar da tabela, que fica recolhida
            pagina.click("#abrir-metricas")
            pagina.wait_for_selector("#metricas svg .barra-da-corrida")
            m = hd.metricas(acervo)
            com_cenarios = [c for c in m["corridas"] if c["execucoes"]]
            assert pagina.locator("#grafico-do-reparo svg .barra-da-corrida").count() == len(com_cenarios)
            assert pagina.locator("#grafico-da-fase-5 svg .barra-do-lado").count() == 2
            texto = pagina.locator("#grafico-da-fase-5").text_content()
            assert "66,3" in texto and "219,7" in texto, texto
            assert pagina.locator("#metricas details.tabela-recolhida tr.corrida").count() == len(m["corridas"]) and pagina.locator("#metricas tr.corrida:visible").count() == 0
            pagina.click('#grafico-do-reparo svg .barra-da-corrida[data-corrida="fase5_agente_b"]')
            pagina.wait_for_selector("#grafico-dos-cenarios svg .barra-do-cenario")
            assert pagina.locator("#grafico-dos-cenarios svg .barra-do-cenario").count() == 10
            assert pagina.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"), "sem rolagem lateral"
        assert erros == [], erros


# ! Alteração de IA - Revisar: (26/11/2026) teste novo, escrito antes do código: `hub.prova_do_botao` resume as corridas lançadas pelo botão do hub
# (uma linha por pasta `hub_<data>_<hora>` com `cenarios.jsonl`), e `hub.py --botao [--check]` grava o resumo em `resultados_alvo/fase4/botao_do_hub`.
# ! Motivo: o Eric rodou os cenários pelo botão em 26/11/2026, e as pastas dessas corridas ficam fora do git (decisão 171); sem um derivado
# versionado, o roadmap, o painel e o texto do TCC não teriam de onde ler que o botão rodou com o modelo. Numa cópia do repositório sem as pastas,
# o `--check` não pode acusar diferença: ele só confere quando há o que ler.
def teste_prova_do_botao_resume_as_corridas_do_hub_e_nao_acusa_diferenca_sem_as_pastas():
    import contextlib
    import io
    _, raiz = _acervo_que_descobre()
    vazio, _ = hub.prova_do_botao(raiz)
    assert vazio["corridas"] == [] and vazio["total"] == 0
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        assert hub.main(["--botao", "--check", "--resultados", str(raiz)]) == 0, "sem pasta do botão nesta cópia, não há o que conferir"
    assert "hub_" in saida.getvalue() and not (raiz / "fase4" / "botao_do_hub.json").exists()
    _corrida_do_hub(raiz)
    dado, md = hub.prova_do_botao(raiz)
    linha = dado["corridas"][0]
    assert dado["total"] == 1 and linha["pasta"] == "hub_20261125_230000" and (linha["execucoes"], linha["cenarios"], linha["task_success"], linha["detectou"]) == (2, 2, 1, 2), linha
    assert "1 de 2" in md and "decisão 171" in md and "não é medida" in md.replace("não medida", "não é medida")
    assert (linha["marcas"], linha["casos_com_o_tempo_das_seis_etapas"]) == (0, 0) and "gravou a hora de cada etapa" not in md, "corrida sem as marcas: o resumo não diz que elas foram gravadas"
    _gravar_marcas(raiz / "hub_20261125_230000", [("contrato-field_missing#1", e, t) for _, e, t in MARCAS_DE_UM_CASO] + [("localizador-front-busca#1", "roteiro", 180.0)])
    com_marcas, md_com_marcas = hub.prova_do_botao(raiz)
    assert (com_marcas["corridas"][0]["marcas"], com_marcas["corridas"][0]["casos_com_o_tempo_das_seis_etapas"]) == (9, 1), com_marcas["corridas"][0]
    assert "gravou a hora de cada etapa" in md_com_marcas and "1 de 2" in md_com_marcas and "decisão 176" in md_com_marcas
    (raiz / "hub_20261125_230000" / "etapas_ao_vivo.jsonl").unlink()
    with contextlib.redirect_stdout(io.StringIO()):
        assert hub.main(["--botao", "--resultados", str(raiz)]) == 0 and hub.main(["--botao", "--check", "--resultados", str(raiz)]) == 0
    assert json.loads((raiz / "fase4" / "botao_do_hub.json").read_text(encoding="utf-8"))["corridas"][0]["task_success"] == 1
    (raiz / "hub_20261125_230000" / "cenarios.jsonl").write_text("", encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()):
        assert hub.main(["--botao", "--check", "--resultados", str(raiz)]) == 1, "se o registro da corrida muda, o --check acusa"
    # o derivado gravado bate com as pastas que existem nesta máquina
    gravado = RA / "fase4" / "botao_do_hub.json"
    assert gravado.exists(), "rode `python hub.py --botao` para gravar o resumo das corridas do botão"
    if any(RA.glob("hub_*/cenarios.jsonl")):
        with contextlib.redirect_stdout(io.StringIO()):
            assert hub.main(["--botao", "--check"]) == 0


# ------------------------------------------------------------------ a hora de cada etapa (ficha 114, decisão 176)
# ! Alteração de IA - Revisar: (26/11/2026, ficha 114, decisão 176) testes novos, escritos antes do código: as marcas da hora de cada etapa
# (`etapas_ao_vivo.py`), desligadas por padrão; a opção `--etapas-ao-vivo` do executor e os pontos em que ele e o diagnóstico marcam; o tempo das
# seis etapas no processo do caso quando a corrida gravou as marcas; a etapa acesa ao vivo, qualquer que seja; e a página.
# ! Motivo: o Eric respondeu a ficha 114 pela opção (a): gravar a hora de cada etapa só nas corridas lançadas pelo botão do hub. O que os testes
# seguram é o que a decisão promete: sem a opção, nenhuma linha é gravada; com ela, o tempo de cada etapa é a diferença entre duas marcas do
# mesmo caso, e não uma estimativa; e uma corrida sem marcas continua mostrando "sem tempo gravado".
def _gravar_marcas(pasta: Path, marcas: list[tuple], idade_s: float = 0.0, pid: int = 4242) -> Path:
    """Grava um `etapas_ao_vivo.jsonl` como a corrida grava: uma linha por marca, com o caso, a etapa e o relógio."""
    import os
    import time
    arq = pasta / "etapas_ao_vivo.jsonl"
    arq.write_text("".join(json.dumps({"caso": caso, "etapa": etapa, "t": t, "ts": "2026-11-26T09:00:00", "pid": pid}) + "\n" for caso, etapa, t in marcas), encoding="utf-8")
    quando = time.time() - idade_s
    os.utime(arq, (quando, quando))
    return arq


MARCAS_DE_UM_CASO = [("lex-4@tela", "roteiro", 100.0), ("lex-4@tela", "deteccao", 101.5), ("lex-4@tela", "poda", 101.7), ("lex-4@tela", "busca", 102.0),
                     ("lex-4@tela", "modelo", 102.4), ("lex-4@tela", "selo", 172.4), ("lex-4@tela", "saida", 172.9), ("lex-4@tela", "fim", 173.0)]


def teste_marcas_das_etapas_vem_desligadas_e_so_gravam_quando_a_corrida_pede():
    import diagnostico_ao_vivo as dv
    import etapas_ao_vivo as ea
    import executar_fase4 as ex
    pasta = tp4._temp()
    assert ea.ligado() is False, "desligado por padrão: a corrida de medida não grava nem cronometra nada"
    ea.marcar("roteiro", "x#1")
    assert not list(pasta.iterdir()) and ea.ler(pasta) == []
    try:
        arq = ea.ligar(pasta)
        assert ea.ligado() is True and arq == pasta / ea.NOME_DO_ARQUIVO
        for etapa in ("roteiro", "deteccao", "poda"):
            ea.marcar(etapa, "x#1")
        marcas = ea.ler(pasta)
        assert [(m["caso"], m["etapa"]) for m in marcas] == [("x#1", "roteiro"), ("x#1", "deteccao"), ("x#1", "poda")]
        assert marcas[0]["t"] <= marcas[1]["t"] <= marcas[2]["t"] and all(m["pid"] == marcas[0]["pid"] and m["ts"] for m in marcas)
        assert _erro(ea.marcar, "etapa_que_nao_existe", "x#1")
    finally:
        ea.desligar()
    ea.marcar("busca", "x#1")
    assert ea.ligado() is False and len(ea.ler(pasta)) == 3, "depois de desligar, nada mais é gravado"
    # a conta: a diferença entre duas marcas seguidas do mesmo caso e do mesmo processo; a última marca de um caso fica sem tempo
    tempos = ea.tempos_por_caso([{"caso": c, "etapa": e, "t": t, "pid": 1} for c, e, t in MARCAS_DE_UM_CASO] + [{"caso": "outro#1", "etapa": "roteiro", "t": 173.2, "pid": 1}])
    assert {k: round(v, 3) for k, v in tempos["lex-4@tela"].items()} == {"roteiro": 1.5, "deteccao": 0.2, "poda": 0.3, "busca": 0.4, "modelo": 70.0, "selo": 0.5, "saida": 0.1}
    assert tempos.get("outro#1", {}) == {}, "a etapa que ainda não terminou não tem tempo"
    de_outro_processo = ea.tempos_por_caso([{"caso": "x#1", "etapa": "roteiro", "t": 10.0, "pid": 1}, {"caso": "x#1", "etapa": "deteccao", "t": 3.0, "pid": 2}])
    assert de_outro_processo.get("x#1", {}) == {}, "marcas de processos diferentes (corrida retomada) não se subtraem"
    (pasta / ea.NOME_DO_ARQUIVO).write_text('{"caso": "x#1", "etapa": "roteiro", "t": 1.0, "pid": 1}\n{"caso": "x#1", "eta', encoding="utf-8")
    assert len(ea.ler(pasta)) == 1, "a linha pela metade (corrida gravando) é pulada"
    # o executor: a opção vem desligada, liga as marcas só quando pedida, e os seis pontos estão onde cada etapa começa
    padrao = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "qualquer"])
    assert padrao.etapas_ao_vivo is False and ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "q", "--etapas-ao-vivo"]).etapas_ao_vivo is True
    cenarios = inspect.getsource(ex.rodar_cenarios)
    assert "if args.etapas_ao_vivo:" in cenarios and "ea.ligar(saida)" in cenarios and "ea.desligar()" in cenarios
    assert 'ea.marcar("saida"' in cenarios and 'ea.marcar("fim"' in cenarios
    for fonte, etapas in ((inspect.getsource(ex.Tela.rodar_caso), ("roteiro", "deteccao", "poda")), (inspect.getsource(ex.Cura.executar), ("roteiro", "deteccao", "poda", "saida")),
                          (inspect.getsource(dv.diagnosticar), ("busca", "modelo", "selo"))):
        posicoes = [fonte.index(f'ea.marcar("{e}"') for e in etapas]
        assert posicoes == sorted(posicoes), etapas
    assert "--etapas-ao-vivo" in hub.comando_direto("hub_x", {"repeticoes": 1, "selecao": "todos", "desde": None}) and "--etapas-ao-vivo" not in " ".join(hub.comando_padrao("hub_x", {"repeticoes": 1}))


def teste_processo_usa_as_marcas_para_o_tempo_das_seis_etapas():
    acervo, raiz = _acervo_de_teste()
    tid = "c2/qwen2.5_7b/lex-4@tela"
    antes = {e["id"]: e for e in acervo.caso(tid)["processo"]["etapas"]}
    assert antes["poda"]["tempo_s"] is None and antes["poda"]["tempo_de"] is None and antes["modelo"]["tempo_de"] == "trilha"
    _gravar_marcas(raiz / "c2", MARCAS_DE_UM_CASO)
    p = acervo.caso(tid)["processo"]
    etapas = {e["id"]: e for e in p["etapas"]}
    assert {i: e["tempo_s"] for i, e in etapas.items()} == {"roteiro": 1.5, "deteccao": 0.2, "poda": 0.3, "busca": 0.4, "modelo": 70.0, "selo": 0.5}, {i: e["tempo_s"] for i, e in etapas.items()}
    assert all(e["tempo_gravado"] and e["tempo_de"] == "marcas" for e in etapas.values()) and p["tempo_nao_gravado"] is None
    assert etapas["modelo"]["tempo_pela_trilha_s"] == antes["modelo"]["tempo_s"] and etapas["roteiro"]["tempo_pela_trilha_s"] == antes["roteiro"]["tempo_s"]
    assert etapas["poda"]["tempo_pela_trilha_s"] is None
    outro = acervo.caso("c2/qwen2.5_7b/lex-1@tela")["processo"]
    assert {e["id"]: e for e in outro["etapas"]}["poda"]["tempo_s"] is None and outro["tempo_nao_gravado"], "o caso sem marcas continua sem tempo, e a página diz por quê"
    de_antes = acervo.caso("c1/qwen2.5_7b/lex-1@tela")["processo"]
    assert de_antes["tempo_nao_gravado"] and all(e["tempo_de"] != "marcas" for e in de_antes["etapas"]), "a corrida antiga, sem o arquivo, não muda"


def teste_ao_vivo_acende_qualquer_etapa_quando_a_corrida_grava_as_marcas():
    acervo, raiz = _acervo_de_teste()
    em_curso = [("lex-9@tela", "roteiro", 200.0), ("lex-9@tela", "deteccao", 201.2), ("lex-9@tela", "poda", 201.3), ("lex-9@tela", "busca", 201.8)]
    _gravar_marcas(raiz / "c2", MARCAS_DE_UM_CASO + em_curso)
    with _hub_no_ar(acervo) as (base, _, _srv):
        v = _json(base, "GET", "/api/ao-vivo")[1]
        assert v["ha_corrida"] is True and v["pasta"] == "c2" and v["em_andamento"] is True, v
        assert v["etapa_agora"] == "busca" and v["caso_agora"] == "lex-9@tela" and v["tempos_agora"] == {"roteiro": 1.2, "deteccao": 0.1, "poda": 0.5}, (v["etapa_agora"], v["tempos_agora"])
        _gravar_marcas(raiz / "c2", MARCAS_DE_UM_CASO + em_curso + [("lex-9@tela", "modelo", 202.0)])
        th._estado_da_barra(raiz / "c2", estado="determinado", fracao=0.5, etapa="lex-9@tela · diagnóstico")
        v = _json(base, "GET", "/api/ao-vivo")[1]
        assert v["etapa_agora"] == "modelo" and v["caso_agora"] == "lex-9@tela" and v["tempos_agora"]["busca"] == 0.2
        th._estado_da_barra(raiz / "c2", estado="concluido", fracao=1.0, etapa="lex-9@tela · diagnóstico")
        _gravar_marcas(raiz / "c2", MARCAS_DE_UM_CASO + em_curso + [("lex-9@tela", "modelo", 202.0), ("lex-9@tela", "selo", 270.0), ("lex-9@tela", "saida", 270.4)])
        v = _json(base, "GET", "/api/ao-vivo")[1]
        assert v["etapa_agora"] == "saida" and v["em_andamento"] is True
        _gravar_marcas(raiz / "c2", MARCAS_DE_UM_CASO + em_curso + [("lex-9@tela", "fim", 271.0)])
        v = _json(base, "GET", "/api/ao-vivo")[1]
        assert v["etapa_agora"] is None and v["em_andamento"] is False, "o caso terminou: nenhuma etapa acesa"
        _gravar_marcas(raiz / "c2", MARCAS_DE_UM_CASO + em_curso, idade_s=120)
        v = _json(base, "GET", "/api/ao-vivo")[1]
        assert v["etapa_agora"] is None, "marca parada há mais de meio minuto fora da inferência: a corrida morreu ou parou, e nada fica aceso"


def teste_pagina_ao_vivo_acende_a_etapa_marcada_e_mostra_o_tempo_das_que_ja_passaram():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_de_teste()
        _gravar_marcas(raiz / "c2", MARCAS_DE_UM_CASO + [("lex-9@tela", "roteiro", 200.0), ("lex-9@tela", "deteccao", 201.2), ("lex-9@tela", "poda", 201.3)])
        with _hub_no_ar(acervo) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#lista-de-casos .item-caso")
            pagina.click("#abrir-ao-vivo")
            pagina.wait_for_selector('#linha-de-producao svg .etapa[data-etapa="poda"].em-andamento')
            assert pagina.locator("#linha-de-producao svg .etapa.em-andamento").count() == 1 and "lex-9@tela" in pagina.inner_text("#caso-ao-vivo")
            assert "1,2 s" in pagina.locator('#linha-de-producao svg .etapa[data-etapa="roteiro"] .tempo').text_content()
            assert "100 ms" in pagina.locator('#linha-de-producao svg .etapa[data-etapa="deteccao"] .tempo').text_content()
            pagina.click('#linha-de-producao svg .etapa[data-etapa="roteiro"]')
            pagina.wait_for_selector("#zoom-da-etapa:visible")
            assert "quando o caso terminar" in pagina.inner_text("#zoom-da-etapa"), "o cartão de uma etapa do caso em andamento não mostra detalhe de outro caso"
            pagina.click("#fechar-zoom")
            # o caso que a corrida já gravou mostra o tempo das seis etapas, e o cartão ampliado diz o que cada tempo cobre
            pagina.click('#lista-de-casos .item-caso[data-tid="c2/qwen2.5_7b/lex-4@tela"]')
            pagina.wait_for_selector("#processo-do-caso svg .etapa")
            assert "300 ms" in pagina.locator('#processo-do-caso svg .etapa[data-etapa="poda"] .tempo').text_content()
            assert pagina.locator("#processo-do-caso svg .etapa.sem-tempo").count() == 0 and pagina.locator("#resumo-do-processo details.nota-do-tempo").count() == 0
            pagina.click('#processo-do-caso svg .etapa[data-etapa="modelo"]')
            pagina.wait_for_selector("#zoom-da-etapa:visible")
            texto = pagina.inner_text("#zoom-da-etapa")
            assert "relógio da corrida" in texto and "pela trilha" in texto, texto[:400]
        assert erros == [], erros


# ! Alteração de IA - Revisar: (26/11/2026, ficha 114, decisão 176) teste do diagnóstico de verdade com um modelo de mentira (o ajudante de
# `testar_fase4.py`): com as marcas ligadas, `diagnosticar` grava a busca, o modelo e a conferência, nessa ordem; e, ligadas ou desligadas, a
# resposta, o pedido enviado ao modelo, a causa escolhida e os eventos da trilha são os mesmos.
# ! Motivo: as marcas entraram dentro do diagnóstico que as corridas 18d, 21d e 28b mediram. O teste segura a promessa da decisão: desligadas,
# nada é gravado; ligadas, o diagnóstico continua respondendo a mesma coisa. Nenhum modelo de verdade é chamado.
def teste_diagnostico_marca_a_busca_o_modelo_e_a_conferencia_sem_mudar_o_que_responde():
    import caso_ao_vivo as cv
    import diagnostico_ao_vivo as dv
    import etapas_ao_vivo as ea
    import testar_fase4 as tf4
    verbetes, indice = tf4._curada()
    caso = cv.montar_caso("localizador-front-admin-login@cenario", "GET admin/login.php", 200, "(página PHP do front legado: sem contrato de API)",
                          "(HTML da página; nenhuma chamada à API falhou)", "o roteiro parou no passo 5", arvore='- button "Entrar"', seletor_quebrado="button.btn-primary")
    resposta = ("O localizador não acha o botão.\nCAUSA_RAIZ: localizador_quebrado\nCAMPO: nenhum\nIMPACTO: o roteiro para no login.\nFONTE: [localizador_quebrado]",
                .9, [(" tempo_de_resposta_excedido", .05)])

    def rodar() -> tuple[dict, list, str, list]:
        t, tid, _ = tf4._trilha_de_cura()
        enviados: list = []
        with tf4._ollama_de_mentira_v2(lambda _p, _c: resposta, enviados):
            saida = dv.diagnosticar(t, tid, caso, verbetes, indice, k=3, modelo="qwen2.5:7b", comum=tf4._comum_de_teste(), limiares=None, intervencoes="desligadas",
                                    evidencia=[], ts=tf4.TS)
        return saida, [(e["tipo"], json.dumps(e["dados"], sort_keys=True, ensure_ascii=False)) for e in t.eventos if e.get("trilha") == tid], tid, [c["prompt"] for c in enviados]

    pasta = tp4._temp()
    assert ea.ligado() is False
    sem, eventos_sem, tid, pedidos_sem = rodar()
    assert ea.ler(pasta) == [] and not list(pasta.iterdir()), "desligadas, nenhuma marca é gravada"
    try:
        ea.ligar(pasta)
        com, eventos_com, _, pedidos_com = rodar()
    finally:
        ea.desligar()
    marcas = ea.ler(pasta)
    assert [(m["caso"], m["etapa"]) for m in marcas] == [(tid.rsplit("/", 1)[-1], e) for e in ("busca", "modelo", "selo")], marcas
    assert pedidos_com == pedidos_sem and len(pedidos_sem) == 1, "o pedido enviado ao modelo é o mesmo"
    assert com["registro"]["resposta"] == sem["registro"]["resposta"] and com["prompt_sha256"] == sem["prompt_sha256"] and com["no"]["escolha"] == sem["no"]["escolha"]
    assert eventos_com == eventos_sem, "os eventos da trilha são os mesmos com as marcas ligadas e desligadas"


# ------------------------------------------------------------------ o painel local aberto pelo hub
# ! Alteração de IA - Revisar: (26/11/2026) testes novos, escritos antes do código: o hub serve o painel do projeto desta máquina em `/painel`
# (o arquivo `Documentacao/dashboard/painel-do-projeto.html`), isolado da página do hub; `/api/central` diz se o arquivo existe e se ele foi gerado
# antes da última mudança nas fichas, no roadmap ou nas decisões; e, na página, "Abrir o painel do projeto" leva a esse endereço, e não ao painel
# publicado no claude.ai. O último teste abre o painel de verdade com a internet barrada e confere que as abas trocam.
# ! Motivo: o Eric aprovou o molde do hub e pediu uma coisa só: o botão do painel tem de abrir o HTML local, e esse local tem de estar em dia. O
# painel traz script e estilo embutidos, que a página do hub não aceita, e por isso sai com regras próprias e sem acesso ao que o hub grava.
def _painel_de_mentira(raiz: Path, texto: str = "<!doctype html><title>Painel de teste</title><p id=p>painel local</p>") -> tuple[Path, tuple]:
    import os
    import time
    painel = raiz / "painel-de-teste.html"
    painel.write_text(texto, encoding="utf-8")
    fontes = tuple(raiz / nome for nome in ("pendencias.md", "roadmap.md", "decisoes.md"))
    for i, fonte in enumerate(fontes):
        fonte.write_text("fonte", encoding="utf-8")
        os.utime(fonte, (time.time() - 600 - i, time.time() - 600 - i))        # as fontes são de dez minutos atrás: o painel está em dia
    return painel, fontes


def teste_hub_serve_o_painel_local_isolado_e_diz_se_ele_esta_atrasado():
    import os
    import time
    acervo, raiz = _acervo_de_teste()
    painel, fontes = _painel_de_mentira(raiz)
    with _hub_no_ar(acervo, painel=painel, fontes_do_painel=fontes) as (base, _, _srv):
        c = _json(base, "GET", "/api/central")[1]["painel"]
        assert c["url"] == "/painel" and c["existe"] is True and c["atrasado"] is False and c["fonte_mais_nova"] is None and c["gerado_em"], c
        status, cabecalhos, corpo = _http(base, "GET", "/painel")
        assert status == 200 and corpo == painel.read_bytes() and cabecalhos["content-type"].startswith("text/html")
        regras = cabecalhos["content-security-policy"]
        assert "sandbox" in regras and "connect-src 'none'" in regras and "default-src 'none'" in regras, regras
        assert "'unsafe-inline'" in regras and regras != _http(base, "GET", "/")[1]["content-security-policy"], "o painel tem regras próprias; a página do hub continua sem script embutido"
        assert "allow-same-origin" not in regras, "o painel não entra na origem do hub: ele não lê nem grava nada do que o hub serve"
        os.utime(fontes[1], (time.time() + 5, time.time() + 5))
        c = _json(base, "GET", "/api/central")[1]["painel"]
        assert c["atrasado"] is True and c["fonte_mais_nova"] == "roadmap.md", c
        painel.unlink()
        c = _json(base, "GET", "/api/central")[1]["painel"]
        assert c["existe"] is False and c["atrasado"] is False and c["gerado_em"] is None
        status, r = _json(base, "GET", "/painel")
        assert status == 404 and "gerar_dashboard.py" in r["erro"], r
    assert hub.PAINEL_LOCAL.name == "painel-do-projeto.html" and hub.PAINEL_LOCAL.parent.name == "dashboard" and len(hub.FONTES_DO_PAINEL) == 3
    assert all(f.exists() for f in hub.FONTES_DO_PAINEL), "as três fontes que o aviso olha existem no repositório"
    assert not hasattr(hub, "PAINEL_PUBLICADO"), "o hub não aponta mais para o painel publicado fora da máquina"


def teste_pagina_abre_o_painel_local_e_avisa_quando_ele_esta_atrasado():
    import os
    import time
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_de_teste()
        painel, fontes = _painel_de_mentira(raiz)
        with _hub_no_ar(acervo, painel=painel, fontes_do_painel=fontes) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#inicio .servico")
            assert pagina.get_attribute("#inicio a.painel", "href") == "/painel" and pagina.get_attribute("#inicio a.painel", "target") == "_blank"
            assert "claude.ai" not in pagina.inner_html("#inicio"), "nada na tela inicial leva ao painel publicado fora da máquina"
            # ! Alteração de IA - Revisar: (26/11/2026, ficha 116, decisão 178) conferência nova, escrita antes da troca do texto: a nota ao lado do
            # atalho do painel diz que ele funciona sem internet e não diz mais que os gráficos ficam de fora.
            # ! Motivo: a nota dizia "sem internet ... os gráficos do painel não"; com a biblioteca de gráficos embutida no painel, isso deixou de ser
            # verdade, e quem lê a tela "Início" do hub acharia que os gráficos ainda dependem da rede.
            nota_do_painel = pagina.inner_text("#inicio .atalho:has(a.painel) p.nota")
            assert "sem internet" in nota_do_painel and "gráficos do painel não" not in nota_do_painel, nota_do_painel
            assert pagina.is_hidden("#aviso-do-painel")
            with pagina.context.expect_page() as nova:
                pagina.click("#inicio a.painel")
            aberta = nova.value
            aberta.wait_for_selector("#p")
            assert aberta.url == base + "/painel" and aberta.inner_text("#p") == "painel local"
            aberta.close()
            os.utime(fontes[0], (time.time() + 5, time.time() + 5))
            pagina.reload()
            pagina.wait_for_selector("#aviso-do-painel:visible")
            aviso = pagina.inner_text("#aviso-do-painel")
            assert "pendencias.md" in aviso and "gerar_dashboard.py" in aviso, aviso
        assert erros == [], erros


def teste_painel_do_projeto_abre_pelo_hub_e_desenha_os_graficos_sem_internet():
    # (26/11/2026, ficha 116) o teste passou a exigir os gráficos: a biblioteca vai embutida no painel, e nenhum pedido dela sai para a internet
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, _ = _acervo_de_teste()
        assert hub.PAINEL_LOCAL.exists(), "rode `python ferramentas/gerar_dashboard.py` para gerar o painel"
        with _hub_no_ar(acervo) as (base, _, _srv):
            barrados: list = []

            def barrar(rota) -> None:
                if rota.request.url.startswith(base):
                    rota.continue_()
                else:
                    barrados.append(rota.request.url)
                    rota.abort()

            pagina.route("**/*", barrar)
            pagina.goto(base + "/painel")
            pagina.wait_for_selector("section#inicio")
            pagina.wait_for_timeout(500)
            assert not any("chart" in u.lower() or "jsdelivr" in u.lower() for u in barrados), "o painel não pede mais a biblioteca de gráficos à internet: " + str(barrados)
            assert pagina.evaluate("typeof Chart") == "function", "a biblioteca embutida carregou com a internet barrada"
            # o clique vai pelo programa da página: no painel, o atalho de uma aba pode estar dentro de um menu recolhido
            pagina.evaluate("""document.querySelector('a[href="#pendencias"]').click()""")
            pagina.wait_for_selector("section#pendencias:visible")
            assert pagina.is_hidden("section#inicio")
            pagina.evaluate("""document.querySelector('a[href="#hub"]').click()""")
            pagina.wait_for_selector("section#hub:visible")
            pagina.wait_for_timeout(600)
            desenhados = pagina.evaluate("[...document.querySelectorAll('section#hub canvas')].map(c => c.width > 300 && !c.hidden)")
            assert desenhados and all(desenhados), "os gráficos da aba são desenhados sem internet: " + str(desenhados)
            assert pagina.locator("p.sem-chart").count() == 0, "nenhum gráfico virou aviso"
        de_script = [e for e in erros if "Failed to load resource" not in e and "ERR_FAILED" not in e]
        assert de_script == [], de_script


# ------------------------------------------------------------------ a coletânea de erros sorteados para a banca (decisões 193 a 197)

# ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca) os testes do hub com a coletânea: as opções novas do botão e o comando que elas
# montam, a recusa fora do `Cobaia.exe` e com a pilha vazia, o log escondido enquanto a rodada roda, a leitura da rodada que esconde a carta
# até a resposta, a grade que só acende as reveladas e as das rodadas anteriores, a conferência do mesmo agente da medida e, na página, os
# campos e o bloco da coletânea. Escritos antes do código: a primeira rodada falhou por ValueError em `opcoes_da_corrida` ("coletanea").
# ! Motivo: plano aprovado da coletânea, seção 4.4. A banca não pode ver o erro antes de o agente responder; se o nome de uma carta escondida
# chegar à página (no bloco, na grade ou no log da corrida), o sorteio deixa de provar alguma coisa. Nada aqui sobe o site, a API ou o modelo.
def _corrida_da_coletanea(raiz: Path, nome: str = "hub_20261204_193000", numero: str = "4821", antes: int = 0, respondidas: int = 2) -> tuple[Path, dict]:
    """Uma rodada da coletânea como o executor grava: o sorteio na pasta e no registro (com `antes` rodadas anteriores do mesmo número) e o
    `cenarios.jsonl` com as `respondidas` primeiras cartas, todas com Task Success."""
    import coletanea as cl
    reg = raiz / "hub" / cl.ARQUIVO_DOS_SORTEIOS
    for i in range(antes):
        cl.gravar_sorteio(cl.sortear(numero, 5, reg, f"hub_antes_{i}", "digitado"), raiz / f"hub_antes_{i}", reg)
    s = cl.sortear(numero, 5, reg, nome, "digitado", quando="2026-12-04T19:30:00")
    pasta = raiz / nome
    cl.gravar_sorteio(s, pasta, reg)
    linhas = []
    for id_ in s["cartas"][:respondidas]:
        c = cl.carta(id_)
        linhas.append({"cenario": id_, "tipo": c["tipo"], "roteiro": c["cenario"], "modo": c["modo"], "campo": c["campo"], "causa_esperada": c["causa"],
                       "classe": c["classe"], "repeticao": 1, "detectou": c["tipo"] != "sem_erro", "task_success": True,
                       "rotulo": c["causa"] if c["tipo"] != "sem_erro" else None, "conferencia": {"conferido": True, "campo": c["campo"]} if c["tipo"] == "contrato" else None,
                       "cura": {"curado": True} if c["tipo"] == "localizador" else None, "mttr_s": 60.0 if c["tipo"] != "sem_erro" else None})
    (pasta / "cenarios.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in linhas), encoding="utf-8")
    return pasta, s


def teste_coletanea_opcoes_do_botao_e_comando_da_corrida():
    import executar_fase4 as ex
    assert hub.opcoes_da_corrida() == {"repeticoes": 1, "selecao": "todos", "desde": None}, "sem a coletânea, as opções de sempre"
    assert hub.opcoes_da_corrida(selecao="coletanea") == {"repeticoes": 1, "selecao": "coletanea", "desde": None, "quantas": 5, "numero": None}
    o = hub.opcoes_da_corrida(selecao="coletanea", quantas=3, numero=" 4821 ")
    assert (o["quantas"], o["numero"]) == (3, "4821")
    for ruim in ({"selecao": "coletanea", "quantas": 4}, {"selecao": "coletanea", "numero": "48a1"}, {"selecao": "todos", "numero": "4821"},
                 {"selecao": "coletanea", "desde": "abc1234"}, {"selecao": "coletanea", "quantas": True}):
        try:
            hub.opcoes_da_corrida(**ruim)
        except ValueError:
            continue
        raise AssertionError(f"{ruim} deveria ser recusado")
    direto = hub.comando_direto("hub_x", o, python="py")
    assert direto == ["py", "executar_fase4.py", "--modo", "cenarios", "--saida", "hub_x", "--coletanea", "--quantas", "3", "--numero", "4821",
                      "--cobaias-no-ar", "--etapas-ao-vivo"], direto
    assert "--numero" not in hub.comando_direto("hub_x", hub.opcoes_da_corrida(selecao="coletanea"), python="py"), "sem número, vale a hora do clique"
    args = ex.montar_parser().parse_args(direto[2:])
    assert args.coletanea and args.quantas == 3 and args.numero == "4821" and args.cobaias_no_ar and args.casos == 0, "o executor entende o comando do hub"


def teste_coletanea_so_roda_pelo_exe_recusa_a_pilha_vazia_e_esconde_o_log():
    import coletanea as cl
    acervo, raiz = _acervo_de_teste()
    lancados = []

    def lancador(saida, opcoes):
        lancados.append(opcoes)
        return [sys.executable, "-c", "import time; print('localizador/front-busca/id_renomeado', flush=True); time.sleep(1.5)"]

    with _hub_no_ar(acervo, permitir_execucao=True, comando_da_corrida=lancador) as (base, _, _srv):
        status, r = _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1, "selecao": "coletanea"})
        assert status == 409 and "Cobaia.exe" in r["erro"] and lancados == [], r
    reg = raiz / "hub" / cl.ARQUIVO_DOS_SORTEIOS
    while True:
        s = cl.sortear("77", 10, reg, "hub_antes", "digitado")
        cl.gravar_sorteio(s, tp4._temp(), reg)
        if s["acabou"]:
            break
    with _hub_no_ar(acervo, pelo_exe=True, comando_da_corrida=lancador) as (base, _, _srv):
        status, r = _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1, "selecao": "coletanea", "numero": "77"})
        assert status == 409 and "acabou" in r["erro"] and lancados == [], r
        e = _json(base, "GET", "/api/execucao?selecao=coletanea&quantas=3&numero=4821")[1]
        assert "--coletanea" in e["comando_sugerido"] and "--numero 4821" in e["comando_sugerido"] and e["quantas"] == [3, 5, 10], e
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1, "selecao": "coletanea", "quantas": 3, "numero": "4821"})[0] == 200
        assert lancados and lancados[-1]["quantas"] == 3 and lancados[-1]["numero"] == "4821"
        rodando = _json(base, "GET", "/api/execucao")[1]
        assert rodando["em_andamento"] and rodando["coletanea"] is True and "front-busca" not in rodando["log"], "o log entrega a carta antes da resposta"
        fim = _ate(lambda: _json(base, "GET", "/api/execucao")[1], lambda d: d["terminou"])
        assert "localizador/front-busca/id_renomeado" in fim["log"], "terminada a rodada, o log volta a aparecer"


def teste_coletanea_da_corrida_esconde_a_carta_ate_a_resposta():
    import coletanea as cl
    raiz = tp4._temp()
    assert hd.coletanea_da_corrida(raiz, raiz / "hub" / cl.ARQUIVO_DOS_SORTEIOS) is None, "pasta sem sorteio não é rodada da coletânea"
    pasta, s = _corrida_da_coletanea(raiz, antes=1, respondidas=2)
    reg = raiz / "hub" / cl.ARQUIVO_DOS_SORTEIOS
    d = hd.coletanea_da_corrida(pasta, reg)
    assert (d["numero"], d["origem"], d["de"], d["ate"], d["total"], d["faltam"]) == ("4821", "digitado", 6, 10, 64, 54), d
    cartas = d["cartas_da_rodada"]
    assert [c["nome"] for c in cartas] == ["carta-06", "carta-07", "carta-08", "carta-09", "carta-10"]
    assert [c["revelada"] for c in cartas] == [True, True, False, False, False]
    primeira = cl.carta(s["cartas"][0])
    assert cartas[0]["id"] == primeira["id"] and cartas[0]["causa_certa"] == primeira["causa"] and cartas[0]["o_que_foi_ligado"] == cl.descricao(primeira)
    assert cartas[0]["veredito"] in ("acertou", "certo: nada foi acusado")
    tudo = json.dumps(d, ensure_ascii=False)
    for id_ in s["cartas"][2:]:
        assert id_ not in tudo and cl.descricao(cl.carta(id_)) not in tudo, "a carta escondida foi para a página"
    grade = d["grade"]
    assert sum(len(g["cartas"]) for g in grade) == 64 and [g["nome"] for g in grade][-1] == "sem erro"
    marca = {x["id"]: x["marca"] for g in grade for x in g["cartas"] if x["marca"]}
    assert all(marca.get(i) == "antes" for i in cl.ordem_da_pilha("4821")[:5]), "as cartas da rodada anterior do mesmo número ficam acesas"
    assert [marca.get(i, "") for i in s["cartas"]] == ["revelada", "revelada", "", "", ""], "a grade não pode acender a carta ainda escondida"
    assert all(x["id"] is None for g in grade for x in g["cartas"] if not x["marca"]), "quadrado apagado não leva o nome da carta"
    assert d["lista"] is None and d["comando"] is None, "a lista e o comando só aparecem no fim da rodada"
    pasta5, s5 = _corrida_da_coletanea(tp4._temp(), respondidas=5)
    d5 = hd.coletanea_da_corrida(pasta5, pasta5.parent / "hub" / cl.ARQUIVO_DOS_SORTEIOS)
    assert d5["lista"] == s5["cartas"] and d5["comando"] == s5["comando"] and all(c["revelada"] for c in d5["cartas_da_rodada"])
    sem = next(c for c in d5["cartas_da_rodada"] if c["tipo"] == "sem_erro")
    assert sem["veredito"] == "certo: nada foi acusado", sem


def teste_coletanea_confere_o_mesmo_agente_da_medida():
    import coletanea as cl
    raiz = tp4._temp()
    pasta, _ = _corrida_da_coletanea(raiz)
    reg = raiz / "hub" / cl.ARQUIVO_DOS_SORTEIOS
    assert hd.coletanea_da_corrida(pasta, reg)["mesmo_agente"] is None, "sem as condições das duas corridas, não há o que conferir"
    (raiz / hd.CORRIDA_DA_MEDIDA).mkdir()
    medida = {"hash_prompt_fixo": "p1", "biblioteca": {"hash": "b1"}}
    (raiz / hd.CORRIDA_DA_MEDIDA / "condicoes_fase4.json").write_text(json.dumps(medida), encoding="utf-8")
    (pasta / "condicoes_fase4.json").write_text(json.dumps(medida), encoding="utf-8")
    assert hd.coletanea_da_corrida(pasta, reg)["mesmo_agente"] == {"prompt_fixo": True, "biblioteca": True, "referencia": hd.CORRIDA_DA_MEDIDA}
    (pasta / "condicoes_fase4.json").write_text(json.dumps({"hash_prompt_fixo": "p2", "biblioteca": {"hash": "b1"}}), encoding="utf-8")
    assert hd.coletanea_da_corrida(pasta, reg)["mesmo_agente"]["prompt_fixo"] is False
    assert hd.CORRIDA_DA_MEDIDA == "fase5_agente_b" and (RA / "fase5_agente_b" / "condicoes_fase4.json").exists()


def teste_ao_vivo_traz_a_coletanea_da_corrida_mais_recente():
    raiz = tp4._temp()
    pasta, _ = _corrida_da_coletanea(raiz)
    (pasta / "progresso.json").write_text(json.dumps({"estado": "concluido", "etapa": "carta-07#1@tela · diagnóstico"}), encoding="utf-8")
    vivo = hd.AoVivo(raiz).ler()
    assert vivo["ha_corrida"] and vivo["coletanea"]["numero"] == "4821" and len(vivo["coletanea"]["cartas_da_rodada"]) == 5


def teste_pagina_mostra_os_campos_e_o_bloco_da_coletanea():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_que_descobre()
        pasta, s = _corrida_da_coletanea(raiz, respondidas=2)
        (pasta / "progresso.json").write_text(json.dumps({"estado": "concluido"}), encoding="utf-8")
        with _hub_no_ar(acervo, pelo_exe=True, garantir_ollama=lambda: "sem Ollama no teste",
                        comando_da_corrida=lambda saida, opcoes: [sys.executable, "-c", "print('nunca roda')"]) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#inicio .servico")
            pagina.click("#ir-para-rodar")
            pagina.wait_for_selector("#rodar-cenarios:visible")
            assert pagina.is_hidden("#campo-das-quantas") and pagina.is_hidden("#campo-do-numero")
            pagina.select_option("#selecao-da-corrida", "coletanea")
            pagina.wait_for_selector("#campo-do-numero:visible")
            assert pagina.is_visible("#campo-das-quantas") and pagina.is_hidden("#campo-das-repeticoes") and pagina.is_visible("#nota-da-coletanea")
            assert pagina.locator("#quantas-da-corrida option").count() == 3
            pagina.wait_for_selector("#coletanea .carta-da-rodada")
            bloco = pagina.inner_text("#coletanea")
            assert "4821" in bloco and pagina.locator("#coletanea .carta-da-rodada").count() == 5
            assert pagina.locator("#coletanea .carta-da-rodada.escondida").count() == 3 and pagina.locator("#coletanea .quadrado").count() == 64
            assert pagina.locator("#coletanea .quadrado.revelada").count() == 2
            assert cl_descricao(s["cartas"][0]).replace("`", "") in bloco, "o cartão revelado diz o que foi ligado: " + bloco
            html = pagina.content()
            assert all(id_ not in html for id_ in s["cartas"][2:]), "a carta escondida está no HTML"
            pagina.fill("#numero-da-corrida", "48a1")
            pagina.click("#rodar-cenarios")
            _esperar_texto(pagina, "#erro", "algarismos")
        assert [e for e in erros if "status of 400" not in e] == [], erros       # o navegador anota a recusa (400) do número com letra, que o teste provocou


def teste_resumo_do_botao_separa_as_cartas_sem_erro_da_coletanea():
    raiz = tp4._temp()
    pasta, s = _corrida_da_coletanea(raiz, respondidas=5)
    dado, md = hub.prova_do_botao(raiz)
    u = dado["corridas"][-1]
    sem = sum(1 for i in s["cartas"] if i.startswith("sem-erro/"))
    assert u["coletanea"] == {"numero": "4821", "cartas_com_erro": 5 - sem, "cartas_sem_erro": sem, "sem_erro_nada_acusado": sem}, u
    assert u["detectou"] == 5 - sem and f"detectada em {5 - sem} de {5 - sem}" in md and "número 4821" in md, md
    _, raiz_dos_dez = _acervo_de_teste()
    _corrida_do_hub(raiz_dos_dez)
    v = hub.prova_do_botao(raiz_dos_dez)[0]["corridas"][-1]
    assert "coletanea" not in v and v["detectou"] == 2, "a corrida dos dez cenários sai como antes, sem chave nova"


def cl_descricao(id_: str) -> str:
    import coletanea as cl
    return cl.descricao(cl.carta(id_))


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:  # noqa: BLE001 - o runner pega qualquer falha do teste para imprimir o rastro e parar com código 1
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        if th._PULADOS:
            print(f"aviso: {len(th._PULADOS)} teste(s) da página pulado(s), sem o Playwright neste Python")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
