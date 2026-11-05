<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/run-1@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete erro_interno_do_servidor não mudou a resposta: sem efeito medido do contexto. A troca do verbete erro_interno_do_servidor por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

O caso, como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "erro interno (fault injection)"}

SINTOMA OBSERVADO: A aba de produtos via API mostra a mensagem de erro ao carregar.
```

Poda de `corpo_http` (evento 1026): regras diff_contra_contrato; antes {"chars": 44}, depois {"chars": 44}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| detail |  | texto |

Trecho podado (hash `6b438745dff984ef`):

```text
{"detail": "erro interno (fault injection)"}
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,98 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["erro_interno_do_servidor"]} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `erro_interno_do_servidor` | erro_interno_do_servidor | erro_interno_do_servidor | 0,98 | 1,00 | sem efeito medido do contexto |
| troca | `erro_interno_do_servidor` | erro_interno_do_servidor | erro_interno_do_servidor | 0,98 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | não se aplica | erro_interno_do_servidor | erro_interno_do_servidor | 0,98 | 1,00 | sem documentação a resposta fica a mesma |
| repeticao_da_base | não se aplica | erro_interno_do_servidor | erro_interno_do_servidor | 0,98 | 0,98 | o mesmo prompt manteve o rótulo |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids run-1 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1024 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:59:06 | caso run-1 |
| 1026 | 2 | poda | programa | ao_vivo | 2026-11-04T23:59:06 | corpo_http: 8 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1027 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:59:06 | poda: escolha json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado; divergência não |
| 1028 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:59:06 | 3 de 39 verbetes entregues |
| 1029 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:59:06 | recuperacao: escolha erro_interno_do_servidor,mensagens-de-erro-do-codigo,contagem_inconsistente; divergência não |
| 1031 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:59:06 | {"chars": 3503, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "4933583fbab8", "sha": "4933583fbab8816a"} |
| 1033 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:59:06 | diagnostico: 71,2 s |
| 1034 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:59:06 | causa_raiz: `erro_interno_do_servidor` |
| 1035 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:59:06 | campo: `nenhum` |
| 1036 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:59:06 | impacto: `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".` |
| 1037 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:59:06 | fonte: `[erro_interno_do_servidor]` |
| 1038 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:59:06 | fonte_citada: `erro_interno_do_servidor` |
| 1039 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | quatro_linhas_presentes: confere |
| 1040 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | rotulo_no_conjunto: confere |
| 1041 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | fonte_existe_na_biblioteca: confere |
| 1042 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | fonte_estava_no_contexto: confere |
| 1043 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | campo_existe_no_caso: nao_se_aplica |
| 1044 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1045 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | notas_nos_verbetes_citados: informativo |
| 1046 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | impacto: nao_verificavel |
| 1047 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | fonte_formato_valido: confere |
| 1048 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:59:06 | fonte_contem_termo_da_causa: confere |
| 1051 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:59:06 | intervencao:remocao: 61,1 s |
| 1052 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:59:06 | remocao de erro_interno_do_servidor: rótulo erro_interno_do_servidor para erro_interno_do_servidor |
| 1055 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:59:06 | intervencao:troca: 70,3 s |
| 1056 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:59:06 | troca de erro_interno_do_servidor: rótulo erro_interno_do_servidor para erro_interno_do_servidor |
| 1059 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:59:06 | intervencao:sem_documentacao: 36,9 s |
| 1060 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:59:06 | sem_documentacao de None: rótulo erro_interno_do_servidor para erro_interno_do_servidor |
| 1061 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:59:06 | intervencao:repeticao_da_base: 17,2 s |
| 1062 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:59:06 | repeticao_da_base de None: rótulo erro_interno_do_servidor para erro_interno_do_servidor |
| 1063 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:59:06 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 1027, `poda`: escolha `json/objeto; id:ausente, nome:ausente, resumo:ausente, tipo:ausente, preco:ausente, imagem:ausente, destaque:ausente, detail:inesperado`; resultado sinais_em_codigo; evidência: evento 1026 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, nome, resumo, tipo, preco, imagem, destaque, detail (gen_ai: plan)
- evento 1029, `recuperacao`: escolha `erro_interno_do_servidor,mensagens-de-erro-do-codigo,contagem_inconsistente`; resultado verbetes_entregues; evidência: evento 1028 (verbete_entregue, erro_interno_do_servidor), evento 1028 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1028 (verbete_entregue, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente (gen_ai: retrieval)
- evento 1063, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 1026 (sinal_em_codigo), evento 1028 (verbete_entregue, erro_interno_do_servidor), evento 1028 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1028 (verbete_entregue, contagem_inconsistente), evento 1033 (resposta), evento 1038 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1024 a 1063 da trilha; hash dos eventos deste caso: `624c4e888d8c01b3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
