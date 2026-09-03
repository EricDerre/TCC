#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cliente compartilhado do Ollama, extraído de
# benchmark_modelos.py para servir também a bateria ampliada da Fase 2-A.
# ! Motivo: as funções de chamada, medição e leitura de memória já existiam e estavam
# corretas; duplicá-las na bateria nova faria as duas medições divergirem com o tempo.
# Acrescenta o que a bateria exige e o benchmark antigo não tinha: descarregar o modelo
# entre rodadas (exigência de rodar um modelo por vez, sem disputa de memória), conferir
# quantos modelos estão residentes, e fixar num_ctx.
#
# Três parâmetros vêm de achados da pesquisa e NÃO devem ser alterados sem refazer as
# medições: num_gpu=0 (a máquina de teste tem GPU, mas a tese afirma operar sob restrição
# de hardware local — medir com GPU inflaria o resultado); num_ctx=8192 (modelos de 128K
# de contexto alocam cache KV proporcional e estouram a RAM antes do peso do modelo);
# e think=False nos modelos com raciocínio embutido (multiplicaria a latência por até 10x).
import json
import sys
import time
import urllib.error
import urllib.request

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, igual ao _env_common.py.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa símbolos usados
# nos relatórios (≈, Δ, →) — o script inteiro abortava com UnicodeEncodeError ao imprimir.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


OLLAMA = "http://localhost:11434"
NUM_CTX = 8192
TEMPERATURA = 0.1

# Modelos com modo "thinking" embutido, que precisa ser desligado explicitamente.
# Enviar think=False para modelo que não suporta faz o Ollama recusar a requisição,
# por isso a lista é explícita em vez de mandar sempre.
MODELOS_COM_THINKING = ("qwen3", "granite4.2", "granite4")


def _post(caminho: str, corpo: dict, timeout: int = 900) -> dict:
    req = urllib.request.Request(
        f"{OLLAMA}{caminho}",
        data=json.dumps(corpo).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _get(caminho: str, timeout: int = 30) -> dict:
    with urllib.request.urlopen(f"{OLLAMA}{caminho}", timeout=timeout) as resp:
        return json.loads(resp.read())


def tem_thinking(modelo: str) -> bool:
    return modelo.split(":")[0] in MODELOS_COM_THINKING


def gerar(modelo: str, prompt: str, max_tokens: int = 400) -> dict:
    """Uma inferência, sempre em CPU e com contexto fixo."""
    corpo = {
        "model": modelo,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_gpu": 0,
            "num_ctx": NUM_CTX,
            "temperature": TEMPERATURA,
            "num_predict": max_tokens,
        },
    }
    if tem_thinking(modelo):
        corpo["think"] = False

    inicio = time.perf_counter()
    r = _post("/api/generate", corpo)
    segundos = time.perf_counter() - inicio
    # ! Alteração de IA - Revisar: passa a gravar a decomposição de tempo que o Ollama já
    # devolve (carga do modelo, prefill do prompt e geração, em nanossegundos), além do
    # tempo de parede.
    # ! Motivo: na Fase 2-B a biblioteca de documentação entra no prompt e infla o PREFILL,
    # não a geração. Só com o tempo total não dá para dizer quanto custou a documentação,
    # nem se o cache de prefixo do Ollama está reaproveitando o KV entre chamadas — e os
    # quatro campos já vinham em toda resposta, estavam sendo descartados.
    return {
        "segundos": round(segundos, 2),
        "tokens_entrada": r.get("prompt_eval_count", 0),
        "tokens_saida": r.get("eval_count", 0),
        "carga_ms": round(r.get("load_duration", 0) / 1e6),
        "prefill_ms": round(r.get("prompt_eval_duration", 0) / 1e6),
        "geracao_ms": round(r.get("eval_duration", 0) / 1e6),
        "total_ms": round(r.get("total_duration", 0) / 1e6),
        "resposta": r.get("response", "").strip(),
    }


def embed(modelo: str, texto: str) -> list[float]:
    """! Alteração de IA - Revisar: gera um vetor de embedding pelo endpoint /api/embed
    do Ollama, sempre em CPU.
    ! Motivo: a ablação de recuperação da Fase 2-B compara BM25 com embedding denso
    (embeddinggemma:300m, o melhor porte pequeno em pt-BR na MTEB-BR). Pedir ao próprio
    Ollama evita instalar sentence-transformers/torch — mais de 2 GB de dependência que
    quebraria a instalação leve ("hit and run") do repositório."""
    r = _post("/api/embed", {"model": modelo, "input": texto, "options": {"num_gpu": 0}})
    vetores = r.get("embeddings") or []
    return vetores[0] if vetores else []


def residentes() -> list[dict]:
    """Modelos carregados na memória agora, com tamanho e quanto foi para a VRAM."""
    return [
        {
            "nome": m.get("name", ""),
            "memoria_mb": round(m.get("size", 0) / 1024 / 1024),
            "vram_mb": round(m.get("size_vram", 0) / 1024 / 1024),
        }
        for m in _get("/api/ps").get("models", [])
    ]


def somente_cpu() -> bool:
    """True se nenhum modelo residente está usando VRAM."""
    return all(m["vram_mb"] == 0 for m in residentes())


def um_modelo_por_vez() -> tuple[bool, list[str]]:
    """Confere a exigência de não ter dois modelos disputando memória."""
    nomes = [m["nome"] for m in residentes()]
    return len(nomes) <= 1, nomes


def descarregar(modelo: str) -> None:
    """Libera a memória do modelo (keep_alive=0), para o próximo começar limpo."""
    try:
        _post("/api/generate", {"model": modelo, "prompt": "", "keep_alive": 0}, timeout=120)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        pass  # descarregar é melhor-esforço; não vale abortar a bateria por isso


def instalados() -> dict[str, str]:
    """Mapa nome -> digest. O digest entra no relatório porque tag do Ollama é
    ponteiro mutável: sem ele, o experimento não é reproduzível depois."""
    return {
        m["name"]: m.get("digest", "")[:12]
        for m in _get("/api/tags").get("models", [])
    }
