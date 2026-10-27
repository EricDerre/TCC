#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (01/10/2026, Pré-Fase 4) com a TRILHA do agente: o arquivo bruto, uma linha
# JSON por evento, com tudo o que o programa fez num diagnóstico, na ordem em que fez (o caso que entrou, os verbetes
# que a busca pontuou e os que escolheu, o prompt montado, a resposta do modelo, o que o modelo declarou e o que o
# código conferiu de cada declaração). Traz o formato do evento, o escritor que numera e não repete texto grande, as
# funções que acham na resposta o trecho exato de cada declaração e conferem cada uma, e o adaptador que remonta a
# trilha das corridas JÁ GRAVADAS da Fase 3 e da Fase 3-B, sem rodar modelo.
# ! Motivo: o Eric pediu (01/10/2026) que o "pensamento" da IA fique aberto: um arquivo bruto, "como um programa
# rodando no cmd", e um relatório para humanos gerado dele. Hoje o harness guarda a resposta e os ids do contexto,
# mas não o prompt nem as pontuações da busca, e nenhum gerador segue um caso por todas as etapas. O levantamento do
# projeto já registra que a explicação escrita por modelo desse porte não pode ser lida como explicação auditável, por
# isso o formato separa três camadas e nunca as mistura: o que o PROGRAMA fez (fato), o que o MODELO declarou
# (alegação, sempre como trecho literal da resposta) e o que o código VERIFICOU. Cada evento diz também de onde veio:
# gravado na corrida (`registro`), refeito agora a partir dos mesmos insumos (`recalculado`), julgado por pessoa
# (`humano`) ou emitido na hora (`ao_vivo`, para a Fase 4). O prompt de diagnóstico não foi gravado nas corridas: ele
# é remontado pelas mesmas funções do executor, e a trilha diz até onde essa remontagem está provada (hash da
# biblioteca, hash do contexto e, nos casos de aprendizado, o prompt de proposta gravado, que começa pelo de
# diagnóstico). Os arquivos congelados (executar_fase3.py, estrategias.py, evolucao_biblioteca.py) são só importados.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python trilha.py --errata
  RESULTADOS_DIR=resultados_alvo python trilha.py --corrida fase3 --modelo qwen2.5:7b --versao 1 [--saida ARQUIVO]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import biblioteca as bib
import caminhos
import cliente_ollama as oll
import curar_biblioteca as curar
import estrategias
import evolucao_biblioteca as evo
import executar_fase3
import recuperacao as rec
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

V = 1
CAMADA_DO_TIPO = {"corrida": "programa", "blob": "programa", "entrada": "programa", "candidatos": "programa", "prompt": "programa",
                  "inferencia": "programa", "declaracao": "modelo", "verificacao": "verificacao", "acao": "programa"}
ORIGENS = ("ao_vivo", "registro", "recalculado", "humano")
# ! Alteração de IA - Revisar: versão 2 do esquema (26/10/2026, Fase 4, pacote P1): os tipos novos da especificação da
# trilha (seção 3.3), as decisões fechadas do nó (4.2), as camadas, os papéis de evidência, os selos, a taxonomia de
# falhas (seção 8), os limites declarados (ficha 33) e a tabela de exportação para os nomes gen_ai (3.4, só nomes).
# O adaptador das corridas gravadas continua escrevendo a versão 1 (`V`), byte a byte como antes.
# ! Motivo: a Fase 4 emite a trilha ao vivo e precisa do cabeçalho de corrida, do nó de decisão com alternativas e
# divergência obrigatória e dos limites de tamanho; sem a versão separada, a vitrine da Pré-Fase 4 (três trilhas
# regeradas e conferidas byte a byte por `gerar_relatorio_raciocinio.py --vitrine --check`) mudaria de forma.
V2 = 2
TIPOS_V2 = {"interceptacao": "programa", "poda": "programa", "decisao": "programa", "intervencao": "verificacao",
            "cura": "programa", "edicao_biblioteca": "programa", "incidente": "programa", "revisao": "humano"}
CAMADA_DO_TIPO_V2 = {**CAMADA_DO_TIPO, **TIPOS_V2}
CAMADAS = ("programa", "modelo", "verificacao")
DECISOES = ("interceptacao", "poda", "recuperacao", "montagem_do_prompt", "diagnostico", "cura", "edicao_biblioteca", "reexecucao")
DECISOES_DE_CURA = ("cura", "reexecucao")
PAPEIS_DE_EVIDENCIA = ("sinal_em_codigo", "verbete_entregue", "verbete_citado", "corpo_http", "arvore_podada", "candidato_de_seletor",
                       "trace", "contrato", "resposta")
PAPEIS_COM_VERBETE = ("verbete_entregue", "verbete_citado")
SELOS = ("alto", "medio", "baixo")
TAXONOMIA_DE_FALHAS = {
    "programa": ("interceptacao_incompleta", "poda_removeu_evidencia", "busca_sem_verbete_relevante", "prompt_diferente_do_fixo",
                 "formato_das_quatro_linhas"),
    "modelo": ("rotulo_errado", "rotulo_fora_da_taxonomia", "campo_errado", "citacao_fora_do_contexto", "citacao_inexistente",
               "causa_sem_verbete_que_a_trate"),
    "cura": ("candidato_invalido", "candidato_ambiguo", "reexecucao_falhou"),
    "biblioteca": ("acrescimo_recusado_pela_validacao", "texto_de_origem_proibida"),
    "harness": ("incidente",),
}
LIMITES_PADRAO = {"nos_por_diagnostico": 40, "nos_por_cura": 20, "blob_inline_max_chars": 64 * 1024, "retencao_meses": 6}
NOMES_GEN_AI = {"diagnostico": "chat", "cura": "execute_tool", "poda": "plan", "recuperacao": "retrieval"}
# Casos de texto corrigido em 28/09/2026 (achado 4.36): as corridas anteriores a essa data leram o texto antigo, que
# sai do git (último commit antes da correção) para a errata.
COMMIT_ANTES_DA_CORRECAO = "6a4381f8"
ARQUIVOS_DOS_CASOS = ("Programacao/AgenteCore/experimentos/banco_casos.py", "Programacao/AgenteCore/experimentos/banco_casos_extra.py")
RAIZ_DO_REPOSITORIO = Path(__file__).resolve().parent.parent.parent.parent


def sha(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


def pasta_derivados() -> Path:
    """resultados/pre_fase4 sob o RESULTADOS_DIR em uso (lido na hora, porque os testes trocam a raiz)."""
    return caminhos.RESULTADOS / "pre_fase4"


# ------------------------------------------------------------------ o arquivo bruto

class Trilha:
    """Escritor da trilha: acumula os eventos na ordem, numera (`seq` no arquivo, `passo` dentro de cada trilha) e
    grava cada texto grande uma vez só, como evento `blob` identificado pelo hash; os outros eventos citam o hash.
    ! Alteração de IA - Revisar: (26/10/2026, P1) o escritor ganhou a versão 2: `Trilha(versao=V2, limites, pasta_blobs)`
    exige o cabeçalho de corrida antes de tudo (`corrida()`), `ts` em todo evento `ao_vivo`, aceita os tipos novos,
    valida cada nó de decisão (`decisao()`), conta os nós por diagnóstico e por cura contra os limites, manda para
    arquivo ao lado o blob acima do limite inline e fecha a corrida com fim e tamanho (`fechar()`); `carregar()` lê um
    arquivo da versão 1 ou 2 e continua numerando de onde ele parou. `Trilha()` sem argumentos é a versão 1 de sempre.
    ! Motivo: especificação da trilha, seções 3.1 (cabeçalho, texto grande uma vez, limites declarados), 3.2 (`ao_vivo`
    com hora) e 4.2 (nó de decisão); o adaptador das corridas gravadas precisa continuar byte a byte igual."""

    def __init__(self, versao: int = V, limites: dict | None = None, pasta_blobs: Path | None = None) -> None:
        if versao not in (V, V2):
            raise ValueError(f"versão do esquema desconhecida: {versao!r}")
        self.versao = versao
        self.limites = dict(LIMITES_PADRAO, **(limites or {}))
        self.pasta_blobs = Path(pasta_blobs) if pasta_blobs else None
        self.ts_padrao: str | None = None
        self.eventos: list[dict] = []
        self._blobs: set[str] = set()
        self._passos: dict[str, int] = {}
        self._nos: dict[str, dict[str, int]] = {}

    @property
    def camadas(self) -> dict[str, str]:
        return CAMADA_DO_TIPO if self.versao == V else CAMADA_DO_TIPO_V2

    def _novo(self, tipo: str, trilha: str | None, dados: dict, origem: str, pai: int | None, ts: str | None) -> int:
        if tipo not in self.camadas:
            raise ValueError(f"tipo de evento desconhecido: {tipo!r}")
        if origem not in ORIGENS:
            raise ValueError(f"origem desconhecida: {origem!r}")
        if self.versao == V2:
            if tipo != "corrida" and not self.eventos:
                raise ValueError("cabeçalho de corrida ausente: chame corrida() antes do primeiro evento")
            if origem == "ao_vivo" and not ts:
                raise ValueError(f"evento {tipo!r} com origem ao_vivo sem ts")
        passo = None
        if trilha is not None:
            passo = self._passos[trilha] = self._passos.get(trilha, 0) + 1
        seq = len(self.eventos) + 1
        self.eventos.append({"v": self.versao, "seq": seq, "trilha": trilha, "passo": passo, "pai": pai, "tipo": tipo,
                             "camada": self.camadas[tipo], "origem": origem, "ts": ts, "dados": dados})
        if ts:
            self.ts_padrao = ts
        return seq

    def blob(self, texto: str, papel: str) -> str:
        h = sha(texto)
        if h in self._blobs:
            return h
        self._blobs.add(h)
        if self.versao == V:
            self._novo("blob", None, {"sha": h, "papel": papel, "chars": len(texto), "texto": texto}, "registro", None, None)
            return h
        dados: dict = {"sha": h, "papel": papel, "chars": len(texto), "texto": texto}
        if len(texto) > self.limites["blob_inline_max_chars"]:
            if self.pasta_blobs is None:
                raise ValueError(f"blob de {len(texto)} caracteres acima do limite inline ({self.limites['blob_inline_max_chars']}) "
                                 "e a trilha não tem pasta de blobs")
            self.pasta_blobs.mkdir(parents=True, exist_ok=True)
            (self.pasta_blobs / f"{h}.txt").write_text(texto, encoding="utf-8", newline="\n")
            dados = {**dados, "texto": None, "arquivo": f"{self.pasta_blobs.name}/{h}.txt"}
        self._novo("blob", None, dados, "ao_vivo", None, self.ts_padrao)
        return h

    def evento(self, tipo: str, trilha: str, dados: dict, origem: str, pai: int | None = None, ts: str | None = None) -> int:
        if self.versao == V2 and tipo == "corrida":
            raise ValueError("cabeçalho de corrida: use corrida(dados, ts)")
        return self._novo(tipo, trilha, dados, origem, pai, ts)

    def corrida(self, dados: dict, ts: str | None = None, origem: str = "ao_vivo") -> int:
        """O cabeçalho da corrida, primeiro evento da trilha v2 (seção 3.1), validado por validar_cabecalho."""
        if self.versao != V2:
            raise ValueError("corrida() é da versão 2; na versão 1 o adaptador grava o evento corrida por evento()")
        if self.eventos:
            raise ValueError("cabeçalho de corrida: só pode ser o primeiro evento")
        validar_cabecalho(dados)
        return self._novo("corrida", dados.get("corrida"), dados, origem, None, ts)

    def decisao(self, trilha: str, no: dict, pai: int | None = None, ts: str | None = None, origem: str = "ao_vivo") -> int:
        """Um nó de decisão (seção 4.2), validado e contado contra os limites de nós por diagnóstico e por cura."""
        if self.versao != V2:
            raise ValueError("nó de decisão é da versão 2 da trilha")
        validar_no(no)
        chave = "nos_por_cura" if no["decisao"] in DECISOES_DE_CURA else "nos_por_diagnostico"
        contagem = self._nos.setdefault(trilha, {"nos_por_diagnostico": 0, "nos_por_cura": 0})
        if contagem[chave] + 1 > self.limites[chave]:
            raise ValueError(f"limite {chave} ({self.limites[chave]}) excedido na trilha {trilha!r}")
        contagem[chave] += 1
        return self._novo("decisao", trilha, no, origem, pai, ts)

    def fechar(self, fim: str) -> None:
        """Grava no cabeçalho a hora de fim e o tamanho do arquivo (eventos, caracteres, blobs fora da linha); o tamanho
        é recalculado até o próprio cabeçalho parar de mudar de comprimento."""
        if self.versao != V2 or not self.eventos or self.eventos[0]["tipo"] != "corrida":
            raise ValueError("fechar() precisa de uma trilha v2 com o cabeçalho de corrida")
        cab = self.eventos[0]["dados"]
        cab["fim"] = fim
        externos = sum(1 for e in self.eventos if e["tipo"] == "blob" and e["dados"].get("arquivo"))
        for _ in range(6):
            chars = sum(len(l) + 1 for l in self.linhas())
            tamanho = {"eventos": len(self.eventos), "chars": chars, "blobs_externos": externos}
            if cab.get("tamanho") == tamanho:
                return
            cab["tamanho"] = tamanho
        raise ValueError("o tamanho do cabeçalho não estabilizou")

    @classmethod
    def carregar(cls, caminho: Path) -> "Trilha":
        """Lê um arquivo da versão 1 ou 2 e devolve o escritor pronto para continuar numerando de onde ele parou."""
        eventos = ler(caminho)
        t = cls(versao=versao_do_arquivo(eventos))
        t.eventos = eventos
        for e in eventos:
            if e["tipo"] == "blob":
                t._blobs.add(e["dados"]["sha"])
            if e["trilha"] is not None and e.get("passo") is not None:
                t._passos[e["trilha"]] = max(t._passos.get(e["trilha"], 0), e["passo"])
            if e["tipo"] == "decisao":
                chave = "nos_por_cura" if e["dados"].get("decisao") in DECISOES_DE_CURA else "nos_por_diagnostico"
                t._nos.setdefault(e["trilha"], {"nos_por_diagnostico": 0, "nos_por_cura": 0})[chave] += 1
            if e.get("ts"):
                t.ts_padrao = e["ts"]
        cab = eventos[0]["dados"] if eventos and eventos[0]["tipo"] == "corrida" else {}
        if isinstance(cab.get("limites"), dict):
            t.limites = dict(LIMITES_PADRAO, **cab["limites"])
        return t

    def linhas(self) -> list[str]:
        return [json.dumps(e, ensure_ascii=False, sort_keys=True) for e in self.eventos]

    def gravar(self, caminho: Path) -> None:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text("\n".join(self.linhas()) + "\n", encoding="utf-8", newline="\n")


def ler(caminho: Path) -> list[dict]:
    return [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]


def versao_do_arquivo(eventos: list[dict]) -> int:
    """A maior versão de esquema entre os eventos (1 quando o campo falta): o leitor v2 lê os dois."""
    return max((int(e.get("v", V)) for e in eventos), default=V)


def validar_cabecalho(dados: dict) -> None:
    for chave in ("modelo", "versao_ollama", "inicio"):
        if not isinstance(dados.get(chave), str) or not dados[chave].strip():
            raise ValueError(f"cabeçalho de corrida sem {chave}")
    if dados.get("versao_do_esquema") != V2:
        raise ValueError(f"cabeçalho de corrida com versao_do_esquema {dados.get('versao_do_esquema')!r}; esperado {V2}")
    limites = dados.get("limites")
    if not isinstance(limites, dict) or any(k not in limites for k in LIMITES_PADRAO):
        raise ValueError(f"cabeçalho de corrida sem os limites declarados {sorted(LIMITES_PADRAO)}")


def cabecalho_de_corrida(modelo: str, versao_ollama: str, inicio: str, quantizacao: str | None = None, top_logprobs: int = 20,
                         leitura_da_probabilidade: str = "primeiro_token_do_rotulo", num_ctx: int | None = None,
                         temperatura: float | None = None, semente: int | None = None, hash_biblioteca: str | None = None,
                         hash_prompt_fixo: str | None = None, hash_indice: str | None = None, playwright: str | None = None,
                         navegador: str | None = None, canal: str | None = None, limites: dict | None = None,
                         etapas_registradas: tuple | list = (), etapas_nao_registradas: tuple | list = (),
                         corrida: str | None = None, extras: dict | None = None) -> dict:
    """! Alteração de IA - Revisar: o cabeçalho de corrida da versão 2 (especificação, seções 3.1 e 13): modelo,
    quantização, versão do Ollama, `top_logprobs` e modo de leitura da probabilidade, `num_ctx`, temperatura, semente,
    hash da biblioteca, do prompt fixo e do índice BM25, versão do Playwright e do navegador, início e fim, limites
    declarados, etapas registradas e não registradas, retenção e a decisão de gravar prompt e resposta inteiros.
    ! Motivo: é o que permite comparar corridas quando o Ollama se atualiza sozinho (decisões 44 e 47) ou quando a
    build do navegador muda; `fim` e `tamanho` ficam vazios até fechar()."""
    for nome, valor in (("modelo", modelo), ("versao_ollama", versao_ollama), ("inicio", inicio)):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"cabeçalho de corrida sem {nome}")
    lim = dict(LIMITES_PADRAO, **(limites or {}))
    cab = {"versao_do_esquema": V2, "corrida": corrida, "modelo": modelo, "quantizacao": quantizacao, "versao_ollama": versao_ollama,
           "top_logprobs": top_logprobs, "leitura_da_probabilidade": leitura_da_probabilidade,
           "num_ctx": oll.NUM_CTX if num_ctx is None else num_ctx, "temperatura": oll.TEMPERATURA if temperatura is None else temperatura,
           "semente": semente, "hash_biblioteca": hash_biblioteca, "hash_prompt_fixo": hash_prompt_fixo, "hash_indice": hash_indice,
           "playwright": playwright, "navegador": navegador, "canal": canal, "inicio": inicio, "fim": None, "tamanho": None,
           "limites": lim, "etapas_registradas": list(etapas_registradas), "etapas_nao_registradas": list(etapas_nao_registradas),
           "grava_prompt_e_resposta_completos": True, "retencao_meses": lim["retencao_meses"], **(extras or {})}
    validar_cabecalho(cab)
    return cab


def origem_da_falha(tipo: str | None) -> str | None:
    """A origem (programa, modelo, cura, biblioteca, harness) de um tipo da taxonomia de falhas, ou None se não existir."""
    for origem, tipos in TAXONOMIA_DE_FALHAS.items():
        if tipo in tipos:
            return origem
    return None


def validar_no(no: dict) -> None:
    """As regras dos campos do nó de decisão (especificação, seção 4.2); a divergência é obrigatória."""
    if no.get("decisao") not in DECISOES:
        raise ValueError(f"decisao {no.get('decisao')!r} fora de {DECISOES}")
    alternativas = no.get("alternativas") or []
    for a in alternativas:
        if not isinstance(a, dict) or "opcao" not in a:
            raise ValueError("alternativa sem o campo 'opcao'")
    opcoes = [a["opcao"] for a in alternativas]
    if alternativas and no.get("escolha") not in opcoes:
        raise ValueError(f"escolha {no.get('escolha')!r} fora das alternativas {opcoes}")
    for e in no.get("evidencia") or []:
        if not isinstance(e, dict) or not isinstance(e.get("seq"), int) or not e.get("papel"):
            raise ValueError("evidencia precisa apontar um evento: seq (inteiro) e papel")
        if "texto" in e or "valor" in e:
            raise ValueError("evidencia aponta eventos, nunca copia texto")
    d = no.get("divergencia")
    if not isinstance(d, dict) or any(k not in d for k in ("ha", "entre", "detalhe")):
        raise ValueError("nó sem divergencia preenchida: precisa de {ha, entre, detalhe}")
    if not isinstance(d["ha"], bool) or not isinstance(d["entre"], list):
        raise ValueError("divergencia: 'ha' é True ou False e 'entre' é a lista de camadas")
    for camada in d["entre"]:
        if camada not in CAMADAS:
            raise ValueError(f"divergencia.entre com camada desconhecida {camada!r}; esperado {CAMADAS}")
    c = no.get("confianca")
    if c is not None:
        if not isinstance(c, dict):
            raise ValueError("confianca precisa ser um dicionário com a probabilidade do rótulo e o selo")
        if c.get("selo") is not None and c["selo"] not in SELOS:
            raise ValueError(f"selo {c['selo']!r} fora de {SELOS}")
    falha = no.get("falha")
    if falha is not None and origem_da_falha(falha) is None:
        raise ValueError(f"falha {falha!r} fora da taxonomia de falhas")
    prov = no.get("prov") or {}
    for chave in ("used", "wasDerivedFrom"):
        if not isinstance(prov.get(chave, []), list):
            raise ValueError(f"prov.{chave} precisa ser uma lista")


def no_de_decisao(decisao: str, escolha, alternativas=(), evidencia=(), resultado: str | None = None, divergencia: dict | None = None,
                  confianca: dict | None = None, prov: dict | None = None, falha: str | None = None, contraste: str | None = None,
                  justificativa: str | None = None, extras: dict | None = None) -> dict:
    """! Alteração de IA - Revisar: monta e valida um nó de decisão (especificação, seção 4.2): decisão fechada,
    alternativas com escore, escolha entre elas, evidência que aponta eventos, resultado, contraste e justificativa
    (preenchidos pelo molde do relatório), divergência obrigatória, confiança (probabilidade do rótulo e selo), falha da
    taxonomia e as arestas PROV (`used`, `wasDerivedFrom`, `wasGeneratedBy`).
    ! Motivo: o nó é o que leva o desenvolvedor ao ponto do erro; sem a validação, um nó sem divergência ou com texto
    copiado na evidência entraria na trilha e o relatório não teria como marcar o conflito."""
    no = {"decisao": decisao, "alternativas": [dict(a) for a in alternativas], "escolha": escolha,
          "evidencia": [dict(e) for e in evidencia], "resultado": resultado, "contraste": contraste, "divergencia": divergencia,
          "confianca": confianca, "justificativa": justificativa, "falha": falha,
          "prov": {"used": [], "wasDerivedFrom": [], "wasGeneratedBy": None, **(prov or {})}, **(extras or {})}
    validar_no(no)
    return no


def exportar_nome_gen_ai(decisao: str) -> str | None:
    """O nome da operação gen_ai equivalente (só o nome; o esquema não muda), ou None quando não há par."""
    return NOMES_GEN_AI.get(decisao)


def _nos_por_trilha(eventos: list[dict]) -> dict[str, list[dict]]:
    saida: dict[str, list[dict]] = {}
    for e in eventos:
        if e["tipo"] == "decisao" and e["trilha"] is not None:
            saida.setdefault(e["trilha"], []).append({"decisao": e["dados"].get("decisao"), "escolha": e["dados"].get("escolha")})
    return saida


def diff_contra_referencia(nova: list[dict], referencia: list[dict]) -> dict:
    """! Alteração de IA - Revisar: diff determinístico entre duas trilhas (especificação, seção 9): para cada trilha
    presente nas duas, compara a sequência de nós de decisão (decisão e escolha) com casamento exato e marca o primeiro
    nó divergente (posição a partir de 1; `obtido` None quando a nova acabou antes). Lista também as trilhas que só
    existem num dos lados.
    ! Motivo: regressão por trilha de referência sem custo de modelo; regras determinísticas no lugar de um juiz por
    LLM (mapa linha 21: abaixo de 70% de precisão)."""
    a, b = _nos_por_trilha(nova), _nos_por_trilha(referencia)
    divergencias = []
    for tid, ref in b.items():
        if tid not in a:
            continue
        obt = a[tid]
        for i in range(max(len(ref), len(obt))):
            esperado = ref[i] if i < len(ref) else None
            obtido = obt[i] if i < len(obt) else None
            if esperado != obtido:
                divergencias.append({"trilha": tid, "posicao": i + 1, "esperado": esperado, "obtido": obtido})
                break
    return {"trilhas_comparadas": len(set(a) & set(b)), "divergencias": divergencias,
            "so_na_nova": sorted(set(a) - set(b)), "so_na_referencia": sorted(set(b) - set(a))}


def regressoes(diff: dict, anterior: dict | None = None, limiar_ruido: int = 3) -> dict:
    """Uma divergência só vira regressão quando se repete em duas corridas (a mesma trilha e a mesma posição em
    `anterior`) ou quando o número de trilhas divergentes passa do limiar de ruído (0 a 3 casos em 36 entre corridas
    iguais, relatório da Fase 3-B)."""
    divergentes = len({d["trilha"] for d in diff["divergencias"]})
    dentro = divergentes <= limiar_ruido
    repetidas = {(d["trilha"], d["posicao"]) for d in (anterior or {}).get("divergencias", [])}
    regs = [d for d in diff["divergencias"] if not dentro or (d["trilha"], d["posicao"]) in repetidas]
    return {"divergentes": divergentes, "limiar_ruido": limiar_ruido, "dentro_do_ruido": dentro, "regressoes": regs}


def por_trilha(eventos: list[dict]) -> dict[str, list[dict]]:
    """Os eventos agrupados pela trilha, na ordem do arquivo (os blobs, que não são de trilha nenhuma, ficam de fora)."""
    saida: dict[str, list[dict]] = {}
    for e in eventos:
        if e["trilha"] is not None:
            saida.setdefault(e["trilha"], []).append(e)
    return saida


def blobs_de(eventos: list[dict], pasta: Path | None = None) -> dict[str, str | None]:
    """{sha: texto}; um blob gravado fora da linha (v2, acima do limite inline) vem None, ou lido do arquivo ao lado
    quando `pasta` é dada."""
    saida: dict[str, str | None] = {}
    for e in eventos:
        if e["tipo"] != "blob":
            continue
        texto = e["dados"].get("texto")
        if texto is None and pasta is not None and e["dados"].get("arquivo"):
            arquivo = Path(pasta) / Path(e["dados"]["arquivo"]).name
            texto = arquivo.read_text(encoding="utf-8") if arquivo.exists() else None
        saida[e["dados"]["sha"]] = texto
    return saida


# ------------------------------------------------------------------ o que o modelo declarou

_CAMPOS = (("causa_raiz", "CAUSA_RAIZ"), ("campo", "CAMPO"), ("impacto", "IMPACTO"), ("fonte", "FONTE"))
_MARCAS = "*`"


def localizar_declaracoes(resposta: str) -> dict:
    """Acha na resposta o trecho exato de cada linha pedida pelo prompt (CAUSA_RAIZ, CAMPO, IMPACTO, FONTE), de cada
    verbete citado e do texto que vem antes delas (o raciocínio). A leitura é a de avaliar.extrair, para a trilha e a
    avaliação nunca lerem a mesma resposta de dois jeitos: `lido` é o que o avaliador leu; `valor`, `ini` e `fim` são
    o trecho como o modelo escreveu, de modo que resposta[ini:fim] == valor."""
    mapa = [i for i, ch in enumerate(resposta) if ch not in _MARCAS]      # posição na resposta de cada caractere sem as marcas
    limpa = "".join(resposta[i] for i in mapa)

    def trecho(a: int, b: int) -> dict:
        ini, fim = mapa[a], mapa[b - 1] + 1
        return {"valor": resposta[ini:fim], "ini": ini, "fim": fim}

    campos: dict[str, dict | None] = {}
    fontes: list[dict] = []
    inicios = []
    for chave, nome in _CAMPOS:
        m = re.search(rf"{nome}\s*:\s*(.+)", limpa, re.IGNORECASE)
        if not m:
            campos[chave] = None
            continue
        inicios.append(mapa[m.start()])
        a, bruto = m.start(1), m.group(1)
        if chave == "causa_raiz":
            palavras = bruto.split()
            alvo = palavras[0] if palavras else ""      # a causa é a primeira palavra da linha
        else:
            alvo = bruto.strip()
        if not alvo:
            campos[chave] = None
            continue
        a2 = a + bruto.index(alvo)
        campos[chave] = trecho(a2, a2 + len(alvo))
        if chave == "fonte":
            for g in re.finditer(r"\[([a-z0-9_\-]+)\]", bruto):
                fontes.append(trecho(a + g.start(1), a + g.end(1)))
    fim_r = len(resposta) if not inicios else len(resposta[:min(inicios)].rstrip(_MARCAS + " \t\r\n#>-"))
    return {"lido": avaliar.extrair(resposta), "campos": campos, "fontes": fontes,
            "raciocinio": {"valor": resposta[:fim_r].strip(), "ini": 0, "fim": fim_r}}


# ------------------------------------------------------------------ o que o programa fez

def partes_do_prompt(verbetes: list[dict], ctx: dict, caso: dict, prompt: str) -> list[dict]:
    """O prompt de diagnóstico repartido em partes nomeadas (cabeçalho da documentação, cada verbete recuperado,
    instrução, dados do caso e formato da resposta). Cada parte leva o separador que vem antes dela, de modo que
    encadear `antes + texto` devolve o prompt byte a byte. A instrução e o formato são iguais em todos os casos, e um
    verbete se repete em muitos: guardados pelo hash, entram uma vez só no arquivo."""
    por_id = {v["id"]: v for v in verbetes}
    partes = [{"papel": "cabecalho_da_documentacao", "texto": bib.CABECALHO, "antes": ""}]
    partes += [{"papel": "verbete", "id": i, "texto": bib.render(por_id[i]), "antes": "\n\n"} for i in ctx["verbetes_ids"]]
    contexto = "".join(p["antes"] + p["texto"] for p in partes)
    if contexto != ctx["texto"]:
        raise ValueError("o contexto não é o da condição A2 (cabeçalho e verbetes recuperados): repartição não prevista")
    dados = estrategias._dados_do_caso(caso)
    pos = prompt.index(dados, len(contexto))
    meio, resto = prompt[len(contexto):pos], prompt[pos + len(dados):]

    def parte(papel: str, bloco: str) -> dict:
        texto = bloco.lstrip("\n")
        return {"papel": papel, "texto": texto, "antes": bloco[:len(bloco) - len(texto)]}

    instrucao = meio.rstrip("\n")
    partes.append(parte("instrucao", instrucao))
    partes.append({"papel": "caso", "texto": dados, "antes": meio[len(instrucao):]})
    partes.append(parte("formato", resto))
    if "".join(p["antes"] + p["texto"] for p in partes) != prompt:
        raise ValueError(f"caso {caso['id']}: as partes não remontam o prompt")
    return partes


def candidatos(indice: rec.Indice, caso: dict, k: int) -> tuple[dict, list[dict]]:
    """Todos os verbetes na ordem em que a busca os pontuou para o caso, com a pontuação repartida (BM25 e os três
    reforços calculados em código) e a marca dos k escolhidos. É a conta de recuperacao.pontuar refeita por
    componente; a soma é conferida contra a pontuação oficial."""
    s = rec.sinais_do_caso(caso)
    componentes = {}
    for i, v in enumerate(indice.verbetes):
        m = v["meta"]
        componentes[v["id"]] = (
            indice.bm25(s["consulta"], i),
            rec.PESO_ENDPOINT if s["endpoint"] and s["endpoint"] in m.get("endpoints", []) else 0.0,
            rec.PESO_ENTIDADE if s["entidade"] and s["entidade"] == m.get("entidade_principal") else 0.0,
            rec.PESO_STATUS if s["status"] is not None and str(s["status"]) in indice.tf[i] else 0.0)
    itens = []
    for posicao, (pontos, v) in enumerate(rec.pontuar(indice, caso), 1):
        bm, endpoint, entidade, status = componentes[v["id"]]
        if abs(bm + endpoint + entidade + status - pontos) > 1e-9:
            raise ValueError(f"caso {caso['id']}, verbete {v['id']}: a soma dos componentes não dá a pontuação da busca")
        itens.append({"id": v["id"], "posicao": posicao, "pontuacao": round(pontos, 4), "bm25": round(bm, 4),
                      "reforco_endpoint": endpoint, "reforco_entidade": entidade, "reforco_status": status,
                      "escolhido": posicao <= k})
    return {"endpoint": s["endpoint"], "entidade": s["entidade"], "status": s["status"], "termos": len(s["consulta"])}, itens


def provar(registro: dict, hash_do_snapshot: str, ctx: dict, prompt: str, proposta: dict | None,
           sha_enviado: str | None = None) -> dict:
    """Até onde o prompt remontado é, com certeza, o que o modelo recebeu. `biblioteca`: o snapshot lido agora tem o
    hash gravado no registro. `contexto`: os mesmos verbetes, o mesmo tamanho e o mesmo hash do contexto gravado (esse
    hash cobre só a documentação, não o texto do caso). `prompt_de_proposta`: nos casos de aprendizado, o prompt de
    proposta gravado começa pelo prompt remontado mais a resposta, o que prova o prompt todo, texto do caso incluído.
    `hash_do_prompt_enviado`: nas corridas da Pré-Fase 4, o arquivo lateral guarda o hash do prompt que foi de fato ao
    Ollama. As duas últimas valem None quando a corrida não deixou o dado. Nível: `prompt_inteiro` quando uma delas
    confere; `contexto` quando só a documentação está provada; `nao_comprovado` quando alguma prova falha."""
    biblioteca = hash_do_snapshot == registro.get("biblioteca_versao")
    contexto = (ctx["verbetes_ids"] == registro.get("verbetes_ids") and len(ctx["texto"]) == registro.get("chars_contexto")
                and executar_fase3._sha12(ctx["texto"]) == registro.get("contexto_sha256"))
    da_proposta = None if proposta is None else str(proposta.get("prompt", "")).startswith(prompt + "\n\n" + registro["resposta"] + "\n\n")
    do_envio = None if sha_enviado is None else hashlib.sha256(prompt.encode("utf-8")).hexdigest().startswith(sha_enviado)
    if da_proposta is False or do_envio is False or not (biblioteca and contexto):
        nivel = "nao_comprovado"
    elif da_proposta or do_envio:
        nivel = "prompt_inteiro"
    else:
        nivel = "contexto"
    return {"provas": {"biblioteca": biblioteca, "contexto": contexto, "prompt_de_proposta": da_proposta,
                       "hash_do_prompt_enviado": do_envio}, "nivel": nivel}


# ------------------------------------------------------------------ o que o código conferiu

def _v(regra: str, alvo, resultado: str, evidencia=None, usa_gabarito: bool = False) -> dict:
    return {"regra": regra, "alvo": alvo, "resultado": resultado, "evidencia": evidencia, "usa_gabarito": usa_gabarito}


def _texto_do_caso(caso: dict) -> str:
    e = caso["entrada"]
    return avaliar._normalizar(" ".join(str(e.get(k, "")) for k in ("contrato", "corpo", "requisicao", "arvore", "seletor_quebrado")))


def verificar(registro: dict, caso: dict, verbetes: list[dict], decl: dict, vereditos: dict | None = None,
              com_gabarito: bool = True) -> list[dict]:
    """As conferências que o código faz sobre o que o modelo declarou, em ordem fixa. As que não dependem do gabarito
    vêm primeiro (são as que o agente poderá fazer sozinho na Fase 4); as três que dependem dele vêm por último e
    levam `usa_gabarito`. O que não dá para conferir por código é dito (`nao_verificavel`), não omitido.
    ! Alteração de IA - Revisar: (26/10/2026, P1) `com_gabarito=False`, ou registro sem gabarito, pula as três últimas.
    ! Motivo: na Fase 4 o agente diagnostica ao vivo, sem gabarito; as oito conferências sem gabarito continuam as
    mesmas, byte a byte, para o adaptador das corridas gravadas."""
    lido, campos = decl["lido"], decl["campos"]
    por_id = {v["id"]: v for v in verbetes}
    no_contexto = list(registro.get("verbetes_ids") or [])
    causa = lido["causa_raiz"]
    citadas = [f["valor"] for f in decl["fontes"]]
    saida = []
    ausentes = [nome for chave, nome in _CAMPOS if campos[chave] is None]
    saida.append(_v("quatro_linhas_presentes", "resposta", "confere" if not ausentes else "nao_confere", {"ausentes": ausentes}))
    if causa is None:
        saida.append(_v("rotulo_no_conjunto", None, "nao_se_aplica", "a resposta não tem a linha CAUSA_RAIZ"))
    else:
        saida.append(_v("rotulo_no_conjunto", causa, "confere" if avaliar._normalizar(causa) in avaliar._PERMITIDAS else "nao_confere",
                        f"{len(avaliar._PERMITIDAS)} causas permitidas"))
    if not citadas:
        saida.append(_v("fonte_existe_na_biblioteca", None, "nao_se_aplica", "nenhum verbete citado na linha FONTE"))
        saida.append(_v("fonte_estava_no_contexto", None, "nao_se_aplica", "nenhum verbete citado na linha FONTE"))
    for i in citadas:
        saida.append(_v("fonte_existe_na_biblioteca", i, "confere" if i in por_id else "nao_confere"))
    for i in citadas:
        saida.append(_v("fonte_estava_no_contexto", i, "confere" if i in no_contexto else "nao_confere", {"contexto": no_contexto}))
    campo = lido["campo"]
    if not campo or "nenhum" in avaliar._normalizar(campo):
        saida.append(_v("campo_existe_no_caso", campo, "nao_se_aplica", "o modelo não apontou campo"))
    else:
        saida.append(_v("campo_existe_no_caso", campo, "confere" if avaliar._normalizar(campo) in _texto_do_caso(caso) else "nao_confere",
                        "procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso"))
    if causa is None:
        saida.append(_v("rotulo_sustentado_por_verbete_do_contexto", None, "nao_se_aplica"))
    else:
        apoio = [i for i in no_contexto if i in por_id and (por_id[i]["meta"].get("causa_raiz") == causa
                                                            or causa in por_id[i]["meta"].get("causas_relacionadas", []))]
        saida.append(_v("rotulo_sustentado_por_verbete_do_contexto", causa, "confere" if apoio else "nao_confere", {"verbetes": apoio}))
    com_notas = []
    for i in citadas:
        if i in por_id:
            notas = [{"epoca": n["epoca"], "caso_de_origem": n["caso"], "operacao": n["operacao"],
                      "veredito_humano": (vereditos or {}).get(curar._chave(n["caso"], i, n["operacao"], n["texto"]))}
                     for n in bib.notas(por_id[i])]
            com_notas.append({"verbete": i, "escrito_pelo_modelo": por_id[i]["pasta"] == evo.PASTA_APRENDIDOS, "notas": notas})
    saida.append(_v("notas_nos_verbetes_citados", citadas or None, "informativo" if com_notas else "nao_se_aplica",
                    {"verbetes": com_notas, "limite": "A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou."}))
    saida.append(_v("impacto", lido["impacto"], "nao_verificavel", "a frase de impacto não tem contraparte no caso para conferir por código"))
    if not com_gabarito or registro.get("gabarito") is None:
        return saida
    av = avaliar.avaliar_registro(registro, set())
    saida.append(_v("causa_correta", causa, "confere" if av["causa_correta"] else "nao_confere",
                    {"gabarito": registro["gabarito"]["causa_raiz"]}, usa_gabarito=True))
    saida.append(_v("campo_correto", campo, "confere" if av["campo_correto"] else "nao_confere",
                    {"gabarito": registro["gabarito"].get("campo_afetado")}, usa_gabarito=True))
    saida.append(_v("verbete_de_ouro_no_contexto", registro.get("verbete_ouro"), "confere" if av["ouro_no_contexto"] else "nao_confere",
                    {"contexto": no_contexto}, usa_gabarito=True))
    return saida


_FONTE_SO_IDS = re.compile(r"^\s*(\[[a-z0-9_\-]+\]\s*(,|;|\se\s)?\s*)+$")


def conferencias_fase4(decl: dict, textos_por_id: dict[str, str]) -> list[dict]:
    """! Alteração de IA - Revisar: as duas conferências sem gabarito que a Fase 4 acrescenta (especificação, seção 5):
    `fonte_formato_valido` (a linha FONTE só tem identificadores no formato do projeto, `[id]` separados por vírgula,
    ponto e vírgula ou "e", sem texto livre) e `fonte_contem_termo_da_causa` (o texto do verbete citado contém o termo
    da causa respondida). `textos_por_id` é {id do verbete: texto renderizado}; verbete desconhecido não se aplica.
    ! Motivo: em modelos de 7B testados na literatura, 54,5% a 62,4% das frases ficaram sem citação e houve citação
    de documento inexistente ou em formato errado (mapa, linhas 17 e 18); as duas regras são baratas e rodam em
    código. Ficam fora de `verificar` para o adaptador das corridas gravadas continuar byte a byte igual."""
    campo = decl["campos"].get("fonte")
    citadas = [f["valor"] for f in decl["fontes"]]
    causa = decl["lido"]["causa_raiz"]
    saida = []
    if campo is None or not citadas:
        saida.append(_v("fonte_formato_valido", None if campo is None else campo["valor"], "nao_se_aplica", "nenhum verbete citado na linha FONTE"))
    else:
        valido = bool(_FONTE_SO_IDS.match(campo["valor"]))
        saida.append(_v("fonte_formato_valido", campo["valor"], "confere" if valido else "nao_confere",
                        {"ids": citadas, "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"}))
    if causa is None or not citadas:
        saida.append(_v("fonte_contem_termo_da_causa", None, "nao_se_aplica", "sem causa ou sem verbete citado"))
        return saida
    termo = avaliar._normalizar(causa)
    for i in citadas:
        texto = textos_por_id.get(i)
        if texto is None:
            saida.append(_v("fonte_contem_termo_da_causa", i, "nao_se_aplica", "verbete não encontrado na biblioteca"))
        else:
            saida.append(_v("fonte_contem_termo_da_causa", i, "confere" if termo in avaliar._normalizar(texto) else "nao_confere", {"termo": termo}))
    return saida


def vereditos_humanos(c3_oficial: dict, modelo: str) -> dict[tuple, str]:
    """{chave da edição -> Correta | Parcial | Errada} das planilhas de revisão do modelo que escreveu a biblioteca: a
    planilha oficial das três épocas e, para a época 1 do modelo decidido, a de curadoria. Sem planilha, dicionário vazio."""
    slug = executar_fase3._slug(modelo)
    saida: dict[tuple, str] = {}
    oficial = c3_oficial["raiz"] / f"revisao_edicoes__{slug}.md"
    if oficial.exists():
        for epoca in (1, 2, 3):
            for chave, (avaliacao, _) in curar.vereditos_da_planilha(oficial, epoca).items():
                if avaliacao.strip():
                    saida[chave] = avaliacao.strip()
    curadoria = c3_oficial["raiz"] / f"curadoria_L1__{slug}.md"
    if curadoria.exists():
        for linha in curadoria.read_text(encoding="utf-8").splitlines():
            c = curar._celulas(linha) if linha.startswith("|") else []
            if len(c) >= 9 and c[0].isdigit() and c[6].strip():
                saida[curar._chave(c[1], c[2], c[3], c[4])] = c[6].strip()
    return saida


# ------------------------------------------------------------------ errata dos casos de texto corrigido

def gerar_errata(commit: str = COMMIT_ANTES_DA_CORRECAO) -> dict:
    """O texto que os casos de a3b.CASOS_DE_TEXTO_ALTERADO tinham no commit anterior à correção de 28/09/2026, lido do
    git (`git show`, só leitura) e executado num espaço de nomes à parte, sem tocar nos módulos atuais."""
    def do_git(caminho: str) -> str:
        r = subprocess.run(["git", "show", f"{commit}:{caminho}"], cwd=RAIZ_DO_REPOSITORIO, capture_output=True, timeout=60)
        if r.returncode != 0:
            raise SystemExit(f"git show {commit}:{caminho} falhou: {r.stderr.decode('utf-8', 'replace')[:200]}")
        return r.stdout.decode("utf-8")

    nomes: dict = {"__name__": "banco_casos_antigo"}
    exec(compile(do_git(ARQUIVOS_DOS_CASOS[0]), "banco_casos_antigo", "exec"), nomes)
    extra = re.sub(r"(?m)^from banco_casos import .*$", "", do_git(ARQUIVOS_DOS_CASOS[1]))   # os nomes já estão no espaço acima
    exec(compile(extra, "banco_casos_extra_antigo", "exec"), nomes)
    antigos = {c["id"]: c for c in list(nomes["CASOS"]) + list(nomes["CASOS_EXTRA"])}
    atuais = {c["id"]: c for c in list(CASOS) + list(CASOS_EXTRA)}
    alvo = sorted(a3b.CASOS_DE_TEXTO_ALTERADO)
    for i in alvo:
        if antigos[i] == atuais[i]:
            raise SystemExit(f"o caso {i} não mudou entre {commit} e hoje: a errata não faz sentido")
    mudaram = sorted(i for i in atuais if i in antigos and antigos[i]["entrada"] != atuais[i]["entrada"])
    return {"metadados": {"commit": commit, "corrigido_em": a3b.DATA_DA_CORRECAO, "casos": alvo,
                          "casos_com_entrada_diferente_no_commit": mudaram,
                          "origem": "git show do commit anterior à correção; achado 4.36 e decisão 58"},
            "casos": {i: antigos[i] for i in alvo}}


def ler_errata() -> dict[str, dict]:
    arq = pasta_derivados() / "errata_casos.json"
    return json.loads(arq.read_text(encoding="utf-8"))["casos"] if arq.exists() else {}


# ------------------------------------------------------------------ adaptador das corridas gravadas

def _todos_os_casos() -> dict[str, dict]:
    casos = {c["id"]: c for c in list(CASOS) + list(CASOS_EXTRA)}
    try:
        from banco_casos_ineditos import CASOS_INEDITOS
        casos.update({c["id"]: c for c in CASOS_INEDITOS})
    except ImportError:
        pass
    return casos


def _condicoes(c3: dict) -> dict:
    arq = c3["raiz"] / "condicoes_3b.json"
    return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else {}


def _leu_o_texto_antigo(corrida: str, condicoes: dict) -> bool:
    """A corrida é anterior à correção dos casos? A oficial da Fase 3 é; as da 3-B dizem quando foram criadas."""
    if corrida == "fase3":
        return True
    criado = condicoes.get("criado_em")
    return bool(criado) and criado[:10] < a3b.DATA_DA_CORRECAO


def _jsonl(arq: Path) -> list[dict]:
    return [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()] if arq.exists() else []


def _trilha_do_registro(t: Trilha, tid: str, r: dict, caso: dict, verbetes: list[dict], indice: rec.Indice, hash_snapshot: str,
                        proposta: dict | None, tem_logprobs: str | None, vereditos: dict, sha_enviado: str | None = None) -> None:
    k = r.get("k", 3)
    ctx, prompt = executar_fase3.contexto_e_prompt(verbetes, indice, caso, k)
    partes = partes_do_prompt(verbetes, ctx, caso, prompt)
    t.evento("entrada", tid, {"caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"], "particao": r.get("particao"),
                              "campos_da_entrada": sorted(caso["entrada"]), "texto": t.blob(partes[-2]["texto"], "caso")}, "recalculado")
    sinais, itens = candidatos(indice, caso, k)
    t.evento("candidatos", tid, {"consulta": sinais, "k": k, "itens": itens}, "recalculado")
    refs = [{"papel": p["papel"], **({"id": p["id"]} if "id" in p else {}), "sha": t.blob(p["texto"], p["papel"]), "antes": p["antes"]} for p in partes]
    t.evento("prompt", tid, {"etapa": "diagnostico", "partes": refs, "sha": sha(prompt), "chars": len(prompt),
                             **provar(r, hash_snapshot, ctx, prompt, proposta, sha_enviado)}, "recalculado")
    s_inf = t.evento("inferencia", tid, {
        "etapa": "diagnostico", "tentativa": 1, "resposta": t.blob(r["resposta"], "resposta"),
        **{c: r.get(c) for c in ("tokens_entrada", "tokens_saida", "segundos", "carga_ms", "prefill_ms", "geracao_ms", "total_ms",
                                 "teto_tokens", "contexto_estourou")},
        "logprobs": {"arquivo": tem_logprobs, "caso": r["caso"]} if tem_logprobs else None}, "registro")
    decl = localizar_declaracoes(r["resposta"])
    rac = decl["raciocinio"]
    t.evento("declaracao", tid, {"campo": "raciocinio", "valor": rac["valor"], "ini": rac["ini"], "fim": rac["fim"], "vazio": not rac["valor"]},
             "registro", pai=s_inf)
    for chave, _ in _CAMPOS:
        item = decl["campos"][chave]
        lido = decl["lido"]["fonte_ids"] if chave == "fonte" else decl["lido"][chave]
        dados = {"campo": chave, "ausente": True, "valor": None, "lido": lido} if item is None else {"campo": chave, "lido": lido, **item}
        t.evento("declaracao", tid, dados, "registro", pai=s_inf)
    for f in decl["fontes"]:
        t.evento("declaracao", tid, {"campo": "fonte_citada", **f}, "registro", pai=s_inf)
    for v in verificar(r, caso, verbetes, decl, vereditos):
        t.evento("verificacao", tid, v, "recalculado", pai=s_inf)
    if proposta is not None:
        _etapa_de_proposta(t, tid, r, prompt, proposta, vereditos)


def _etapa_de_proposta(t: Trilha, tid: str, r: dict, prompt_diag: str, p: dict, vereditos: dict) -> None:
    """Nos casos de aprendizado da Fase 3, a segunda chamada: o modelo recebe a correção do caso e propõe edições na
    biblioteca; o validador em código aceita ou rejeita cada uma, com o código do motivo, e as aceitas são aplicadas."""
    prefixo = prompt_diag + "\n\n" + r["resposta"] + "\n\n"
    texto = str(p.get("prompt", ""))
    continua = texto.startswith(prefixo)
    cauda = texto[len(prefixo):] if continua else texto
    t.evento("prompt", tid, {"etapa": "proposta", "continua_o_diagnostico": continua, "sha": sha(texto), "chars": len(texto),
                             "partes": [{"papel": "correcao_e_instrucoes" if continua else "prompt_de_proposta",
                                         "sha": t.blob(cauda, "correcao_e_instrucoes"), "antes": ""}]}, "registro")
    s_inf = t.evento("inferencia", tid, {
        "etapa": "proposta", "tentativa": 1, "resposta": t.blob(str(p.get("resposta", "")), "resposta_da_proposta"),
        **{c: p.get(c) for c in ("tokens_entrada", "tokens_saida", "segundos", "carga_ms", "prefill_ms", "geracao_ms", "total_ms",
                                 "teto_tokens", "contexto_estourou", "resposta_truncada", "nenhuma")}}, "registro")
    decisoes = {d.get("numero"): d for d in p.get("decisoes") or []}
    resposta = str(p.get("resposta", ""))
    for prop in p.get("propostas_parseadas") or []:
        c = prop.get("campos") or {}
        txt = c.get("TEXTO") or ""
        pos = resposta.find(txt) if txt else -1
        s_dec = t.evento("declaracao", tid, {"campo": "proposta", "numero": prop.get("numero"), "operacao": c.get("OPERACAO"), "verbete": c.get("VERBETE"),
                                             "valor": txt, "ini": pos if pos >= 0 else None, "fim": pos + len(txt) if pos >= 0 else None,
                                             "motivo_declarado": c.get("MOTIVO"), "trecho_alvo": c.get("TRECHO")}, "registro", pai=s_inf)
        d = decisoes.get(prop.get("numero"))
        if d is None:
            continue
        t.evento("verificacao", tid, _v("validador_da_biblioteca", f"proposta {prop.get('numero')}", "aceita" if d.get("aceita") else "rejeitada",
                                        {"codigo": d.get("motivo"), "detalhe": d.get("detalhe")}), "registro", pai=s_dec)
        e = d.get("edicao") or {}
        if d.get("aceita") and e:
            s_acao = t.evento("acao", tid, {"acao": "edicao_aplicada", "operacao": e.get("operacao"), "verbete": e.get("verbete"),
                                            "arquivo": e.get("arquivo"), "epoca": e.get("epoca"),
                                            "hash_da_biblioteca_depois": p.get("hash_biblioteca_apos")}, "registro", pai=s_dec)
            humano = vereditos.get(curar._chave(str(e.get("caso", "")), str(e.get("verbete", "")), str(e.get("operacao", "")), str(e.get("texto", ""))))
            if humano:
                t.evento("verificacao", tid, _v("revisao_humana_da_edicao", f"proposta {prop.get('numero')}", humano), "humano", pai=s_acao)


def adaptar_corrida(corrida: str, modelo: str, versao: int, errata: dict | None = None) -> Trilha:
    """Remonta a trilha de uma corrida gravada (pasta em caminhos.fase3(corrida)) para um modelo e uma versão da
    biblioteca: um evento `corrida` e, por diagnóstico gravado, a sequência entrada, candidatos, prompt, inferência,
    declarações, verificações e, quando há proposta gravada para o caso, a etapa de proposta. `errata` é o texto antigo
    dos casos corrigidos em 28/09 (None lê o arquivo gerado por --errata; {} desliga)."""
    c3 = caminhos.fase3(corrida)
    slug = executar_fase3._slug(modelo)
    pasta = c3["raiz"] / slug
    registros = _jsonl(pasta / f"diagnosticos__L{versao}.jsonl")
    if not registros:
        raise SystemExit(f"sem diagnósticos em {pasta / f'diagnosticos__L{versao}.jsonl'}")
    snapshot = c3["bibliotecas"] / slug / f"epoca-{versao}"
    verbetes = bib.carregar(snapshot)
    indice = rec.Indice(verbetes)
    hash_snapshot = evo.hash_biblioteca(snapshot)
    condicoes = _condicoes(c3)
    antigo = _leu_o_texto_antigo(corrida, condicoes)
    casos = _todos_os_casos()
    usadas = {}
    if antigo:
        usadas = ler_errata() if errata is None else errata
        casos.update(usadas)
    propostas = {p["caso"]: p for p in _jsonl(pasta / f"propostas__E{versao + 1}.jsonl")}
    lateral = pasta / f"logprobs__L{versao}.jsonl"
    enviados = {l["caso"]: l.get("prompt_sha256") for l in _jsonl(lateral)}     # caso -> hash do prompt que foi ao Ollama
    vereditos = vereditos_humanos(caminhos.fase3("fase3"), condicoes.get("doador") or modelo)
    condicao = {r.get("condicao") for r in registros}
    if condicao != {executar_fase3.CONDICAO}:
        raise SystemExit(f"registros com condição {sorted(condicao, key=str)}: o adaptador remonta só a condição {executar_fase3.CONDICAO}")

    t = Trilha()
    r0 = registros[0]
    t.evento("corrida", f"{corrida}/{slug}/L{versao}", {
        "corrida": corrida, "modelo": modelo, "digest": r0.get("digest"), "versoes_do_ollama": sorted({str(r.get("versao_ollama")) for r in registros}),
        "biblioteca_epoca": versao, "biblioteca_versao": hash_snapshot, "dono_da_biblioteca": condicoes.get("doador") or modelo,
        "k": r0.get("k"), "condicao": r0.get("condicao"), "estrategia": r0.get("estrategia"),
        "opcoes": {"num_gpu": 0, "num_ctx": oll.NUM_CTX, "temperature": oll.TEMPERATURA, "num_predict": r0.get("teto_tokens")},
        "registros": len(registros), "texto_dos_casos": "anterior à correção de 28/09/2026" if antigo else "atual",
        "casos_lidos_da_errata": sorted(i for i in usadas if any(r["caso"] == i for r in registros))}, "registro")
    for r in registros:
        tid = f"{corrida}/{slug}/{r['caso']}@L{versao}"
        _trilha_do_registro(t, tid, r, casos[r["caso"]], verbetes, indice, hash_snapshot, propostas.get(r["caso"]),
                            lateral.name if r["caso"] in enviados else None, vereditos, enviados.get(r["caso"]))
    return t


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--errata", action="store_true", help="grava pre_fase4/errata_casos.json com o texto antigo dos casos corrigidos em 28/09")
    ap.add_argument("--corrida", help="pasta da corrida em RESULTADOS_DIR (fase3, fase3b_ineditos, …)")
    ap.add_argument("--modelo", default="qwen2.5:7b")
    ap.add_argument("--versao", type=int, default=1)
    ap.add_argument("--saida", help="arquivo .jsonl de destino (padrão: pre_fase4/trilhas/<corrida>__<modelo>__L<n>.jsonl)")
    args = ap.parse_args()
    print(caminhos.descricao())
    if args.errata:
        dado = gerar_errata()
        destino = pasta_derivados() / "errata_casos.json"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"gravado: {destino} ({', '.join(dado['metadados']['casos'])}; commit {dado['metadados']['commit']})")
        return 0
    if not args.corrida:
        ap.error("informe --corrida ou --errata")
    t = adaptar_corrida(args.corrida, args.modelo, args.versao)
    destino = Path(args.saida) if args.saida else (pasta_derivados() / "trilhas" / f"{args.corrida}__{executar_fase3._slug(args.modelo)}__L{args.versao}.jsonl")
    t.gravar(destino)
    niveis = [e["dados"]["nivel"] for e in t.eventos if e["tipo"] == "prompt" and e["dados"].get("etapa") == "diagnostico"]
    print(f"gravado: {destino} ({len(t.eventos)} eventos, {len(niveis)} diagnósticos; prova do prompt: "
          + ", ".join(f"{n} {niveis.count(n)}" for n in ("prompt_inteiro", "contexto", "nao_comprovado") if n in niveis) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
