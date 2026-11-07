<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-27`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-27@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **baixo** (p = 0,64)

**IMPACTO (declarado):** `O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a API retorna uma lista em vez de um objeto.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,18. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,64); trate como hipótese e confira o campo id antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": -2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": -3, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]

SINTOMA OBSERVADO: A grade carrega os 14 cartoes sem erro, mas qualquer 'Saiba Mais...' abre o modal com 'Erro' no titulo e 'HTTP 404' no corpo. Ao clicar no botao da Picanha ao Alho, a requisicao disparada foi GET /api/produtos/-2 e a resposta foi 404.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens da Picanha ao Alho e da Picanha Simples; a lista completa tem 14.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não campo_ausente: a escolha tem probabilidade 0,64 contra 0,18; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,64 | sim |
| campo_ausente | 0,18 |  |
| campo_renomeado | 0,18 |  |
| resposta_truncada | 0,07 |  |
| tipo_divergente | 0,05 |  |
| estrutura_aninhada_divergente | 0,04 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-27 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1027 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:05:19 | caso semt-27 |
| 1028 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:05:19 | 3 de 39 verbetes entregues |
| 1030 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:05:19 | {"etapa": "diagnostico", "sha": "195bce3574fbfd2d", "prompt_sha256": "195bce3574fb", "chars": 4108, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1032 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:05:19 | diagnostico: 65,4 s |
| 1033 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:05:19 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 1034 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:05:19 | campo: `id` |
| 1035 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:05:19 | impacto: `O usuário vê um erro ao tentar acessar detalhes de um produto específico, pois a API retorna uma lista em vez de um objeto.` |
| 1036 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:05:19 | fonte: `[contrato-produto]` |
| 1037 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:05:19 | fonte_citada: `contrato-produto` |
| 1038 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | quatro_linhas_presentes: confere |
| 1039 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | rotulo_no_conjunto: confere |
| 1040 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | fonte_existe_na_biblioteca: confere |
| 1041 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | fonte_estava_no_contexto: confere |
| 1042 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | campo_existe_no_caso: confere |
| 1043 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1044 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | notas_nos_verbetes_citados: informativo |
| 1045 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | impacto: nao_verificavel |
| 1046 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | fonte_formato_valido: confere |
| 1047 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:05:19 | fonte_contem_termo_da_causa: nao_confere |
| 1048 | 20 | decisao | programa | ao_vivo | 2026-11-06T12:05:19 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 1048, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 1028 (verbete_entregue, entidade-produto), evento 1028 (verbete_entregue, contrato-produto), evento 1028 (verbete_entregue, estrutura_aninhada_divergente), evento 1032 (resposta), evento 1037 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1027 a 1048 da trilha; hash dos eventos deste caso: `f895c2c9f0d7267d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
