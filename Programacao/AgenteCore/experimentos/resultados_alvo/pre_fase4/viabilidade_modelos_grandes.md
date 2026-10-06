<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por viabilidade_modelos_grandes.py a partir de disco.json, dos registros oficiais da Fase 3 e das constantes citadas do repositório (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Viabilidade dos modelos grandes do colibri nesta máquina, gerada em 2026-10-01

Repositório: https://github.com/JustVugg/colibri (acesso em 2026-10-01). As constantes do repositório (requisitos por modelo, GB lidos por token e medidas de terceiros) já foram conferidas (ressalva: o verificador não confirmou o tamanho em disco do GLM-5.3 (419 GB)) pela rodada 5 da pesquisa. Um token frio do GLM-5.2 lê cerca de 11,4 GB do disco (`docs/benchmarks.md`). Os tempos de disco são piso: ainda falta a conta na CPU e a leitura do prompt, que o repositório não mede em máquina pequena.

Como ler a última coluna da tabela dos modelos: roda (sim) o que cabe no disco livre e pede menos RAM do que a instalada; fica no limite o que cabe no disco livre e pede exatamente a RAM instalada, que é o mínimo declarado pelo repositório (não há medida publicada de nenhum deles numa máquina dessa classe); o resto não roda.


<!-- tabela:tb_viab_maquina -->
| Item | Valor | Origem |
|---|---|---|
| Processador | 12th Gen Intel(R) Core(TM) i5-1235U | `disco.json` (`maquina.cpu`) |
| RAM instalada | 16,0 GB | `disco.json` (`maquina.ram_instalada_gb`) |
| RAM que o sistema enxerga | 15,69 GB | `disco.json` (`maquina.ram_gb`) |
| RAM livre no início de uma corrida | 7,2 GB | `resultados_alvo/maquina.json` (`ram_livre_no_inicio_gb`, Fase 2-B) |
| Disco | NVMe SM2P41C3 NVMe ADATA 512GB (NVMe) | `disco.json` (`maquina.disco`) |
| Disco: tamanho e espaço livre | 474,0 GB, 218,1 GB livres | `disco.json` (`maquina.disco`) |
| Leitura do disco por fora do cache (mediana) | 3,77 GB/s | `disco.json` (`direto.gb_por_s_mediana`) |
| Leitura passando pelo cache (mediana) | 2,31 GB/s | `disco.json` (`pelo_cache.gb_por_s_mediana`) |
| Resposta mediana do `qwen2.5:7b` | 61,0 tokens em 66,7 s (360 diagnósticos) | registros oficiais da Fase 3 |
| Prompt mediano | 1285,5 tokens | registros oficiais da Fase 3 |
<!-- /tabela:tb_viab_maquina -->

<!-- tabela:tb_viab_familias -->
| Modelo | Parâmetros (bilhões) | Ativos por token (bilhões) | Disco pedido (GB) | RAM pedida (texto do repositório) | Cabe no disco livre | Caberia no disco vazio | RAM pedida contra a instalada | Roda nesta máquina |
|---|---|---|---|---|---|---|---|---|
| OLMoE | 7 | 1 | 7,0 | 8 GB | sim | sim | sim | sim |
| Qwen3.6-35B-A3B | 35 | 3 | 20,0 | 24 GB (needs full RAM residency) | sim | sim | **não** | **não** |
| DeepSeek V4 Flash | 284 | 13 | 167,0 | 16 GB min, 32 GB comfortable | sim | sim | no mínimo declarado | no limite |
| Qwen3.8-Flash-Next | 180 | 6 | 185,5 | 16 GB min, 24 GB comfortable at the default context | sim | sim | no mínimo declarado | no limite |
| GLM-5.3-Flash | 320 | 18 | 195,0 | 25 GB (12 GB weights at int4 + expert cache) | sim | sim | **não** | **não** |
| GLM-5.2 | 744 | 40 | 372,0 | 16 GB min, 24 GB comfortable | **não** | sim | no mínimo declarado | **não** |
| GLM-5.3 | n/a | n/a | 419,0 | 16 GB min, 24 GB comfortable | **não** | sim | no mínimo declarado | **não** |
| Inkling | 975 | 41 | 469,0 | 25 GB with the int4 dense container, ~120 GB without | **não** | sim | **não** | **não** |
| Kimi K3 | 2800 | 104 | 1600,0 | 32 GB+ | **não** | **não** | **não** | **não** |
<!-- /tabela:tb_viab_familias -->

<!-- tabela:tb_viab_disco -->
| Disco | Leitura (GB/s) | Medido ou premissa | Segundos de disco por token frio | Teto de tokens por segundo | Minutos só de leitura para a resposta mediana |
|---|---|---|---|---|---|
| NVMe desta máquina, leitura por fora do cache (medido) | 3,77 | medido | 3,0 | 0,330 | 3,1 |
| SSD SATA (premissa: 0,55 GB/s, teto prático da interface) | 0,55 | premissa | 20,7 | 0,048 | 21,1 |
| disco rígido de 7.200 rpm (premissa: 0,15 GB/s em leitura sequencial) | 0,15 | premissa | 76,0 | 0,013 | 77,3 |
<!-- /tabela:tb_viab_disco -->

<!-- tabela:tb_viab_terceiros -->
| Máquina (medida publicada no repositório) | Modelo | Tokens por segundo | Condição | Minutos só de geração para a nossa resposta mediana | Vezes o tempo total de um diagnóstico de hoje | Issue |
|---|---|---|---|---|---|---|
| Intel Core Ultra 7 270K Plus, 24 GB, WSL2, NVMe | GLM-5.2 | 0,07 | padrão; cache de especialistas com acerto de 3 a 4% | 14,5 | 13,1 | #2 |
| Intel Core Ultra 7 270K Plus, 24 GB, WSL2, NVMe | GLM-5.2 | 0,11 | com --topp 0.7, que o repositório marca como opção com perda | 9,2 | 8,3 | #2 |
| Intel i5-12600K, 32 GB, Windows 11 nativo, só CPU | GLM-5.2 | 0,08 | frio, cache limitado pela RAM a cerca de 2 especialistas por camada | 12,7 | 11,4 | #113 |
| Intel Core Ultra 9 185H, 32 GB, Windows 11 nativo | GLM-5.2 | 0,03 | frio, só CPU; a mesma máquina chega a 0,5 com o cache quente | 33,9 | 30,5 | #128 |
| Apple M3 básico, 16 GB, só CPU | OLMoE | 3,69 | frio; 4,18 com o cache quente | 0,3 | 0,2 | #949 |
<!-- /tabela:tb_viab_terceiros -->
