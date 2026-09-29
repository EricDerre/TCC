<!-- ! Alteração de IA - Revisar: documento DERIVADO de experimento_recuperador.json, gerado por experimento_recuperador.py (--check regera e compara); não editar à mão.
     ! Motivo: regra do projeto — nenhum número digitado à mão em Markdown de resultados. -->
# Experimento do recuperador — 2026-09-29

Embedding: `embeddinggemma:300m` (204 chamadas ao /api/embed); fusão de posições com k = 60. Bibliotecas: L0 (original) (hash 3196327e7fd5); L1 qwen2.5:7b (hash 3394d203cab9); L3 qwen2.5:7b (hash 71258b553152). Casos: 90 oficiais = 90; 36 inéditos = 36.

## 90 oficiais

| Biblioteca | Método | hit@1 | hit@3 | hit@5 | MRR |
|---|---|---|---|---|---|
| L0 (original) | bm25 (Fase 3) | 38,9% | 80,0% | 91,1% | 0,596 |
| L0 (original) | denso (termos do BM25) | 22,2% | 35,6% | 61,1% | 0,366 |
| L0 (original) | denso (texto do caso) | 0,0% | 11,1% | 20,0% | 0,117 |
| L0 (original) | híbrido RRF (bm25 + denso termos) | 25,6% | 60,0% | 73,3% | 0,457 |
| L0 (original) | híbrido RRF (bm25 + denso texto) | 25,6% | 37,8% | 47,8% | 0,391 |
| L1 qwen2.5:7b | bm25 (Fase 3) | 36,7% | 77,8% | 92,2% | 0,580 |
| L1 qwen2.5:7b | denso (termos do BM25) | 20,0% | 34,4% | 57,8% | 0,351 |
| L1 qwen2.5:7b | denso (texto do caso) | 0,0% | 6,7% | 16,7% | 0,091 |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 25,6% | 61,1% | 74,4% | 0,464 |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 24,4% | 35,6% | 43,3% | 0,370 |
| L3 qwen2.5:7b | bm25 (Fase 3) | 36,7% | 78,9% | 88,9% | 0,579 |
| L3 qwen2.5:7b | denso (termos do BM25) | 20,0% | 38,9% | 61,1% | 0,367 |
| L3 qwen2.5:7b | denso (texto do caso) | 0,0% | 0,0% | 11,1% | 0,077 |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 26,7% | 67,8% | 80,0% | 0,490 |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 26,7% | 34,4% | 45,6% | 0,378 |

### hit@3 por classe

| Biblioteca | Método | 1 lexica | 2 sintatica | 3 semantica | 4 traducao | 5 runtime | 6 efeito |
|---|---|---|---|---|---|---|---|
| L0 (original) | bm25 (Fase 3) | 93,3% | 86,7% | 80,0% | 46,7% | 80,0% | 93,3% |
| L0 (original) | denso (termos do BM25) | 33,3% | 0,0% | 26,7% | 26,7% | 66,7% | 60,0% |
| L0 (original) | denso (texto do caso) | 0,0% | 60,0% | 0,0% | 0,0% | 0,0% | 6,7% |
| L0 (original) | híbrido RRF (bm25 + denso termos) | 60,0% | 26,7% | 60,0% | 46,7% | 86,7% | 80,0% |
| L0 (original) | híbrido RRF (bm25 + denso texto) | 46,7% | 80,0% | 0,0% | 60,0% | 26,7% | 13,3% |
| L1 qwen2.5:7b | bm25 (Fase 3) | 86,7% | 80,0% | 80,0% | 40,0% | 86,7% | 93,3% |
| L1 qwen2.5:7b | denso (termos do BM25) | 33,3% | 0,0% | 26,7% | 20,0% | 80,0% | 46,7% |
| L1 qwen2.5:7b | denso (texto do caso) | 0,0% | 33,3% | 0,0% | 0,0% | 0,0% | 6,7% |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 60,0% | 20,0% | 60,0% | 53,3% | 93,3% | 80,0% |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 46,7% | 73,3% | 0,0% | 60,0% | 26,7% | 6,7% |
| L3 qwen2.5:7b | bm25 (Fase 3) | 86,7% | 86,7% | 80,0% | 46,7% | 86,7% | 86,7% |
| L3 qwen2.5:7b | denso (termos do BM25) | 33,3% | 0,0% | 33,3% | 26,7% | 80,0% | 60,0% |
| L3 qwen2.5:7b | denso (texto do caso) | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 66,7% | 40,0% | 66,7% | 53,3% | 93,3% | 86,7% |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 46,7% | 73,3% | 0,0% | 60,0% | 20,0% | 6,7% |

## 36 inéditos

| Biblioteca | Método | hit@1 | hit@3 | hit@5 | MRR |
|---|---|---|---|---|---|
| L0 (original) | bm25 (Fase 3) | 41,7% | 69,4% | 69,4% | 0,547 |
| L0 (original) | denso (termos do BM25) | 19,4% | 44,4% | 58,3% | 0,370 |
| L0 (original) | denso (texto do caso) | 0,0% | 8,3% | 19,4% | 0,109 |
| L0 (original) | híbrido RRF (bm25 + denso termos) | 22,2% | 55,6% | 72,2% | 0,429 |
| L0 (original) | híbrido RRF (bm25 + denso texto) | 16,7% | 25,0% | 41,7% | 0,304 |
| L1 qwen2.5:7b | bm25 (Fase 3) | 38,9% | 66,7% | 66,7% | 0,532 |
| L1 qwen2.5:7b | denso (termos do BM25) | 22,2% | 41,7% | 55,6% | 0,386 |
| L1 qwen2.5:7b | denso (texto do caso) | 0,0% | 5,6% | 13,9% | 0,086 |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 30,6% | 50,0% | 69,4% | 0,469 |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 11,1% | 22,2% | 38,9% | 0,259 |
| L3 qwen2.5:7b | bm25 (Fase 3) | 38,9% | 63,9% | 66,7% | 0,530 |
| L3 qwen2.5:7b | denso (termos do BM25) | 19,4% | 47,2% | 66,7% | 0,391 |
| L3 qwen2.5:7b | denso (texto do caso) | 0,0% | 0,0% | 8,3% | 0,074 |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 25,0% | 61,1% | 66,7% | 0,446 |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 11,1% | 22,2% | 36,1% | 0,260 |

### hit@3 por classe

| Biblioteca | Método | 1 lexica | 2 sintatica | 3 semantica | 4 traducao | 5 runtime | 6 efeito |
|---|---|---|---|---|---|---|---|
| L0 (original) | bm25 (Fase 3) | 66,7% | 100,0% | 66,7% | 33,3% | 83,3% | 66,7% |
| L0 (original) | denso (termos do BM25) | 33,3% | 0,0% | 33,3% | 33,3% | 100,0% | 66,7% |
| L0 (original) | denso (texto do caso) | 0,0% | 50,0% | 0,0% | 0,0% | 0,0% | 0,0% |
| L0 (original) | híbrido RRF (bm25 + denso termos) | 66,7% | 33,3% | 50,0% | 33,3% | 83,3% | 66,7% |
| L0 (original) | híbrido RRF (bm25 + denso texto) | 16,7% | 66,7% | 0,0% | 50,0% | 16,7% | 0,0% |
| L1 qwen2.5:7b | bm25 (Fase 3) | 66,7% | 100,0% | 66,7% | 33,3% | 83,3% | 50,0% |
| L1 qwen2.5:7b | denso (termos do BM25) | 50,0% | 0,0% | 16,7% | 16,7% | 100,0% | 66,7% |
| L1 qwen2.5:7b | denso (texto do caso) | 0,0% | 33,3% | 0,0% | 0,0% | 0,0% | 0,0% |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 50,0% | 33,3% | 33,3% | 33,3% | 83,3% | 66,7% |
| L1 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 16,7% | 66,7% | 0,0% | 33,3% | 16,7% | 0,0% |
| L3 qwen2.5:7b | bm25 (Fase 3) | 66,7% | 83,3% | 66,7% | 33,3% | 83,3% | 50,0% |
| L3 qwen2.5:7b | denso (termos do BM25) | 50,0% | 0,0% | 33,3% | 33,3% | 100,0% | 66,7% |
| L3 qwen2.5:7b | denso (texto do caso) | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso termos) | 66,7% | 66,7% | 50,0% | 33,3% | 83,3% | 66,7% |
| L3 qwen2.5:7b | híbrido RRF (bm25 + denso texto) | 16,7% | 66,7% | 0,0% | 33,3% | 16,7% | 0,0% |
