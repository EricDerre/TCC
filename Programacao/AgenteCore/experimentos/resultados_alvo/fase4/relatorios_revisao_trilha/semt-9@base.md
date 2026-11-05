<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-9@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O produto Picanha ao Alho aparece na seção de destaque, mesmo não estando marcado como destaque no cadastro.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal destaque: esperado booleano, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete tipo_divergente não mudou a resposta: sem efeito medido do contexto. A troca do verbete tipo_divergente por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

O caso, como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": 2}]

SINTOMA OBSERVADO: O produto aparece na secao de destaques mesmo nao estando marcado no cadastro.
```

Poda de `corpo_http` (evento 2688): regras diff_contra_contrato; antes {"chars": 146}, depois {"chars": 146}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano | inteiro |

Trecho podado (hash `2203e279e833f5c4`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": 2}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["tipo_divergente"]} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `tipo_divergente` | tipo_divergente | tipo_divergente | 1,00 | 0,88 | sem efeito medido do contexto |
| troca | `tipo_divergente` | tipo_divergente | tipo_divergente | 1,00 | 0,43 | sem efeito medido do contexto |
| sem_documentacao | não se aplica | tipo_divergente | tipo_divergente | 1,00 | 0,58 | sem documentação a resposta fica a mesma |
| repeticao_da_base | não se aplica | tipo_divergente | tipo_divergente | 1,00 | 1,00 | o mesmo prompt manteve o rótulo |

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-9 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2686 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:32:13 | caso semt-9 |
| 2688 | 2 | poda | programa | ao_vivo | 2026-11-05T01:32:13 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2689 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:32:13 | poda: escolha json/lista; destaque:tipo_diferente; divergência não |
| 2690 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:32:13 | 3 de 39 verbetes entregues |
| 2691 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:32:13 | recuperacao: escolha entidade-produto,contrato-produto,tipo_divergente; divergência não |
| 2693 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:32:13 | {"chars": 3558, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "94bb644b83ad", "sha": "94bb644b83ad84aa"} |
| 2695 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:32:13 | diagnostico: 37,9 s |
| 2696 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:32:13 | causa_raiz: `tipo_divergente` |
| 2697 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:32:13 | campo: `destaque` |
| 2698 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:32:13 | impacto: `O produto Picanha ao Alho aparece na seção de destaque, mesmo não estando marcado como destaque no cadastro.` |
| 2699 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:32:13 | fonte: `[tipo_divergente]` |
| 2700 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:32:13 | fonte_citada: `tipo_divergente` |
| 2701 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | quatro_linhas_presentes: confere |
| 2702 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | rotulo_no_conjunto: confere |
| 2703 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | fonte_existe_na_biblioteca: confere |
| 2704 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | fonte_estava_no_contexto: confere |
| 2705 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | campo_existe_no_caso: confere |
| 2706 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2707 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | notas_nos_verbetes_citados: informativo |
| 2708 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | impacto: nao_verificavel |
| 2709 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | fonte_formato_valido: confere |
| 2710 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:32:13 | fonte_contem_termo_da_causa: confere |
| 2713 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:32:13 | intervencao:remocao: 43,0 s |
| 2714 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:32:13 | remocao de tipo_divergente: rótulo tipo_divergente para tipo_divergente |
| 2717 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:32:13 | intervencao:troca: 55,6 s |
| 2718 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:32:13 | troca de tipo_divergente: rótulo tipo_divergente para tipo_divergente |
| 2721 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:32:13 | intervencao:sem_documentacao: 31,4 s |
| 2722 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:32:13 | sem_documentacao de None: rótulo tipo_divergente para tipo_divergente |
| 2723 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:32:13 | intervencao:repeticao_da_base: 16,2 s |
| 2724 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:32:13 | repeticao_da_base de None: rótulo tipo_divergente para tipo_divergente |
| 2725 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:32:13 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2689, `poda`: escolha `json/lista; destaque:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 2688 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: destaque (gen_ai: plan)
- evento 2691, `recuperacao`: escolha `entidade-produto,contrato-produto,tipo_divergente`; resultado verbetes_entregues; evidência: evento 2690 (verbete_entregue, entidade-produto), evento 2690 (verbete_entregue, contrato-produto), evento 2690 (verbete_entregue, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: retrieval)
- evento 2725, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2688 (sinal_em_codigo), evento 2690 (verbete_entregue, entidade-produto), evento 2690 (verbete_entregue, contrato-produto), evento 2690 (verbete_entregue, tipo_divergente), evento 2695 (resposta), evento 2700 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2686 a 2725 da trilha; hash dos eventos deste caso: `898f3a955555d0a1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
