#!/usr/bin/env python3
# ! Alteração de IA - Revisar: ponto único que decide ONDE os experimentos gravam e leem —
# resultados brutos, avaliação, resumo de métricas, gráficos e relatório — a partir da
# variável de ambiente RESULTADOS_DIR.
# ! Motivo: a Fase 2-B roda na máquina-alvo (notebook corporativo i5-1235U, 16 GB, sem GPU
# dedicada), não no Ryzen em que a Fase 2-A foi medida. Os dois conjuntos de resultados
# precisam coexistir no repositório sem um sobrescrever o outro: a linha de base A0 é refeita
# na máquina-alvo (as comparações são pareadas caso a caso e não podem misturar máquinas —
# CPU diferente muda o tempo e pode mudar a resposta), e os números do Ryzen ficam como
# referência de desenvolvimento. Sem a variável, tudo continua onde a Fase 2-A deixou
# (resultados/, avaliacao.json, graficos/ na raiz de experimentos/); com ela, tudo vai para
# dentro da pasta indicada (ex.: resultados_alvo/), inclusive o log e o maquina.json.
import os
from pathlib import Path

AQUI = Path(__file__).resolve().parent
_ENV = os.environ.get("RESULTADOS_DIR", "").strip()

if _ENV:
    RESULTADOS = Path(_ENV) if Path(_ENV).is_absolute() else AQUI / _ENV
    RAIZ_SAIDA = RESULTADOS
else:
    RESULTADOS = AQUI / "resultados"
    RAIZ_SAIDA = AQUI

AVALIACAO = RAIZ_SAIDA / "avaliacao.json"
RESUMO = RAIZ_SAIDA / "resumo_metricas.json"
GRAFICOS = RAIZ_SAIDA / "graficos"
RELATORIO = RAIZ_SAIDA / "relatorio.html"
MAQUINA = RESULTADOS / "maquina.json"


# ! Alteração de IA - Revisar: caminhos de saída da Fase 3, todos dentro de uma subpasta
# própria (resultados/fase3/ ou <RESULTADOS_DIR>/fase3/), menos os gráficos da corrida
# oficial.
# ! Motivo: avaliar.carregar() varre os JSONL com glob("*.jsonl") NÃO recursivo e
# gerar_relatorio.py lê avaliacao.json/resumo_metricas.json da raiz — se os arquivos da
# Fase 3 caíssem lá junto, os resultados da Fase 2-B (que estão fechados e não podem mudar)
# passariam a ser reprocessados junto com os novos. Os gráficos vão para a pasta comum
# porque a numeração das figuras do TCC é uma sequência só, que continua do 12 em diante;
# a exceção é o piloto, descartável, que leva os gráficos dele para dentro da própria pasta.
def fase3(nome: str = "fase3") -> dict[str, Path]:
    raiz = RESULTADOS / nome
    return {"raiz": raiz, "bibliotecas": raiz / "bibliotecas", "particao": raiz / "particao.json",
            "maquina": raiz / "maquina.json", "log": raiz / "fase3.log",
            "avaliacao": raiz / "avaliacao_fase3.json", "resumo": raiz / "resumo_fase3.json",
            "comparacao": raiz / "comparacao_fases.json",
            "comparacao_md": raiz / "comparacao_fases.md",
            "relatorio": raiz / "relatorio_fase3.html",
            "graficos": GRAFICOS if nome == "fase3" else raiz / "graficos"}


def descricao() -> str:
    origem = f"RESULTADOS_DIR={_ENV}" if _ENV else "RESULTADOS_DIR não definida (padrão)"
    return f"resultados em {RESULTADOS} — {origem}"
