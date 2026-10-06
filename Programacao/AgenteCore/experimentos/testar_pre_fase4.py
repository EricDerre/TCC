#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria testar_pre_fase4.py, o runner de testes da Pré-Fase 4 (pre_fase4.py,
# sondar_logprobs.py, viabilidade_modelos_grandes.py, ferramentas/medir_disco.py e, nas próximas sessões,
# trilha.py, sonda_confianca.py, analisar_confianca.py e gerar_atlas.py), no mesmo formato sem pytest de
# testar_fase3b.py: funções teste_<nome>(), main() roda todas em ordem de definição e termina em
# "N testes ok". A tag deste cabeçalho cobre as funções de teste e os ajudantes de teste.
# ! Motivo: a Pré-Fase 4 só acrescenta arquivos; sem um runner próprio, a leitura do disco, a captura das
# probabilidades por token do Ollama e a conta de viabilidade do colibri não teriam onde ser exercitadas
# sem Ollama e sem ler o disco inteiro. Os testes são escritos ANTES dos módulos: a primeira rodada falha
# por ModuleNotFoundError nos imports abaixo, que é o RED aceito para módulo novo.
"""Testes da Pré-Fase 4, sem pytest (asserts em Python puro)."""
import inspect
import json
import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

EXP = Path(__file__).resolve().parent
FER = EXP.parent.parent.parent / "ferramentas"
sys.path.insert(0, str(FER))

import argparse  # noqa: E402

import analisar_fase3b as a3b  # noqa: E402
import biblioteca as bib  # noqa: E402
import caminhos  # noqa: E402
import cliente_ollama as oll  # noqa: E402
import evolucao_biblioteca as evo  # noqa: E402
import executar_fase3  # noqa: E402
import executar_fase3b as e3b  # noqa: E402
import recuperacao as rec  # noqa: E402
import testar_fase3  # noqa: E402
import testar_fase3b  # noqa: E402

import analisar_confianca as conf  # noqa: E402
import avaliar  # noqa: E402
import gerar_atlas as atlas  # noqa: E402
import gerar_relatorio_raciocinio as grr  # noqa: E402
import medir_disco  # noqa: E402
import pre_fase4 as pf  # noqa: E402
import sonda_confianca  # noqa: E402
import sondar_logprobs  # noqa: E402
import trilha  # noqa: E402
import viabilidade_modelos_grandes as viab  # noqa: E402

MB = 1024 * 1024
RA = EXP / "resultados_alvo"
# Pastas que a Pré-Fase 4 só pode LER: a biblioteca original, a corrida oficial e as corridas da 3-B.
_SO_LEITURA = {"base_conhecimento": bib.BASE, "fase3": RA / "fase3", "fase3b_ponte": RA / "fase3b_ponte",
               "fase3b_ponte_0344": RA / "fase3b_ponte_0344", "fase3b_ineditos": RA / "fase3b_ineditos",
               "fase3b_cruzada_qwen": RA / "fase3b_cruzada_qwen", "fase3b_correcao": RA / "fase3b_correcao"}
_HASH_ANTES: dict[str, str | None] = {}
_TEMPORARIOS: list[Path] = []


def _temp() -> Path:
    caminho = Path(tempfile.mkdtemp(prefix="pre_fase4_teste_"))
    _TEMPORARIOS.append(caminho)
    return caminho


# ------------------------------------------------------------------ 0. área só de leitura (antes)

def teste_area_so_de_leitura_hash_antes() -> None:
    """Primeiro teste do arquivo: guarda o hash das pastas que nenhum código da Pré-Fase 4 pode escrever."""
    for nome, pasta in _SO_LEITURA.items():
        _HASH_ANTES[nome] = testar_fase3b._hash_arvore(pasta)


# ------------------------------------------------------------------ 1. medir_disco

def teste_disco_deslocamentos_alinhados_e_distintos() -> None:
    tamanho = 10 * MB + 123
    offs = medir_disco.deslocamentos(tamanho, MB, 8, semente=1)
    assert len(offs) == 8 and len(set(offs)) == 8, offs
    assert all(o % MB == 0 and o + MB <= tamanho for o in offs), offs
    assert offs == medir_disco.deslocamentos(tamanho, MB, 8, semente=1), "mesma semente, mesma lista"
    assert offs != medir_disco.deslocamentos(tamanho, MB, 8, semente=2), "outra semente, outra lista"
    # arquivo com menos blocos inteiros do que o pedido: repete blocos em vez de falhar
    poucos = medir_disco.deslocamentos(3 * MB, MB, 8, semente=1)
    assert len(poucos) == 8 and set(poucos) <= {0, MB, 2 * MB}, poucos
    # arquivo menor que um bloco: não há o que ler
    try:
        medir_disco.deslocamentos(MB - 1, MB, 4, semente=1)
    except ValueError:
        pass
    else:
        raise AssertionError("arquivo menor que um bloco deveria ser recusado")


def teste_disco_medir_le_todos_os_blocos_nos_dois_modos() -> None:
    arq = _temp() / "blob.bin"
    conteudo = os.urandom(8 * MB)
    arq.write_bytes(conteudo)
    r = medir_disco.medir(arq, MB, 8, threads=2, direto=False, semente=3)
    assert r["modo"] == "pelo_cache" and r["bytes"] == 8 * MB and r["blocos"] == 8 and r["threads"] == 2, r
    assert r["segundos"] > 0 and r["gb_por_s"] > 0, r
    offs = medir_disco.deslocamentos(arq.stat().st_size, MB, 8, semente=3)
    assert medir_disco.ler_blocos(arq, offs[:2], MB, direto=False, guardar=True) == [conteudo[o:o + MB] for o in offs[:2]]
    if medir_disco.TEM_LEITURA_DIRETA:
        d = medir_disco.medir(arq, MB, 8, threads=2, direto=True, semente=3)
        assert d["modo"] == "direto" and d["bytes"] == 8 * MB, d
        # a leitura que passa por fora do cache do sistema devolve os mesmos bytes do arquivo
        assert medir_disco.ler_blocos(arq, offs[:2], MB, direto=True, guardar=True) == [conteudo[o:o + MB] for o in offs[:2]]


def teste_disco_resumir_usa_a_mediana() -> None:
    medidas = [{"gb_por_s": 2.0, "segundos": 1.0}, {"gb_por_s": 3.0, "segundos": 0.7}, {"gb_por_s": 10.0, "segundos": 0.2}]
    r = medir_disco.resumir(medidas)
    assert r["repeticoes"] == 3 and r["gb_por_s_mediana"] == 3.0 and r["gb_por_s_min"] == 2.0 and r["gb_por_s_max"] == 10.0, r
    assert medir_disco.resumir([]) == {"repeticoes": 0, "gb_por_s_mediana": None, "gb_por_s_min": None, "gb_por_s_max": None}


# ------------------------------------------------------------------ 2. sondar_logprobs

def _post_de_mentira(vistos: list, com_logprobs: bool = True):
    """Substituto de cliente_ollama._post: anota o corpo recebido e devolve uma resposta no formato do Ollama."""
    def falso(caminho: str, corpo: dict, timeout: int = 900) -> dict:
        vistos.append((caminho, corpo))
        r = {"response": "CAUSA_RAIZ: campo_ausente\n", "prompt_eval_count": 10, "eval_count": 3, "context": [1, 2, 3],
             "load_duration": 1, "prompt_eval_duration": 2, "eval_duration": 3, "total_duration": 6}
        if com_logprobs and corpo.get("logprobs"):
            r["logprobs"] = [{"token": "CAUSA", "logprob": -0.1, "bytes": list(b"CAUSA"), "top_logprobs": []}]
        return r
    return falso


def teste_logprobs_gancho_acrescenta_campos_sem_vazar_no_retorno() -> None:
    vistos: list = []
    original = oll._post
    falso = _post_de_mentira(vistos)
    oll._post = falso
    try:
        base = oll.gerar("qwen2.5:7b", "prompt de teste", 600)          # o que o cliente manda sem o gancho
        corpo_base = vistos[-1][1]
        capturas: list = []
        with sondar_logprobs.com_logprobs(20, capturas):
            r = oll.gerar("qwen2.5:7b", "prompt de teste", 600)
            corpo_gancho = vistos[-1][1]
            oll.descarregar("qwen2.5:7b")                               # prompt vazio: tem de passar sem mudança
            corpo_descarga = vistos[-1][1]
        assert oll._post is falso, "o gancho tem de restaurar o _post que encontrou"
    finally:
        oll._post = original
    assert corpo_gancho == {**corpo_base, "logprobs": True, "top_logprobs": 20}, corpo_gancho
    assert corpo_gancho["options"] == {"num_gpu": 0, "num_ctx": 8192, "temperature": 0.1, "num_predict": 600}
    assert "logprobs" not in corpo_descarga and corpo_descarga["prompt"] == "", corpo_descarga
    assert set(r) == set(base) and len(r) == 8, f"o retorno de gerar mudou de chaves: {sorted(r)}"
    assert len(capturas) == 1, capturas
    cap = capturas[0]
    assert cap["resposta"]["logprobs"][0]["token"] == "CAUSA" and "context" not in cap["resposta"], cap
    assert "prompt" not in cap["corpo"] and cap["corpo"]["top_logprobs"] == 20 and len(cap["prompt_sha256"]) == 12, cap


def teste_logprobs_gancho_troca_temperatura_so_quando_pedido() -> None:
    vistos: list = []
    original = oll._post
    oll._post = _post_de_mentira(vistos)
    try:
        with sondar_logprobs.com_logprobs(5, [], temperatura=1.0, num_predict=8):
            oll.gerar("qwen2.5:7b", "p", 600)
    finally:
        oll._post = original
    assert vistos[-1][1]["options"] == {"num_gpu": 0, "num_ctx": 8192, "temperature": 1.0, "num_predict": 8}, vistos[-1][1]


def teste_logprobs_gancho_para_quando_o_ollama_nao_devolve_probabilidades() -> None:
    original = oll._post
    oll._post = _post_de_mentira([], com_logprobs=False)
    try:
        try:
            with sondar_logprobs.com_logprobs(20, [], exigir=True):
                oll.gerar("qwen2.5:7b", "p", 600)
        except RuntimeError as e:
            assert "logprobs" in str(e), e
        else:
            raise AssertionError("resposta sem logprobs deveria interromper quando exigir=True")
        with sondar_logprobs.com_logprobs(20, [], exigir=False):          # na sonda, a ausência é só anotada
            oll.gerar("qwen2.5:7b", "p", 600)
    finally:
        oll._post = original


def teste_logprobs_texto_dos_tokens_junta_acento_partido() -> None:
    # "não" com o "ã" (C3 A3) partido entre dois tokens: só os bytes juntos formam o caractere
    lp = [{"token": "n", "bytes": [0x6E]}, {"token": "�", "bytes": [0xC3]}, {"token": "�o", "bytes": [0xA3, 0x6F]}]
    assert sondar_logprobs.texto_dos_tokens(lp) == "não"
    assert sondar_logprobs.texto_dos_tokens([{"token": "ab"}, {"token": "c"}]) == "abc", "sem bytes, usa o texto do token"
    assert sondar_logprobs.tokens_que_partem_caractere(lp) == 2


def teste_logprobs_temperatura_antes_ou_depois() -> None:
    def pos(pares):
        return {"token": pares[0][0], "logprob": pares[0][1], "top_logprobs": [{"token": t, "logprob": l} for t, l in pares]}
    # mesma distribuição nas duas temperaturas: a probabilidade devolvida é a de antes da temperatura
    a = pos([("CA", -0.105), ("ca", -2.303), ("Ca", -6.0)])
    assert sondar_logprobs.comparar_temperatura(a, a, 0.1, 1.0)["veredito"] == "antes"
    # diferenças dez vezes maiores a 0,1 do que a 1,0: a probabilidade devolvida já passou pela temperatura
    quente = pos([("CA", -0.2), ("ca", -1.8), ("Ca", -4.2)])
    frio = pos([("CA", -1e-7), ("ca", -16.0), ("Ca", -40.0)])
    r = sondar_logprobs.comparar_temperatura(frio, quente, 0.1, 1.0)
    assert r["veredito"] == "depois" and abs(r["razao"] - 10.0) < 0.5, r
    # sem dois tokens em comum não dá para dizer
    assert sondar_logprobs.comparar_temperatura(pos([("x", -0.1)]), pos([("y", -0.1)]), 0.1, 1.0)["veredito"] == "indeterminado"


def teste_logprobs_resumo_da_resposta() -> None:
    r = {"response": " não\n", "logprobs": [
        {"token": " n", "logprob": -0.5, "bytes": [0x20, 0x6E], "top_logprobs": [{"token": " n", "logprob": -0.5}, {"token": " s", "logprob": -1.0}]},
        {"token": "ão", "logprob": -0.1, "bytes": [0xC3, 0xA3, 0x6F], "top_logprobs": [{"token": "ão", "logprob": -0.1}]},
        {"token": "\n", "logprob": -0.01, "bytes": [0x0A], "top_logprobs": []}]}
    s = sondar_logprobs.resumo_da_resposta(r)
    assert s == {"tokens_com_logprob": 3, "top_por_posicao_max": 2, "tem_bytes": True, "texto_bate": True,
                 "tokens_que_partem_caractere": 0}, s
    assert sondar_logprobs.resumo_da_resposta({"response": "x"})["tokens_com_logprob"] == 0


# ------------------------------------------------------------------ 3. pre_fase4 (derivados da fase)

def teste_pre_fase4_colar_so_os_blocos_do_proprio_prefixo() -> None:
    doc = _temp() / "relatorio.md"
    doc.write_text("texto\n\n<!-- tabela:tb_viab_x -->\n<!-- /tabela:tb_viab_x -->\n\nmeio\n\n"
                   "<!-- tabela:tb_conf_y -->\n<!-- /tabela:tb_conf_y -->\n", encoding="utf-8")
    md = a3b.tab("tb_viab_x", ["a"], [["1"]])
    assert pf.blocos_divergentes(doc, md, "tb_viab_") == ["tb_viab_x"], "bloco vazio no documento ainda não bate"
    n, mudou = pf.colar_blocos(doc, md, "tb_viab_")
    assert (n, mudou) == (1, True)
    depois = doc.read_text(encoding="utf-8")
    assert "| 1 |" in depois and "<!-- tabela:tb_conf_y -->\n<!-- /tabela:tb_conf_y -->" in depois, depois
    assert pf.blocos_divergentes(doc, md, "tb_viab_") == []
    assert pf.colar_blocos(doc, md, "tb_viab_") == (1, False), "colar de novo não muda nada"
    # bloco do mesmo prefixo no documento sem tabela gerada: interrompe, para não deixar tabela órfã
    doc.write_text(depois + "\n<!-- tabela:tb_viab_z -->\n<!-- /tabela:tb_viab_z -->\n", encoding="utf-8")
    try:
        pf.colar_blocos(doc, md, "tb_viab_")
    except SystemExit as e:
        assert "tb_viab_z" in str(e), e
    else:
        raise AssertionError("bloco sem tabela gerada deveria interromper")


def teste_pre_fase4_fechar_grava_e_confere() -> None:
    pasta = _temp()
    dado = {"metadados": {"gerado_em": "2026-10-01T10:00:00", "fonte": "x"}, "valor": 1.5}
    md = "\n".join(pf.cabecalho("Título", "script.py", "arquivo.json", "2026-10-01")) + "\n" + a3b.tab("tb_viab_x", ["a"], [["1,5"]]) + "\n"
    assert pf.fechar("teste", dado, md, "tb_viab_", pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert json.loads((pasta / "teste.json").read_text(encoding="utf-8"))["valor"] == 1.5
    assert (pasta / "teste.md").read_text(encoding="utf-8") == md
    # a data de geração não conta na conferência; o conteúdo conta
    outro_dia = {"metadados": {"gerado_em": "2026-10-02T09:00:00", "fonte": "x"}, "valor": 1.5}
    md2 = md.replace("2026-10-01", "2026-10-02")
    assert pf.fechar("teste", outro_dia, md2, "tb_viab_", check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    mudou = {"metadados": {"gerado_em": "2026-10-02T09:00:00", "fonte": "x"}, "valor": 2.0}
    assert pf.fechar("teste", mudou, md2, "tb_viab_", check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 1
    assert pf.fechar("teste", outro_dia, md2.replace("1,5", "9,9"), "tb_viab_", check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 1


# ------------------------------------------------------------------ 4. viabilidade dos modelos grandes

_MAQUINA_TESTE = {"cpu": "CPU de teste", "nucleos": 10, "threads": 12, "ram_gb": 15.69, "ram_instalada_gb": 16.0, "ram_livre_no_inicio_de_corrida_gb": 7.2,
                  "disco_modelo": "NVMe de teste", "disco_barramento": "NVMe", "disco_total_gb": 476.9, "disco_livre_gb": 218.2,
                  "sistema": "Windows de teste", "ollama": "0.34.4"}


def teste_viabilidade_cabe_no_disco_e_na_ram() -> None:
    # A máquina tem 16 GB instalados e o sistema enxerga 15,69. O "16 GB min" do repositório é da classe da máquina:
    # comparar com 15,69 dizia que ela ficava abaixo do mínimo, e ela fica exatamente nele.
    glm = {"nome": "GLM-5.2", "disco_gb": 372, "ram_min_gb": 16}
    assert viab.cabe(glm, _MAQUINA_TESTE) == {"disco_livre": False, "disco_total": True, "ram": "no_minimo", "roda": "nao"}
    assert viab.cabe({"nome": "OLMoE", "disco_gb": 7, "ram_min_gb": 8}, _MAQUINA_TESTE) == {
        "disco_livre": True, "disco_total": True, "ram": "sim", "roda": "sim"}
    # cabe no disco livre e pede exatamente a RAM instalada: roda no limite, não com folga
    assert viab.cabe({"nome": "DeepSeek V4 Flash", "disco_gb": 167, "ram_min_gb": 16}, _MAQUINA_TESTE) == {
        "disco_livre": True, "disco_total": True, "ram": "no_minimo", "roda": "no_limite"}
    kimi = viab.cabe({"nome": "Kimi K3", "disco_gb": 1600, "ram_min_gb": 32}, _MAQUINA_TESTE)
    assert kimi["disco_total"] is False and kimi["ram"] == "nao" and kimi["roda"] == "nao"
    # cabe no disco e pede mais RAM do que a instalada: não roda
    assert viab.cabe({"nome": "Qwen3.6", "disco_gb": 20, "ram_min_gb": 24}, _MAQUINA_TESTE) == {
        "disco_livre": True, "disco_total": True, "ram": "nao", "roda": "nao"}
    # sem a memória instalada gravada, a conta para em vez de comparar com o que o sistema enxerga
    sem = {k: v for k, v in _MAQUINA_TESTE.items() if k != "ram_instalada_gb"}
    try:
        viab.cabe(glm, sem)
    except SystemExit as e:
        assert "ram_instalada_gb" in str(e)
    else:
        raise AssertionError("sem a memória instalada a conta deveria parar")


def teste_disco_memoria_instalada_e_completar_maquina() -> None:
    instalada = medir_disco.memoria_instalada_gb()
    total = medir_disco._ram_total_gb()
    if instalada is not None and total is not None:
        assert instalada >= total, (instalada, total)      # o sistema nunca enxerga mais do que há instalado
    # completar_maquina acrescenta o campo que falta sem refazer a medição do disco nem tocar nos outros campos
    arq = _temp() / "disco.json"
    antes = {"gerado_em": "2026-10-01T10:00:00", "maquina": {"cpu": "x", "ram_gb": 15.69, "disco": {"livre_gb": 218.1}}, "direto": {"gb_por_s_mediana": 3.77}}
    arq.write_text(json.dumps(antes), encoding="utf-8")
    mudou = medir_disco.completar_maquina(arq, instalada_gb=16.0)
    depois = json.loads(arq.read_text(encoding="utf-8"))
    assert mudou is True and depois["maquina"]["ram_instalada_gb"] == 16.0
    assert {k: v for k, v in depois["maquina"].items() if k != "ram_instalada_gb"} == antes["maquina"] and depois["direto"] == antes["direto"]
    assert medir_disco.completar_maquina(arq, instalada_gb=16.0) is False, "com o campo já gravado, nada muda"


def teste_viabilidade_tempos() -> None:
    assert abs(viab.segundos_por_token_frio(11.4, 2.0) - 5.7) < 1e-9
    assert viab.segundos_por_token_frio(11.4, 0) is None and viab.segundos_por_token_frio(11.4, None) is None
    assert abs(viab.segundos_de_geracao(61, 0.08) - 762.5) < 1e-9
    assert viab.segundos_de_geracao(61, 0) is None


def teste_viabilidade_medianas_dos_registros() -> None:
    pasta = _temp() / "modelo_x"
    pasta.mkdir()
    linhas = [{"tokens_entrada": 2000, "tokens_saida": 50, "segundos": 40.0, "prefill_ms": 30000, "geracao_ms": 9000},
              {"tokens_entrada": 3000, "tokens_saida": 70, "segundos": 60.0, "prefill_ms": 45000, "geracao_ms": 14000},
              {"tokens_entrada": 2600, "tokens_saida": 61, "segundos": 50.0, "prefill_ms": 38000, "geracao_ms": 11000}]
    (pasta / "diagnosticos__L0.jsonl").write_text("\n".join(json.dumps(l) for l in linhas[:2]) + "\n", encoding="utf-8")
    (pasta / "diagnosticos__L1.jsonl").write_text(json.dumps(linhas[2]) + "\n", encoding="utf-8")
    (pasta / "propostas__E1.jsonl").write_text(json.dumps({"tokens_saida": 999}) + "\n", encoding="utf-8")  # não entra
    m = viab.medianas_dos_registros(pasta)
    assert m == {"n": 3, "tokens_entrada": 2600, "tokens_saida": 61, "segundos": 50.0, "prefill_ms": 38000, "geracao_ms": 11000}, m


def teste_viabilidade_montar_render_e_check() -> None:
    medianas = {"n": 360, "tokens_entrada": 2600, "tokens_saida": 61, "segundos": 50.0, "prefill_ms": 38000, "geracao_ms": 11000}
    disco = {"direto": {"repeticoes": 3, "gb_por_s_mediana": 2.0, "gb_por_s_min": 1.9, "gb_por_s_max": 2.1},
             "pelo_cache": {"repeticoes": 3, "gb_por_s_mediana": 4.0, "gb_por_s_min": 2.0, "gb_por_s_max": 6.0},
             "bloco_bytes": 19 * MB, "blocos": 64, "threads": 8, "arquivo_gb": 4.36}
    dado = viab.montar(_MAQUINA_TESTE, medianas, disco, modelo="qwen2.5:7b", gerado_em="2026-10-01T10:00:00")
    por_nome = {f["nome"]: f for f in dado["familias"]}
    assert por_nome["GLM-5.2"]["roda"] == "nao" and por_nome["OLMoE"]["roda"] == "sim", por_nome
    assert [f["nome"] for f in dado["familias"] if f["roda"] == "sim"] == ["OLMoE"], "só o OLMoE roda com folga"
    assert [f["nome"] for f in dado["familias"] if f["roda"] == "no_limite"] == ["DeepSeek V4 Flash", "Qwen3.8-Flash-Next"],         "os dois que cabem no disco livre e pedem exatamente a RAM instalada ficam no limite"
    nvme = dado["cenarios_de_disco"][0]
    assert nvme["premissa"] is False and abs(nvme["segundos_por_token_frio"] - 5.7) < 1e-9, nvme
    assert all(c["premissa"] for c in dado["cenarios_de_disco"][1:]), "os discos que não medimos entram como premissa declarada"
    assert abs(nvme["minutos_de_leitura_por_resposta"] - 5.7 * 61 / 60) < 1e-9
    i5 = next(m for m in dado["medidas_de_terceiros"] if "12600K" in m["maquina"])
    assert abs(i5["minutos_por_resposta"] - 61 / 0.08 / 60) < 1e-9, i5
    assert all(m["fonte"].startswith("https://") for m in dado["medidas_de_terceiros"] + dado["familias"])
    md = viab.render(dado)
    for bloco in ("tb_viab_maquina", "tb_viab_familias", "tb_viab_disco", "tb_viab_terceiros"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "| RAM instalada | 16,0 GB |" in md and "15,69 GB" in md, "a tabela diz a memória instalada e a que o sistema enxerga"
    assert md.count("| no limite |") == 2 and "no mínimo declarado" in md
    assert "—" not in md and "→" not in md, "texto derivado sem travessão e sem seta"
    pasta = _temp()
    assert pf.fechar(viab.NOME, dado, md, viab.PREFIXO, pasta=pasta, doc=pasta / "nao_existe.md") == 0
    assert pf.fechar(viab.NOME, dado, md, viab.PREFIXO, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0


# ------------------------------------------------------------------ 5. sonda de confiança

_MODELO_SONDA = "modelo:teste"
# As 37 chaves do registro de diagnóstico oficial (executar_fase3.diagnosticar): a sonda não pode acrescentar nenhuma.
_CHAVES_DO_REGISTRO_OFICIAL = {
    "biblioteca_epoca", "biblioteca_versao", "carga_ms", "caso", "causa_plantada", "chars_contexto", "classe", "condicao",
    "contexto_estourou", "contexto_sha256", "digest", "epoca", "estrategia", "fase", "gabarito", "geracao_ms", "k", "maquina",
    "memoria_mb", "modelo", "modelos_residentes", "nivel", "notas_no_contexto", "particao", "prefill_ms", "resposta", "segundos",
    "somente_cpu", "teto_tokens", "tipo", "tokens_entrada", "tokens_saida", "total_ms", "verbete_ouro", "verbetes_ids",
    "verbetes_novos_no_contexto", "versao_ollama"}


def _post_da_sonda(casos: list[dict], vistos: list, devolver_logprobs: bool = True):
    """_post de mentira no formato cru do Ollama: responde o gabarito do caso (achado pelo sintoma no prompt) e devolve
    um `logprobs` cujos bytes remontam a resposta, em pedaços de 3 bytes para partir os acentos de propósito."""
    verbetes = bib.carregar()
    por_sintoma = {c["entrada"]["sintoma"]: c for c in casos}

    def falso(caminho: str, corpo: dict, timeout: int = 900) -> dict:
        vistos.append(corpo)
        caso = next(c for s, c in por_sintoma.items() if s in corpo["prompt"])
        ouro = rec.verbete_ouro(verbetes, caso)["id"]
        texto = (f"CAUSA_RAIZ: {caso['gabarito']['causa_raiz']}\nCAMPO: nenhum\n"
                 f"IMPACTO: a tela não mostra o dado esperado.\nFONTE: [{ouro}]\n")
        r = {"response": texto, "prompt_eval_count": 1500, "eval_count": 60, "load_duration": 0, "prompt_eval_duration": 3e8,
             "eval_duration": 2e8, "total_duration": 5e8, "done_reason": "stop", "prompt_eval_cached_count": 7, "context": [1, 2]}
        if devolver_logprobs and corpo.get("logprobs"):
            dados = texto.encode("utf-8")
            r["logprobs"] = []
            for i in range(0, len(dados), 3):
                p = dados[i:i + 3]
                t = p.decode("utf-8", errors="replace")
                r["logprobs"].append({"token": t, "logprob": -0.25, "bytes": list(p),
                                      "top_logprobs": [{"token": t, "logprob": -0.25, "bytes": list(p)},
                                                       {"token": "x", "logprob": -2.123456, "bytes": [120]}]})
        return r
    return falso


def _stubs_da_sonda(casos: list[dict], vistos: list, devolver_logprobs: bool = True) -> dict:
    return {"_post": _post_da_sonda(casos, vistos, devolver_logprobs), "instalados": lambda: {_MODELO_SONDA: "deadbeef0000"},
            "residentes": lambda: [{"nome": _MODELO_SONDA, "memoria_mb": 5200, "vram_mb": 0}], "descarregar": lambda m: None,
            "um_modelo_por_vez": lambda: (True, []), "_get": lambda caminho, timeout=30: {"version": "0.34.4-teste"}}


def _oficial_de_mentira(versoes: list[int]) -> dict:
    """Árvore oficial mínima sob caminhos.RESULTADOS (já apontado para uma pasta temporária): particao.json e as
    bibliotecas fechadas do modelo de teste."""
    c3_of = caminhos.fase3("fase3")
    particao = evo.particionar(e3b.TODOS_OS_CASOS)
    c3_of["raiz"].mkdir(parents=True, exist_ok=True)
    evo.gravar_ou_conferir_particao(c3_of["particao"], particao)
    slug = executar_fase3._slug(_MODELO_SONDA)
    for v in versoes:
        testar_fase3b._fechar_biblioteca_de_mentira(c3_of["bibliotecas"] / slug, v, _MODELO_SONDA)
    return particao


def teste_sonda_compacta_e_expande_logprobs() -> None:
    cru = [{"token": "CA", "logprob": -0.0189123456, "bytes": [67, 65],
            "top_logprobs": [{"token": "CA", "logprob": -0.0189123456, "bytes": [67, 65]}, {"token": "**", "logprob": -4.39412345, "bytes": [42, 42]}]},
           {"token": "�", "logprob": -0.5, "bytes": [0xC3], "top_logprobs": []}]
    c = sonda_confianca.compactar(cru)
    assert c == [{"t": "CA", "l": -0.01891, "b": [67, 65], "a": [["CA", -0.01891], ["**", -4.39412]]},
                 {"t": "�", "l": -0.5, "b": [0xC3], "a": []}], c
    e = sonda_confianca.expandir(c)
    assert e[0]["token"] == "CA" and e[0]["bytes"] == [67, 65] and e[0]["top_logprobs"][1] == {"token": "**", "logprob": -4.39412}
    assert sondar_logprobs.texto_dos_tokens(e) == sondar_logprobs.texto_dos_tokens(cru), "os bytes do token gerado não se perdem"


def teste_sonda_casos_sao_os_36_oficiais_e_os_36_ineditos() -> None:
    particao = evo.particionar(e3b.TODOS_OS_CASOS)
    casos = sonda_confianca.casos_da_sonda(particao)
    ids = [c["id"] for c in casos]
    assert len(ids) == 72 and len(set(ids)) == 72, len(ids)
    oficiais = [c["id"] for c in e3b._casos_avaliacao(particao)]
    assert ids[:36] == oficiais, "os 36 oficiais de avaliação vêm primeiro, na ordem do banco"
    p = sonda_confianca.particao_da_sonda(casos)
    assert p["n_avaliacao"] == 72 and all(v["particao"] == "avaliacao" for v in p["casos"].values())
    assert sonda_confianca.particao_da_sonda(casos) == p, "partição determinística, para o relance conferir em vez de recusar"


def teste_sonda_grava_lateral_e_mantem_o_registro_oficial() -> None:
    def corpo(tmp: Path) -> None:
        particao = _oficial_de_mentira([1])
        casos = sonda_confianca.casos_da_sonda(particao)
        vistos: list = []
        stubs = _stubs_da_sonda(casos, vistos)
        args = argparse.Namespace(saida="pre_fase4_confianca_teste", modelo=_MODELO_SONDA, versoes=[1], top=20, casos=4, k=3,
                                  max_tokens_diagnostico=600, max_tokens_proposta=700)
        diag_antes = executar_fase3.diagnosticar
        falhas = testar_fase3._com_stubs(stubs, lambda: sonda_confianca.rodar(args))
        assert falhas == [], falhas
        assert executar_fase3.diagnosticar is diag_antes, "a troca de diagnosticar tem de ser desfeita"
        slug = executar_fase3._slug(_MODELO_SONDA)
        c3b = caminhos.fase3("pre_fase4_confianca_teste")
        pasta = c3b["raiz"] / slug
        regs = [json.loads(l) for l in (pasta / "diagnosticos__L1.jsonl").read_text(encoding="utf-8").splitlines()]
        lat = [json.loads(l) for l in (pasta / "logprobs__L1.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(regs) == 4 and [l["caso"] for l in lat] == [r["caso"] for r in regs], (len(regs), len(lat))
        assert all(set(r) == _CHAVES_DO_REGISTRO_OFICIAL for r in regs), sorted(set(regs[0]) ^ _CHAVES_DO_REGISTRO_OFICIAL)
        assert all(c.get("logprobs") is True and c.get("top_logprobs") == 20 for c in vistos), "toda inferência pediu as probabilidades"
        assert all(c["options"] == {"num_gpu": 0, "num_ctx": 8192, "temperature": 0.1, "num_predict": 600} for c in vistos)
        l0, r0 = lat[0], regs[0]
        assert sondar_logprobs.texto_dos_tokens(sonda_confianca.expandir(l0["logprobs"])).strip() == r0["resposta"]
        assert l0["biblioteca_versao"] == r0["biblioteca_versao"] and l0["biblioteca_epoca"] == 1 and l0["modelo"] == _MODELO_SONDA
        assert l0["top_logprobs"] == 20 and len(l0["prompt_sha256"]) == 12 and l0["prompt_eval_cached_count"] == 7 and l0["done_reason"] == "stop"
        cond = json.loads((c3b["raiz"] / "condicoes_3b.json").read_text(encoding="utf-8"))
        assert cond["modo"] == "confianca" and cond["top_logprobs"] == 20 and cond["versoes"] == [1], cond
        assert cond["conjuntos"] == {"oficiais_de_avaliacao": 36, "ineditos": 36}, cond
        # relance: nada é refeito e nenhuma linha lateral é duplicada
        n = len(vistos)
        assert testar_fase3._com_stubs(stubs, lambda: sonda_confianca.rodar(args)) == []
        assert len(vistos) == n
        assert len((pasta / "logprobs__L1.jsonl").read_text(encoding="utf-8").splitlines()) == 4
        cond2 = json.loads((c3b["raiz"] / "condicoes_3b.json").read_text(encoding="utf-8"))
        assert cond2["top_logprobs"] == 20 and cond2["criado_em"] == cond["criado_em"]

    testar_fase3b._com_resultados_temporarios(corpo)


def teste_sonda_para_se_o_ollama_nao_devolve_probabilidades() -> None:
    def corpo(tmp: Path) -> None:
        particao = _oficial_de_mentira([1])
        casos = sonda_confianca.casos_da_sonda(particao)
        stubs = _stubs_da_sonda(casos, [], devolver_logprobs=False)
        args = argparse.Namespace(saida="pre_fase4_confianca_teste2", modelo=_MODELO_SONDA, versoes=[1], top=20, casos=2, k=3,
                                  max_tokens_diagnostico=600, max_tokens_proposta=700)
        falhas = testar_fase3._com_stubs(stubs, lambda: sonda_confianca.rodar(args))
        assert falhas == [_MODELO_SONDA], falhas
        pasta = caminhos.fase3("pre_fase4_confianca_teste2")["raiz"] / executar_fase3._slug(_MODELO_SONDA)
        assert not (pasta / "diagnosticos__L1.jsonl").exists() or not (pasta / "diagnosticos__L1.jsonl").read_text(encoding="utf-8").strip(), \
            "sem probabilidades, nenhum registro pode ser gravado"

    testar_fase3b._com_resultados_temporarios(corpo)


# ------------------------------------------------------------------ 6. trilha: o arquivo bruto e o adaptador

_RESPOSTAS_DE_TESTE = [
    "CAUSA_RAIZ: campo_ausente\nCAMPO: imagem\nIMPACTO: o cartão aparece sem foto.\nFONTE: [contrato-produto], [campo_ausente]",
    "O corpo veio cortado no meio do preço.\n\n**CAUSA_RAIZ:** `resposta_truncada`\n**CAMPO:** preco\n**IMPACTO:** a listagem fica vazia.\n**FONTE:** [resposta_truncada]",
    "Causa_Raiz: Coleção_no_lugar_de_objeto extra\ncampo: nenhum\nimpacto: nada muda\nfonte: nenhum",
    "sem as linhas pedidas",
]


def teste_trilha_declaracoes_sao_trechos_literais_e_batem_com_o_avaliador() -> None:
    for r in _RESPOSTAS_DE_TESTE:
        d = trilha.localizar_declaracoes(r)
        assert d["lido"] == avaliar.extrair(r), (r, d["lido"])
        for nome, item in d["campos"].items():
            if item is not None:
                assert r[item["ini"]:item["fim"]] == item["valor"], (nome, item)
        for f in d["fontes"]:
            assert r[f["ini"]:f["fim"]] == f["valor"] and f["valor"] in d["lido"]["fonte_ids"], f
        assert r[d["raciocinio"]["ini"]:d["raciocinio"]["fim"]].strip() == d["raciocinio"]["valor"]
    d0, d1, d2, d3 = [trilha.localizar_declaracoes(r) for r in _RESPOSTAS_DE_TESTE]
    assert d0["raciocinio"]["valor"] == "" and d0["campos"]["causa_raiz"]["valor"] == "campo_ausente"
    assert [f["valor"] for f in d0["fontes"]] == ["contrato-produto", "campo_ausente"]
    assert d1["raciocinio"]["valor"] == "O corpo veio cortado no meio do preço."
    assert d1["campos"]["causa_raiz"]["valor"] == "resposta_truncada" and d1["campos"]["campo"]["valor"] == "preco"
    assert d2["campos"]["causa_raiz"]["valor"] == "Coleção_no_lugar_de_objeto", "o valor é o texto como o modelo escreveu; o lido é que vai em minúsculas"
    assert d2["fontes"] == [] and d2["campos"]["fonte"]["valor"] == "nenhum"
    assert all(v is None for v in d3["campos"].values()) and d3["raciocinio"]["valor"] == "sem as linhas pedidas"


def teste_trilha_prompt_e_a_concatenacao_das_partes() -> None:
    verbetes = bib.carregar()
    indice = rec.Indice(verbetes)
    for caso in e3b.TODOS_OS_CASOS:
        ctx, prompt = executar_fase3.contexto_e_prompt(verbetes, indice, caso, 3)
        partes = trilha.partes_do_prompt(verbetes, ctx, caso, prompt)
        assert "".join(p["antes"] + p["texto"] for p in partes) == prompt, caso["id"]
        assert [p["papel"] for p in partes] == ["cabecalho_da_documentacao", "verbete", "verbete", "verbete", "instrucao", "caso", "formato"], caso["id"]
        assert [p["id"] for p in partes if p["papel"] == "verbete"] == ctx["verbetes_ids"], caso["id"]
    # a instrução e o formato são os mesmos em todos os casos: é o que permite guardá-los uma vez só
    def partes(caso: dict) -> list[dict]:
        ctx, prompt = executar_fase3.contexto_e_prompt(verbetes, indice, caso, 3)
        return trilha.partes_do_prompt(verbetes, ctx, caso, prompt)

    p1, p2 = partes(e3b.TODOS_OS_CASOS[0]), partes(e3b.TODOS_OS_CASOS[-1])
    assert p1[4]["texto"] == p2[4]["texto"] and p1[6]["texto"] == p2[6]["texto"]


def teste_trilha_candidatos_somam_e_batem_com_a_recuperacao() -> None:
    verbetes = bib.carregar()
    indice = rec.Indice(verbetes)
    for caso in e3b.TODOS_OS_CASOS[::7]:
        sinais, itens = trilha.candidatos(indice, caso, 3)
        assert len(itens) == len(verbetes) and [i["posicao"] for i in itens] == list(range(1, len(verbetes) + 1))
        assert [i["id"] for i in itens[:3]] == [v["id"] for v in rec.recuperar(indice, caso, 3)], caso["id"]
        assert [i["escolhido"] for i in itens] == [True] * 3 + [False] * (len(verbetes) - 3)
        for i in itens:
            soma = i["bm25"] + i["reforco_endpoint"] + i["reforco_entidade"] + i["reforco_status"]
            assert abs(soma - i["pontuacao"]) < 1e-6, (caso["id"], i)
        assert set(sinais) == {"endpoint", "entidade", "status", "termos"}


def teste_trilha_escritor_numera_dedupa_e_valida() -> None:
    t = trilha.Trilha()
    h1 = t.blob("texto do verbete", "verbete")
    h2 = t.blob("texto do verbete", "verbete")
    assert h1 == h2 and len(h1) == 16 and len(t.eventos) == 1, "o mesmo texto é gravado uma vez só"
    s1 = t.evento("entrada", "x@L1", {"caso": "x"}, "recalculado")
    s2 = t.evento("declaracao", "x@L1", {"campo": "causa_raiz"}, "registro", pai=s1)
    s3 = t.evento("entrada", "y@L1", {"caso": "y"}, "recalculado")
    e = {ev["seq"]: ev for ev in t.eventos}
    assert (s1, s2, s3) == (2, 3, 4) and e[1]["tipo"] == "blob"
    assert e[s2]["camada"] == "modelo" and e[s1]["camada"] == "programa" and e[s2]["pai"] == s1
    assert (e[s1]["passo"], e[s2]["passo"], e[s3]["passo"]) == (1, 2, 1), "o passo conta dentro de cada trilha"
    assert all(ev["v"] == trilha.V and ev["ts"] is None for ev in t.eventos)
    linhas = t.linhas()
    assert [json.loads(l)["seq"] for l in linhas] == [1, 2, 3, 4]
    assert linhas[1] == json.dumps(json.loads(linhas[1]), ensure_ascii=False, sort_keys=True), "chaves ordenadas: a mesma trilha sai igual byte a byte"
    for ruim in (lambda: t.evento("tipo_que_nao_existe", "x", {}, "registro"), lambda: t.evento("entrada", "x", {}, "origem_que_nao_existe")):
        try:
            ruim()
        except ValueError:
            pass
        else:
            raise AssertionError("tipo ou origem fora do vocabulário deveria ser recusado")


def _corrida_de_mentira(nome: str, n_casos: int = 3) -> tuple[dict, dict]:
    """Roda a sonda de confiança com o Ollama de mentira sob caminhos.RESULTADOS (já temporário) e devolve os caminhos
    da saída e a partição oficial: registros no formato oficial e o arquivo lateral de probabilidades, sem inferência."""
    particao = _oficial_de_mentira([1])
    casos = sonda_confianca.casos_da_sonda(particao)
    args = argparse.Namespace(saida=nome, modelo=_MODELO_SONDA, versoes=[1], top=20, casos=n_casos, k=3,
                              max_tokens_diagnostico=600, max_tokens_proposta=700)
    assert testar_fase3._com_stubs(_stubs_da_sonda(casos, []), lambda: sonda_confianca.rodar(args)) == []
    return caminhos.fase3(nome), particao


def teste_trilha_adapta_corrida_gravada() -> None:
    def corpo(tmp: Path) -> None:
        c3b, _ = _corrida_de_mentira("trilha_teste")
        t = trilha.adaptar_corrida("trilha_teste", _MODELO_SONDA, 1)
        ev = t.eventos
        por_trilha = trilha.por_trilha(ev)
        slug = executar_fase3._slug(_MODELO_SONDA)
        regs = [json.loads(l) for l in (c3b["raiz"] / slug / "diagnosticos__L1.jsonl").read_text(encoding="utf-8").splitlines()]
        ids = [f"trilha_teste/{slug}/{r['caso']}@L1" for r in regs]
        assert [k for k in por_trilha if "@" in k] == ids, list(por_trilha)
        assert sum(e["tipo"] == "corrida" for e in ev) == 1
        blobs = {e["dados"]["sha"]: e["dados"]["texto"] for e in ev if e["tipo"] == "blob"}
        for r, tid in zip(regs, ids):
            seq = por_trilha[tid]
            tipos = [e["tipo"] for e in seq]
            assert tipos[:4] == ["entrada", "candidatos", "prompt", "inferencia"], tipos
            assert set(tipos[4:]) == {"declaracao", "verificacao"}, tipos
            p = next(e for e in seq if e["tipo"] == "prompt")["dados"]
            # a sonda guardou o hash do prompt que foi ao Ollama: o prompt remontado é provado inteiro por ele
            assert p["provas"] == {"biblioteca": True, "contexto": True, "prompt_de_proposta": None, "hash_do_prompt_enviado": True}, p
            assert p["nivel"] == "prompt_inteiro", p
            prompt = "".join(x["antes"] + blobs[x["sha"]] for x in p["partes"])
            assert trilha.sha(prompt) == p["sha"] and len(prompt) == p["chars"], "o prompt se remonta dos blobs"
            inf = next(e for e in seq if e["tipo"] == "inferencia")["dados"]
            assert blobs[inf["resposta"]] == r["resposta"] and inf["tokens_entrada"] == r["tokens_entrada"]
            assert inf["logprobs"] == {"arquivo": "logprobs__L1.jsonl", "caso": r["caso"]}, inf["logprobs"]
            decl = {e["dados"]["campo"]: e["dados"] for e in seq if e["tipo"] == "declaracao" and e["dados"]["campo"] != "fonte_citada"}
            assert decl["causa_raiz"]["lido"] == r["gabarito"]["causa_raiz"] and decl["raciocinio"]["vazio"] is True
            assert all(e["camada"] == "modelo" and e["origem"] == "registro" for e in seq if e["tipo"] == "declaracao")
            ver = {e["dados"]["regra"]: e["dados"] for e in seq if e["tipo"] == "verificacao"}
            assert ver["quatro_linhas_presentes"]["resultado"] == "confere"
            assert ver["rotulo_no_conjunto"]["resultado"] == "confere"
            assert ver["fonte_estava_no_contexto"]["resultado"] in ("confere", "nao_confere")
            assert ver["impacto"]["resultado"] == "nao_verificavel"
            assert ver["causa_correta"]["usa_gabarito"] is True and ver["causa_correta"]["resultado"] == "confere"
            assert [k for k, v in ver.items() if v["usa_gabarito"]] == ["causa_correta", "campo_correto", "verbete_de_ouro_no_contexto"], \
                "as conferências que usam o gabarito vêm por último e são só estas"
        # a instrução e o formato do prompt aparecem uma vez só no arquivo, e os verbetes repetidos também
        papeis = [e["dados"]["papel"] for e in ev if e["tipo"] == "blob"]
        assert papeis.count("instrucao") == 1 and papeis.count("formato") == 1 and papeis.count("cabecalho_da_documentacao") == 1
        # remontar de novo dá o mesmo arquivo, byte a byte
        assert trilha.adaptar_corrida("trilha_teste", _MODELO_SONDA, 1).linhas() == t.linhas()

    testar_fase3b._com_resultados_temporarios(corpo)


def teste_trilha_verificacoes_acusam_o_que_nao_confere() -> None:
    verbetes = bib.carregar()
    caso = e3b.TODOS_OS_CASOS[0]
    ids_contexto = [v["id"] for v in verbetes[:3]]
    fora = next(v["id"] for v in verbetes if v["id"] not in ids_contexto)
    resposta = f"CAUSA_RAIZ: causa_que_nao_existe\nCAMPO: campo_inventado_xyz\nIMPACTO: nada.\nFONTE: [{fora}], [verbete-que-nao-existe]"
    registro = {"caso": caso["id"], "resposta": resposta, "verbetes_ids": ids_contexto, "verbete_ouro": ids_contexto[0],
                "gabarito": caso["gabarito"], "modelo": "m", "classe": caso["classe"], "nivel": caso["nivel"], "estrategia": "linear",
                "segundos": 1.0, "tokens_saida": 10, "somente_cpu": True, "condicao": "A2"}
    ver = {v["regra"] + ":" + str(v["alvo"]): v for v in trilha.verificar(registro, caso, verbetes, trilha.localizar_declaracoes(resposta))}
    assert ver["rotulo_no_conjunto:causa_que_nao_existe"]["resultado"] == "nao_confere"
    assert ver[f"fonte_existe_na_biblioteca:{fora}"]["resultado"] == "confere"
    assert ver["fonte_existe_na_biblioteca:verbete-que-nao-existe"]["resultado"] == "nao_confere"
    assert ver[f"fonte_estava_no_contexto:{fora}"]["resultado"] == "nao_confere"
    assert ver["campo_existe_no_caso:campo_inventado_xyz"]["resultado"] == "nao_confere"
    assert ver["rotulo_sustentado_por_verbete_do_contexto:causa_que_nao_existe"]["resultado"] == "nao_confere"
    assert ver["causa_correta:causa_que_nao_existe"]["resultado"] == "nao_confere"
    # sem nenhuma fonte citada, as conferências de fonte dizem que não se aplicam em vez de sumir
    sem = "CAUSA_RAIZ: campo_ausente\nCAMPO: nenhum\nIMPACTO: nada.\nFONTE: nenhum"
    ver2 = {v["regra"]: v for v in trilha.verificar({**registro, "resposta": sem}, caso, verbetes, trilha.localizar_declaracoes(sem))}
    assert ver2["fonte_estava_no_contexto"]["resultado"] == "nao_se_aplica" and ver2["campo_existe_no_caso"]["resultado"] == "nao_se_aplica"


def teste_trilha_registros_oficiais_se_remontam_com_a_errata() -> None:
    """Com os dados reais: toda trilha do qwen2.5:7b na L1 oficial prova a biblioteca e o contexto, e nos casos de
    aprendizado o prompt inteiro bate, byte a byte, com o começo do prompt de proposta que a bateria gravou. Depende
    da errata dos dois casos de texto corrigido em 28/09; sem os registros ou sem a errata o teste não roda."""
    oficial = RA / "fase3" / "qwen2.5_7b" / "diagnosticos__L1.jsonl"
    errata = RA / "pre_fase4" / "errata_casos.json"
    if not oficial.exists() or not errata.exists():
        print("  (pulado: sem resultados_alvo/fase3 ou sem a errata dos casos)")
        return
    anterior = caminhos.RESULTADOS
    caminhos.RESULTADOS = RA
    try:
        t = trilha.adaptar_corrida("fase3", "qwen2.5:7b", 1)
        prompts = [e["dados"] for e in t.eventos if e["tipo"] == "prompt" and e["dados"].get("etapa") == "diagnostico"]
        assert len(prompts) == 90, len(prompts)
        assert all(p["provas"]["biblioteca"] and p["provas"]["contexto"] for p in prompts), \
            [p for p in prompts if not (p["provas"]["biblioteca"] and p["provas"]["contexto"])][:2]
        inteiros = [p for p in prompts if p["provas"]["prompt_de_proposta"] is not None]
        assert len(inteiros) == 54 and all(p["provas"]["prompt_de_proposta"] for p in inteiros), \
            [p["sha"] for p in inteiros if not p["provas"]["prompt_de_proposta"]]
        assert [p["nivel"] for p in prompts].count("prompt_inteiro") == 54 and "nao_comprovado" not in [p["nivel"] for p in prompts]
        # sem a errata, os casos de texto corrigido deixam de bater: é a errata que os prova
        sem = trilha.adaptar_corrida("fase3", "qwen2.5:7b", 1, errata={})
        falhos = [e["trilha"] for e in sem.eventos if e["tipo"] == "prompt" and e["dados"].get("etapa") == "diagnostico"
                  and e["dados"]["nivel"] == "nao_comprovado"]
        assert falhos and all(any(c in f for c in ("efe-3@", "efe-10@")) for f in falhos), falhos
    finally:
        caminhos.RESULTADOS = anterior


# ------------------------------------------------------------------ 7. relatório de raciocínio (gerado só da trilha)

_SECOES_DO_RELATORIO = ["## O que o programa fez", "## O que o modelo declarou", "## O que o código conferiu",
                        "## Avaliação contra o gabarito", "## Rastro"]


def _trilha_com_um_erro(nome: str) -> tuple["trilha.Trilha", str, str, str]:
    """Corrida de mentira em que o primeiro registro é regravado com uma causa errada e uma fonte fora do contexto, para
    o relatório ter o que acusar. Devolve a trilha, o id da trilha do caso alterado, a causa do gabarito e a respondida."""
    c3b, _ = _corrida_de_mentira(nome)
    slug = executar_fase3._slug(_MODELO_SONDA)
    arq = c3b["raiz"] / slug / "diagnosticos__L1.jsonl"
    regs = [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines()]
    certa = regs[0]["gabarito"]["causa_raiz"]
    errada = next(c for c in sorted(avaliar._PERMITIDAS) if c != certa)
    regs[0]["resposta"] = f"CAUSA_RAIZ: {errada}\nCAMPO: nenhum\nIMPACTO: a tela não mostra o dado esperado.\nFONTE: [verbete-que-nao-existe]"
    arq.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in regs) + "\n", encoding="utf-8")
    t = trilha.adaptar_corrida(nome, _MODELO_SONDA, 1)
    return t, f"{nome}/{slug}/{regs[0]['caso']}@L1", certa, errada


def teste_relatorio_secoes_na_ordem_e_gabarito_num_lugar_so() -> None:
    def corpo(tmp: Path) -> None:
        t, tid, certa, errada = _trilha_com_um_erro("relatorio_teste")
        md = grr.relatorio_do_caso(t.eventos, tid)
        posicoes = [md.index(s) for s in _SECOES_DO_RELATORIO]
        assert posicoes == sorted(posicoes), "as seções vêm sempre na mesma ordem"
        ini = md.index("## Avaliação contra o gabarito")
        fim = md.index("## Rastro")
        fora = md[:ini] + md[fim:]
        assert "gabarito" not in fora.lower(), "o gabarito só aparece na seção de avaliação"
        assert f"`{certa}`" in md[ini:fim] and f"`{errada}`" in md[:ini]
        # as três camadas aparecem no resumo do topo, cada uma numa linha
        topo = md[:md.index("## O que o programa fez")]
        for camada in ("O que o programa fez", "O que o modelo declarou", "O que o código conferiu"):
            assert f"| {camada} |" in topo, camada
        assert "não escreveu raciocínio" in md, "a ausência de raciocínio é dita, não omitida"
        assert "**não confere**" in md[md.index("## O que o código conferiu"):ini], "a fonte inexistente é acusada sem precisar do gabarito"
        assert "não dá para conferir por código" in md, "a frase de impacto é declarada como não verificável"
        # o texto do relatório não usa travessão nem seta; o material citado (caso, verbetes, prompt, resposta) fica como veio
        import re as _re
        prosa = _re.sub(r"(?s)`{3,4}text\n.*?\n`{3,4}", "", md)
        assert tid in md and "—" not in prosa and "→" not in prosa
        assert grr.relatorio_do_caso(t.eventos, tid) == md, "gerar de novo dá o mesmo texto"
        # o hash do rastro é o dos eventos da trilha do caso: muda se um evento mudar
        outro = [dict(e) for e in t.eventos]
        alvo = next(e for e in outro if e["trilha"] == tid and e["tipo"] == "inferencia")
        alvo["dados"] = {**alvo["dados"], "tokens_saida": 999}
        assert grr.hash_da_trilha(outro, tid) != grr.hash_da_trilha(t.eventos, tid)

    testar_fase3b._com_resultados_temporarios(corpo)


def teste_relatorio_indicadores_contam_as_conferencias() -> None:
    def corpo(tmp: Path) -> None:
        t, tid, _, _ = _trilha_com_um_erro("indicadores_teste")
        ind = grr.indicadores(t.eventos)
        assert ind["diagnosticos"] == 3 and ind["sem_raciocinio_antes_das_linhas"] == 3, ind
        regras = {r["regra"]: r for r in ind["conferencias"]}
        assert regras["fonte_existe_na_biblioteca"]["nao_confere"] == 1 and regras["rotulo_no_conjunto"]["confere"] == 3, regras
        assert regras["quatro_linhas_presentes"]["confere"] == 3
        assert "causa_correta" not in regras, "as conferências que usam o gabarito ficam no bloco de avaliação"
        assert ind["avaliacao"]["causa_correta"] == {"confere": 2, "nao_confere": 1}
        assert ind["prova_do_prompt"] == {"prompt_inteiro": 3}
        sus = ind["acerto_por_sustentacao"]
        assert sus["sustentado"]["n"] + sus["nao_sustentado"]["n"] == 3
        dado = grr.montar([("indicadores_teste", _MODELO_SONDA, 1, t.eventos)], gerado_em="2026-10-01T10:00:00")
        md = grr.render(dado)
        for bloco in ("tb_rac_corridas", "tb_rac_conferencias", "tb_rac_avaliacao"):
            assert f"<!-- tabela:{bloco} -->" in md, bloco
        assert "—" not in md and "→" not in md
        pasta = _temp()
        assert pf.fechar(grr.NOME, dado, md, grr.PREFIXO, pasta=pasta, doc=pasta / "nao_existe.md") == 0
        assert pf.fechar(grr.NOME, dado, md, grr.PREFIXO, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0

    testar_fase3b._com_resultados_temporarios(corpo)


# ------------------------------------------------------------------ 8. atlas (método do expert_atlas do colibri nos nossos dados)

def teste_atlas_afinidade_corrige_pela_taxa_de_base() -> None:
    # 5 casos de 10 numa classe e 1 de 2 na outra: a taxa é a mesma (0,5), então não há especialização nenhuma;
    # a contagem crua (5 contra 1) diria o contrário
    a = atlas.afinidade({1: 5, 2: 1}, {1: 10, 2: 2})
    assert a["n"] == [5, 1] and a["f"] == [0.5, 0.5] and a["p"] == [0.5, 0.5], a
    assert a["entropia_bits"] == 1.0 and a["especializacao"] == 0.0 and a["dominante"] is None and a["itens"] == 6, a
    # tudo numa classe só: entropia zero, especialização 1
    b = atlas.afinidade({1: 3}, {1: 10, 2: 2})
    assert b["p"] == [1.0, 0.0] and b["entropia_bits"] == 0.0 and b["especializacao"] == 1.0 and b["dominante"] == 1, b
    # nas seis classes por igual: entropia máxima, log2(6) bits
    c = atlas.afinidade({k: 2 for k in range(1, 7)}, {k: 15 for k in range(1, 7)})
    assert abs(c["entropia_bits"] - 2.585) < 1e-3 and c["especializacao"] == 0.0, c
    # nunca recuperado: sem afinidade para medir
    d = atlas.afinidade({}, {1: 10, 2: 2})
    assert d["itens"] == 0 and d["p"] is None and d["especializacao"] is None and d["dominante"] is None, d


def teste_atlas_rotulo_exige_repeticao() -> None:
    assert atlas.rotular(0, None) == "nunca_recuperado"
    assert atlas.rotular(1, 1.0) == "sem_repeticao", "um caso só não faz especialista"
    assert atlas.rotular(2, 0.5) == "especialista" and atlas.rotular(2, 1.0) == "especialista"
    assert atlas.rotular(40, 0.49) == "generalista"
    assert atlas.MINIMO_DE_CASOS == 2 and atlas.LIMIAR_ESPECIALISTA == 0.5


def _rotas_de_mentira() -> tuple[dict, dict, list[str]]:
    """Seis casos, duas classes: os da classe 1 recuperam `a`, os da classe 2 recuperam `b`, e todos recuperam `g`."""
    rotas = {"c1": ["a", "g"], "c2": ["a", "g"], "c3": ["g", "a", "a"], "c4": ["b", "g"], "c5": ["b", "g"], "c6": ["g", "b"]}
    classe = {"c1": 1, "c2": 1, "c3": 1, "c4": 2, "c5": 2, "c6": 2}
    return rotas, classe, ["a", "b", "g", "z"]


def teste_atlas_de_recuperacao_conta_casos_distintos() -> None:
    rotas, classe, ids = _rotas_de_mentira()
    at = atlas.atlas_de_recuperacao(rotas, classe, ids)
    assert set(at) == set(ids)
    assert at["a"]["n"] == [3, 0] and at["a"]["itens"] == 3, "o verbete repetido na rota do mesmo caso conta uma vez"
    assert at["a"]["rotulo"] == "especialista" and at["a"]["dominante"] == 1 and at["b"]["dominante"] == 2
    assert at["g"]["itens"] == 6 and at["g"]["rotulo"] == "generalista" and at["g"]["especializacao"] == 0.0
    assert at["z"]["itens"] == 0 and at["z"]["rotulo"] == "nunca_recuperado"
    assert at["g"]["vezes_em_primeiro"] == 2 and at["a"]["vezes_em_primeiro"] == 2 and at["b"]["vezes_em_primeiro"] == 2


def teste_atlas_deixar_um_de_fora() -> None:
    rotas, classe, ids = _rotas_de_mentira()
    v = atlas.deixar_um_de_fora(rotas, classe, ids)
    assert (v["total"], v["acertos"], v["empates"], v["sem_evidencia"]) == (6, 6, 0, 0), v
    # um caso que só recupera um verbete que nenhum outro caso recupera: sem ele o atlas não tem o que dizer
    rotas2, classe2 = {**rotas, "c7": ["x"]}, {**classe, "c7": 1}
    v2 = atlas.deixar_um_de_fora(rotas2, classe2, ids + ["x"])
    assert (v2["total"], v2["acertos"], v2["sem_evidencia"]) == (7, 6, 1), v2
    assert v2["erros"] == [{"caso": "c7", "classe": 1, "previsto": None, "motivo": "sem_evidencia"}], v2["erros"]
    # só generalistas, duas classes do mesmo tamanho: empate, que conta como erro
    v3 = atlas.deixar_um_de_fora({"c1": ["g"], "c2": ["g"], "c3": ["g"], "c4": ["g"]}, {"c1": 1, "c2": 1, "c3": 2, "c4": 2}, ["g"])
    assert (v3["total"], v3["acertos"], v3["empates"]) == (4, 0, 4), v3
    assert v2["por_classe"] == [{"classe": 1, "n": 4, "acertos": 3}, {"classe": 2, "n": 3, "acertos": 3}], v2["por_classe"]


def teste_atlas_preve_a_classe_de_casos_novos() -> None:
    rotas, classe, ids = _rotas_de_mentira()
    at = atlas.atlas_de_recuperacao(rotas, classe, ids)
    v = atlas.fora_da_amostra(at, [1, 2], {"n1": ["a", "g"], "n2": ["b"], "n3": ["z"], "n4": ["a", "b"]}, {"n1": 1, "n2": 2, "n3": 1, "n4": 2})
    assert (v["total"], v["acertos"], v["sem_evidencia"], v["empates"]) == (4, 2, 1, 1), v
    previsto, pontos = atlas.prever_classe(["a", "g"], at, [1, 2])
    assert previsto == 1 and pontos == {1: 1.5, 2: 0.5}, (previsto, pontos)


def teste_atlas_posicoes_deterministicas_e_sem_sobreposicao() -> None:
    classes = [1, 2, 3, 4, 5, 6]
    total = {c: 15 for c in classes}
    at = {f"esp{c}_{k}": {**atlas.afinidade({c: 3}, total), "rotulo": "especialista"} for c in classes for k in range(4)}
    at["geral"] = {**atlas.afinidade({c: 7 for c in classes}, total), "rotulo": "generalista"}
    at["nunca1"] = {**atlas.afinidade({}, total), "rotulo": "nunca_recuperado"}
    at["nunca2"] = {**atlas.afinidade({}, total), "rotulo": "nunca_recuperado"}
    pos = atlas.posicoes(at, classes)
    assert pos == atlas.posicoes(dict(reversed(list(at.items()))), classes), "a disposição não depende da ordem de entrada"
    ancoras = atlas.ancoras(classes)
    dist = lambda p, q: ((p["x"] - q["x"]) ** 2 + (p["y"] - q["y"]) ** 2) ** 0.5  # noqa: E731
    centro = {"x": 0.0, "y": 0.0}
    assert dist(pos["geral"], centro) < 0.05, pos["geral"]
    for c in classes:
        for k in range(4):
            p = pos[f"esp{c}_{k}"]
            perto = min(classes, key=lambda x: dist(p, ancoras[x]))
            assert perto == c, (c, k, p)
    dentro = [i for i in pos if not pos[i]["fora"]]
    assert sorted(i for i in pos if pos[i]["fora"]) == ["nunca1", "nunca2"]
    for a in dentro:
        for b in dentro:
            if a < b:
                assert dist(pos[a], pos[b]) >= pos[a]["r"] + pos[b]["r"] - 1e-3, (a, b, dist(pos[a], pos[b]))
    assert pos["geral"]["r"] > pos["esp1_0"]["r"], "o raio cresce com o número de casos"


def teste_atlas_montar_render_e_check() -> None:
    def corpo(tmp: Path) -> None:
        c3b, _ = _corrida_de_mentira("atlas_teste", n_casos=6)
        slug = executar_fase3._slug(_MODELO_SONDA)
        regs = [json.loads(l) for l in (c3b["raiz"] / slug / "diagnosticos__L1.jsonl").read_text(encoding="utf-8").splitlines()]
        # um erro de rótulo e uma fonte fora do contexto, para a confusão e a citação terem o que contar
        certa = regs[0]["gabarito"]["causa_raiz"]
        errada = next(c for c in sorted(avaliar._PERMITIDAS) if c != certa)
        citado = regs[0]["verbetes_ids"][0]
        regs[0]["resposta"] = f"CAUSA_RAIZ: {errada}\nCAMPO: nenhum\nIMPACTO: nada.\nFONTE: [{citado}], [verbete-de-fora]"
        (c3b["raiz"] / slug / "diagnosticos__L1.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in regs) + "\n", encoding="utf-8")
        dado = atlas.montar(corridas=["atlas_teste"], base="atlas_teste", gerado_em="2026-10-01T10:00:00")
        assert [f["id"] for f in dado["fatias"]] == [f"atlas_teste/{slug}/L1"], dado["fatias"]
        f = dado["fatias"][0]
        h = regs[0]["biblioteca_versao"]
        assert f["biblioteca"] == h and f["casos"] == len(regs) and f["acertos"] == len(regs) - 1, f
        assert [certa, errada, 1] in f["confusoes"], f["confusoes"]
        fora = sum(1 for r in regs for i in dict.fromkeys(avaliar.extrair(r["resposta"])["fonte_ids"]) if i not in r["verbetes_ids"])
        assert f["citacoes"][citado]["casos"] >= 1 and f["citados_fora_do_contexto"] == fora >= 1, (f["citados_fora_do_contexto"], fora)
        b = dado["bibliotecas"][h]
        assert set(b["verbetes"]) == {v["id"] for v in bib.carregar(c3b["bibliotecas"] / slug / "epoca-1")}
        assert b["validacao"]["deixando_um_de_fora"]["total"] == len(regs)
        assert set(b["posicoes"]) == set(b["verbetes"])
        for r in regs:
            rota = dado["casos"][r["caso"]]["rotas"][f["id"]]
            assert rota["recuperados"] == r["verbetes_ids"], rota
            assert dado["casos"][r["caso"]]["classe"] == r["classe"]
            assert "classe_da_rota" in rota and (rota["classe_da_rota"] is None or rota["classe_da_rota"] in atlas.CLASSES), rota
        aponta = sum(1 for r in regs if dado["casos"][r["caso"]]["rotas"][f["id"]]["classe_da_rota"] == r["classe"])
        assert f["rota_e_acerto"]["aponta"]["n"] == aponta, (f["rota_e_acerto"], aponta)
        rota0 = dado["casos"][regs[0]["caso"]]["rotas"][f["id"]]
        assert rota0["rotulo"] == errada and rota0["acerto"] is False and rota0["citados"] == [citado, "verbete-de-fora"], rota0
        assert atlas.montar(corridas=["atlas_teste"], base="atlas_teste", gerado_em="2026-10-01T10:00:00") == dado, "montar de novo dá o mesmo dado"
        md = atlas.render(dado)
        for bloco in ("tb_atlas_bibliotecas", "tb_atlas_verbetes", "tb_atlas_validacao", "tb_atlas_fatias"):
            assert f"<!-- tabela:{bloco} -->" in md, bloco
        assert set(a3b.blocos_de(md)) == {"tb_atlas_bibliotecas", "tb_atlas_verbetes", "tb_atlas_validacao", "tb_atlas_fatias"},             "cada bloco fecha com o próprio nome, que é o que a colagem no relatório procura"
        assert "—" not in md and "→" not in md
        pasta = _temp()
        assert pf.fechar(atlas.NOME, dado, md, atlas.PREFIXO, pasta=pasta, doc=pasta / "nao_existe.md") == 0
        assert pf.fechar(atlas.NOME, dado, md, atlas.PREFIXO, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0

    testar_fase3b._com_resultados_temporarios(corpo)


def teste_atlas_dos_dados_reais_bate_com_os_registros() -> None:
    """Com os dados reais: toda biblioteca da corrida oficial tem o atlas sobre os 90 casos, a mesma biblioteca dá a
    mesma rota para o mesmo caso em todos os modelos que a leram, e os acertos de cada fatia são os do avaliador."""
    if not (RA / "fase3" / "qwen2.5_7b" / "diagnosticos__L1.jsonl").exists():
        print("  (pulado: sem resultados_alvo/fase3)")
        return
    anterior = caminhos.RESULTADOS
    caminhos.RESULTADOS = RA
    try:
        dado = atlas.montar(gerado_em="2026-10-01T10:00:00")
        oficiais = [f for f in dado["fatias"] if f["corrida"] == "fase3"]
        assert len(oficiais) == 16 and all(f["casos"] == 90 for f in oficiais), [(f["id"], f["casos"]) for f in oficiais]
        assert dado["metadados"]["divergencias_de_rota"] == [], dado["metadados"]["divergencias_de_rota"][:3]
        for f in oficiais:
            regs = [json.loads(l) for l in (RA / "fase3" / f["slug"] / f"diagnosticos__L{f['versao']}.jsonl").read_text(encoding="utf-8").splitlines()]
            assert f["acertos"] == sum(avaliar.avaliar_registro(r, set())["causa_correta"] for r in regs), f["id"]
            b = dado["bibliotecas"][f["biblioteca"]]
            assert b["casos"] == 90 and sum(b["total_por_classe"]) == 90 and b["validacao"]["deixando_um_de_fora"]["total"] == 90
        original = dado["bibliotecas"][dado["metadados"]["biblioteca_original"]]
        assert sum(1 for v in original["verbetes"].values() if v["itens"]) <= len(original["verbetes"])
        assert all(len(c["rotas"]) >= 1 for c in dado["casos"].values())
    finally:
        caminhos.RESULTADOS = anterior


# ------------------------------------------------------------------ 9. análise da sonda de confiança

def _tok(texto: str, p: float, alternativas: list[tuple[str, float]] | None = None, dados: bytes | None = None) -> dict:
    """Um token na forma do Ollama, com a probabilidade dada (e as alternativas, se houver)."""
    import math
    b = dados if dados is not None else texto.encode("utf-8")
    return {"token": texto, "logprob": math.log(p), "bytes": list(b),
            "top_logprobs": [{"token": texto, "logprob": math.log(p)}] + [{"token": t, "logprob": math.log(q)} for t, q in (alternativas or [])]}


def teste_confianca_trecho_do_rotulo_em_fluxos_sinteticos() -> None:
    import math
    # caso simples: o rótulo sai em três tokens
    simples = [_tok("CAUSA", .99), _tok("_RAIZ", .99), _tok(":", .99), _tok(" campo", .6), _tok("_aus", .9), _tok("ente", .95), _tok("\n", .99),
               _tok("CAMPO", .99), _tok(": preco", .5)]
    t = conf.trecho_do_rotulo(simples)
    assert (t["ini"], t["fim"], t["texto"]) == (3, 6, "campo_ausente"), t
    assert abs(conf.probabilidade_conjunta(simples, t) - .6 * .9 * .95) < 1e-9
    assert abs(conf.probabilidade_do_primeiro(simples, t) - .6) < 1e-9
    # com a marca de negrito em volta do nome da linha
    negrito = [_tok("**", .9), _tok("CAUSA_RAIZ", .9), _tok(":**", .9), _tok(" campo_ausente", .7), _tok("\n", .9)]
    t = conf.trecho_do_rotulo(negrito)
    assert (t["ini"], t["fim"], t["texto"]) == (3, 4, "campo_ausente"), t
    # o fim do rótulo e a quebra de linha no mesmo token: o token inteiro entra na conta
    junto = [_tok("CAUSA_RAIZ", .9), _tok(":", .9), _tok(" tipo", .8), _tok("_divergente\nCAMPO", .5), _tok(": x", .9)]
    t = conf.trecho_do_rotulo(junto)
    assert (t["ini"], t["fim"], t["texto"]) == (2, 4, "tipo_divergente"), t
    assert abs(conf.probabilidade_conjunta(junto, t) - .8 * .5) < 1e-9
    # um acento partido entre dois tokens antes do rótulo: a posição é contada em bytes, não em caracteres
    o_agudo = "ó".encode("utf-8")
    partido = [_tok("Diagn", .9), _tok("�", .9, dados=o_agudo[:1]), _tok("�", .9, dados=o_agudo[1:]), _tok("stico\n", .9),
               _tok("CAUSA_RAIZ", .9), _tok(":", .9), _tok(" corpo", .7), _tok("_vazio", .6), _tok("\n", .9)]
    t = conf.trecho_do_rotulo(partido)
    assert (t["ini"], t["fim"], t["texto"]) == (6, 8, "corpo_vazio"), t
    # sem a linha CAUSA_RAIZ não há trecho
    assert conf.trecho_do_rotulo([_tok("não", .9), _tok(" sei", .9)]) is None
    assert math.isclose(conf.probabilidade_conjunta(partido, t), .42)


def teste_confianca_alternativas_pela_arvore_de_prefixos() -> None:
    causas = sorted(avaliar._PERMITIDAS)
    fluxo = [_tok("CAUSA_RAIZ", .99), _tok(":", .99),
             _tok(" campo", .6, [(" tipo", .3), (" **", .04), (" corpo", .05)]),
             _tok("_ausente", .9, [("_renomeado", .08), ("_aus", .01)]), _tok("\n", .99)]
    t = conf.trecho_do_rotulo(fluxo)
    d = conf.alternativas_divergentes(fluxo, t, causas)
    # " tipo" leva a tipo_divergente; " corpo" leva a duas causas (corpo_nao_e_json e corpo_vazio); "_renomeado" depois
    # de "campo" leva a campo_renomeado e pesa 0,6 x 0,08; " **" não diz nada; "_aus" continua sendo campo_ausente
    assert abs(d["massa_divergente"] - (.3 + .05 + .6 * .08)) < 1e-9, d
    assert d["segunda"]["causas"] == ["tipo_divergente"] and abs(d["segunda"]["p"] - .3) < 1e-9, d["segunda"]
    assert conf.gabarito_na_segunda(d, "tipo_divergente") is True and conf.gabarito_na_segunda(d, "campo_renomeado") is False
    # a alternativa que fecha o rótulo (tem espaço ou quebra depois) só conta se for uma causa inteira
    fecha = [_tok("CAUSA_RAIZ", .99), _tok(":", .99), _tok(" campo", .5, [(" tipo\n", .2), (" corpo_vazio\n", .25)]), _tok("_ausente", .9), _tok("\n", .9)]
    d2 = conf.alternativas_divergentes(fecha, conf.trecho_do_rotulo(fecha), causas)
    assert abs(d2["massa_divergente"] - .25) < 1e-9 and d2["segunda"]["causas"] == ["corpo_vazio"], d2


def teste_confianca_auroc_contra_contagem_de_pares() -> None:
    notas = [.9, .8, .8, .7, .6, .55, .5, .4, .4, .2]
    acertos = [True, True, False, True, True, False, True, False, True, False]
    pares = [(a, b) for a, x in zip(notas, acertos) if x for b, y in zip(notas, acertos) if not y]
    bruto = sum(1.0 if a > b else .5 if a == b else 0.0 for a, b in pares) / len(pares)
    assert abs(conf.auroc(notas, acertos) - bruto) < 1e-12, (conf.auroc(notas, acertos), bruto)
    assert conf.auroc([.1, .2], [True, True]) is None, "sem erro nenhum não há o que separar"
    assert conf.auroc([.9, .1], [True, False]) == 1.0 and conf.auroc([.1, .9], [True, False]) == 0.0
    # sinal de sim ou não: vale a média entre acertar os certos e acusar os errados
    assert abs(conf.auroc([1, 1, 0, 0], [True, False, True, False]) - .5) < 1e-12


def teste_confianca_intervalo_por_reamostragem_dos_casos() -> None:
    notas = [.9, .8, .8, .7, .6, .55, .5, .4, .4, .2] * 3
    acertos = [True, True, False, True, True, False, True, False, True, False] * 3
    grupos = [f"caso-{k}" for k in range(10)] * 3            # cada caso aparece três vezes (três bibliotecas)
    a = conf.auroc_com_intervalo(notas, acertos, grupos, replicas=300, semente=7)
    b = conf.auroc_com_intervalo(notas, acertos, grupos, replicas=300, semente=7)
    assert a == b, "a mesma semente dá o mesmo intervalo"
    assert a["n"] == 30 and a["casos"] == 10 and a["erros"] == 12
    assert a["ic95"][0] <= a["auroc"] <= a["ic95"][1], a
    assert conf.auroc_com_intervalo([.1, .2], [True, True], ["x", "y"])["auroc"] is None


def teste_confianca_risco_por_cobertura_e_revisao() -> None:
    notas = [.9, .8, .7, .6, .5]
    acertos = [True, True, False, True, False]
    pontos = conf.risco_por_cobertura(notas, acertos)
    assert [p["cobertura"] for p in pontos] == [.2, .4, .6, .8, 1.0]
    assert [round(p["risco"], 4) for p in pontos] == [0.0, 0.0, .3333, .25, .4], pontos
    r = conf.revisao(notas, acertos, .4)       # manda para revisão os 2 de menor nota
    assert r == {"revisados": 2, "erros_pegos": 1, "erros": 2, "acertos_revisados": 1, "risco_no_que_sobra": round(1 / 3, 4)}, r
    assert conf.revisao(notas, acertos, 0.0)["revisados"] == 0


def teste_confianca_montar_render_e_check() -> None:
    def corpo(tmp: Path) -> None:
        import math
        c3b, _ = _corrida_de_mentira("confianca_teste", n_casos=6)
        slug = executar_fase3._slug(_MODELO_SONDA)
        regs = [json.loads(l) for l in (c3b["raiz"] / slug / "diagnosticos__L1.jsonl").read_text(encoding="utf-8").splitlines()]
        dado = conf.montar(saida="confianca_teste", replicas=50, gerado_em="2026-10-01T10:00:00")
        assert len(dado["casos"]) == len(regs) and dado["metadados"]["medida_principal"] == "p_conjunta"
        for linha, r in zip(dado["casos"], regs):
            assert linha["caso"] == r["caso"] and linha["rotulo"] == r["gabarito"]["causa_raiz"] and linha["acerto"] is True
            # o Ollama de mentira dá -0,25 a cada pedaço de 3 bytes: a conjunta é exp(-0,25 x pedaços do rótulo)
            assert abs(linha["p_conjunta"] - math.exp(-.25 * linha["tokens_do_rotulo"])) < 1e-6, linha
            assert linha["sustentado"] in (True, False)
        resumo = dado["resumos"][0]
        assert resumo["casos"] == len(regs) and resumo["erros"] == 0 and resumo["sinais"]["p_conjunta"]["auroc"] is None
        md = conf.render(dado)
        assert set(a3b.blocos_de(md)) == {"tb_conf_resumo", "tb_conf_revisao", "tb_conf_casos"}, list(a3b.blocos_de(md))
        assert "—" not in md and "→" not in md
        pasta = _temp()
        assert pf.fechar(conf.NOME, dado, md, conf.PREFIXO, pasta=pasta, doc=pasta / "nao_existe.md") == 0
        assert pf.fechar(conf.NOME, dado, md, conf.PREFIXO, check=True, pasta=pasta, doc=pasta / "nao_existe.md") == 0

    testar_fase3b._com_resultados_temporarios(corpo)


def teste_rodar_sonda_confianca_ps1_bom_e_sem_travessao() -> None:
    """O Windows PowerShell 5.1 lê .ps1 sem BOM na codepage ANSI, e um travessão dentro de string encerra a string;
    a linha FIM trunca as horas com Floor (com [int] sozinho, 1h46 saía como 02h46)."""
    dados = (EXP / "rodar_sonda_confianca.ps1").read_bytes()
    assert dados[:3] == b"\xef\xbb\xbf", "sem BOM"
    texto = dados[3:].decode("utf-8")
    assert "—" not in texto and "–" not in texto
    for script in ("testar_fase3.py", "testar_fase3b.py", "testar_pre_fase4.py", "sonda_confianca.py", "analisar_confianca.py"):
        assert script in texto, script
    assert "[int][math]::Floor($duracao.TotalHours)" in texto
    assert "de IA - Revisar" in texto and "! Motivo:" in texto


# ------------------------------------------------------------------ 9. área só de leitura (depois)

def teste_area_so_de_leitura_hash_depois() -> None:
    """Último teste do arquivo: nenhuma pasta oficial mudou durante a suíte."""
    for nome, pasta in _SO_LEITURA.items():
        agora = testar_fase3b._hash_arvore(pasta)
        assert agora == _HASH_ANTES[nome], f"{nome} mudou durante os testes da Pré-Fase 4: {_HASH_ANTES[nome]} -> {agora}"


# ------------------------------------------------------------------ runner

def main() -> None:
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
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
        for caminho in _TEMPORARIOS + testar_fase3b._TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
