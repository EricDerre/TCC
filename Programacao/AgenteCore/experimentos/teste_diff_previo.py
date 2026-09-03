# ! Alteração de IA - Revisar: experimento A/B — o mesmo cenário de quebra de contrato,
# NOTA (Fase 2-B): script CONGELADO como registro da primeira leva (RESULTADO_FASE2.md);
# o cliente do Ollama em uso pelos experimentos atuais esta em cliente_ollama.py.
# uma vez com o JSON cru e outra com a divergência já calculada em código.
# ! Motivo: no benchmark, os três portes erraram a causa raiz do campo renomeado
# (preco -> preco_v2), culpando a conversão numérica. A hipótese é que comparar chaves
# entre duas estruturas é tarefa de código, não de modelo de linguagem; se o diff for
# pré-calculado, o modelo só precisa explicar — que é onde ele é bom. O resultado decide
# se o agente envia o JSON cru ou o diff ao LLM.
import json
import time
import urllib.request

from prompts_benchmark import CENARIO_DIAGNOSTICO, INSTRUCAO_DIAGNOSTICO

MODELOS = ["qwen2.5-coder:1.5b", "qwen2.5-coder:3b", "qwen2.5-coder:7b"]

# O diff é o que o interceptador conseguiria calcular sozinho, comparando as chaves da
# resposta com as do contrato esperado — sem nenhuma inferência.
CENARIO_COM_DIFF = """DIVERGÊNCIA DE CONTRATO DETECTADA (comparação automática de chaves)
- Campo ausente na resposta: "preco" (esperado: número)
- Campo inesperado na resposta: "preco_v2" (número)
- Demais campos conferem: id, nome, resumo, tipo, imagem, destaque

REQUISIÇÃO
GET http://localhost:8000/api/produtos
Origem: http://localhost:8080/produtos_api.php

SINTOMA OBSERVADO NA INTERFACE
Os cartões de produto exibem "R$ NaN" no lugar do valor.

CONHECIMENTO PRÉVIO DO SISTEMA
- A função formatarPreco() em produtos_api.php converte o campo preco com Number() antes de exibir."""


def gerar(modelo: str, prompt: str) -> tuple[float, str]:
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps({
            "model": modelo, "prompt": prompt, "stream": False,
            "options": {"num_gpu": 0, "temperature": 0.1, "num_predict": 300},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    inicio = time.perf_counter()
    with urllib.request.urlopen(req, timeout=600) as resp:
        r = json.loads(resp.read())
    return round(time.perf_counter() - inicio, 2), r.get("response", "").strip()


for modelo in MODELOS:
    for rotulo, cenario in (("JSON CRU", CENARIO_DIAGNOSTICO), ("COM DIFF", CENARIO_COM_DIFF)):
        seg, resposta = gerar(modelo, f"{INSTRUCAO_DIAGNOSTICO}\n\n{cenario}")
        print("=" * 70)
        print(f"{modelo}  |  {rotulo}  |  {seg}s")
        print("=" * 70)
        print(resposta)
        print()
