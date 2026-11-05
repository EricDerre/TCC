<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-3@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `imagem` · selo de probabilidade: **baixo** (p = 0,57)

**IMPACTO (declarado):** `Os cartões aparecem sem foto nenhuma, pois o campo "imagem" está ausente na resposta da API.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo imagem porque o sinal imagem: esperado texto|nulo, recebido None está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,26. A FONTE cita 2 verbete(s), todos presentes no contexto. A remoção do verbete contrato-produto não mudou a resposta: sem efeito medido do contexto. A troca do verbete contrato-produto por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,57); trate como hipótese e confira o campo imagem antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1478): regras diff_contra_contrato; antes {"chars": 119}, depois {"chars": 119}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | texto\|nulo |  |

Trecho podado (hash `55555e369bef5da7`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "destaque": true}]
```

## 3. Contraste com a segunda causa

campo_ausente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,57 contra 0,26; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,57 | sim |
| colecao_no_lugar_de_objeto | 0,26 |  |
| resposta_truncada | 0,09 |  |
| tipo_divergente | 0,04 |  |
| corpo_nao_e_json | 0,03 |  |
| corpo_vazio | 0,03 |  |
| formato_de_data_divergente | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[contrato-produto] [campo_ausente]` | confere | {"ids": ["contrato-produto", "campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-produto` | campo_ausente | campo_ausente | 0,57 | 0,91 | sem efeito medido do contexto |
| troca | `contrato-produto` | campo_ausente | campo_ausente | 0,57 | 0,99 | sem efeito medido do contexto |
| sem_documentacao | `` | campo_ausente | campo_ausente | 0,57 | 0,69 | sem efeito medido do contexto |
| repeticao_da_base | `` | campo_ausente | campo_ausente | 0,57 | 0,52 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `imagem` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-3 --sem-seletor`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1476 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:27:38 | caso efe-3 |
| 1478 | 2 | poda | programa | ao_vivo | 2026-11-05T00:27:38 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1479 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:27:38 | poda: escolha json/lista; imagem:ausente; divergência não |
| 1480 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:27:38 | 3 de 39 verbetes entregues |
| 1481 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:27:38 | recuperacao: escolha entidade-produto,contrato-produto,campo_ausente; divergência não |
| 1483 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:27:38 | {"etapa": "diagnostico", "sha": "11a3fe94e7df2dcc", "prompt_sha256": "11a3fe94e7df", "chars": 3419, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1485 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:27:38 | diagnostico: 49,0 s |
| 1486 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:38 | causa_raiz: `campo_ausente` |
| 1487 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:38 | campo: `imagem` |
| 1488 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:38 | impacto: `Os cartões aparecem sem foto nenhuma, pois o campo "imagem" está ausente na resposta da API.` |
| 1489 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:38 | fonte: `[contrato-produto] [campo_ausente]` |
| 1490 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:38 | fonte_citada: `contrato-produto` |
| 1491 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T00:27:38 | fonte_citada: `campo_ausente` |
| 1492 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | quatro_linhas_presentes: confere |
| 1493 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | rotulo_no_conjunto: confere |
| 1494 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | fonte_existe_na_biblioteca: confere |
| 1495 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | fonte_existe_na_biblioteca: confere |
| 1496 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | fonte_estava_no_contexto: confere |
| 1497 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | fonte_estava_no_contexto: confere |
| 1498 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | campo_existe_no_caso: confere |
| 1499 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1500 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | notas_nos_verbetes_citados: informativo |
| 1501 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | impacto: nao_verificavel |
| 1502 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | fonte_formato_valido: confere |
| 1503 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | fonte_contem_termo_da_causa: nao_confere |
| 1504 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T00:27:38 | fonte_contem_termo_da_causa: confere |
| 1507 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:27:38 | intervencao:remocao: 47,7 s |
| 1508 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:27:38 | remocao de contrato-produto: rótulo campo_ausente para campo_ausente |
| 1511 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:27:38 | intervencao:troca: 63,7 s |
| 1512 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:27:38 | troca de contrato-produto: rótulo campo_ausente para campo_ausente |
| 1515 | 31 | inferencia | programa | ao_vivo | 2026-11-05T00:27:38 | intervencao:sem_documentacao: 30,1 s |
| 1516 | 32 | intervencao | verificacao | ao_vivo | 2026-11-05T00:27:38 | sem_documentacao de None: rótulo campo_ausente para campo_ausente |
| 1518 | 33 | inferencia | programa | ao_vivo | 2026-11-05T00:27:38 | intervencao:repeticao_da_base: 13,9 s |
| 1519 | 34 | intervencao | verificacao | ao_vivo | 2026-11-05T00:27:38 | repeticao_da_base de None: rótulo campo_ausente para campo_ausente |
| 1520 | 35 | decisao | programa | ao_vivo | 2026-11-05T00:27:38 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1479, `poda`: escolha `json/lista; imagem:ausente`; resultado sinais_em_codigo; evidência: evento 1478 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: imagem (gen_ai: plan)
- evento 1481, `recuperacao`: escolha `entidade-produto,contrato-produto,campo_ausente`; resultado verbetes_entregues; evidência: evento 1480 (verbete_entregue, entidade-produto), evento 1480 (verbete_entregue, contrato-produto), evento 1480 (verbete_entregue, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: retrieval)
- evento 1520, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1478 (sinal_em_codigo), evento 1480 (verbete_entregue, entidade-produto), evento 1480 (verbete_entregue, contrato-produto), evento 1480 (verbete_entregue, campo_ausente), evento 1485 (resposta), evento 1490 (verbete_citado, contrato-produto), evento 1491 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1476 a 1520 da trilha; hash dos eventos deste caso: `0df43b1dede3d304`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
