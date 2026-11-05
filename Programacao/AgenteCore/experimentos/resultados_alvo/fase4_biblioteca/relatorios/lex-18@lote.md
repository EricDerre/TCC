<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-18@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `resumo` · selo de probabilidade: **baixo** (p = 0,33) · **CONFLITO**: nenhum verbete entregue trata da causa respondida valor_fora_do_dominio

**IMPACTO (declarado):** `O usuário vê o resumo com caracteres inválidos e um nome corretamente formatado.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo resumo porque os verbetes contrato-produto, entidade-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, codificacao_incorreta, ficou com probabilidade 0,24 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida valor_fora_do_dominio. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,33); trate como hipótese e confira o campo resumo antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}]

SINTOMA OBSERVADO: O card da Agua Mineral mostra o resumo como 'Garrafa 500ml, com ou sem gÃ¡s'; o nome do produto, logo acima no mesmo card, aparece com o acento certo ('Água').

OBSERVAÇÃO ADICIONAL: So o campo resumo veio com os bytes trocados; nome, no mesmo item, chegou certo — nao e um problema de charset da resposta inteira.
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não codificacao_incorreta: a escolha tem probabilidade 0,33 contra 0,24; verbete(s) na evidência: contrato-produto, entidade-produto, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,33 | sim |
| codificacao_incorreta | 0,24 |  |
| chave_de_juncao_errada | 0,15 |  |
| formato_de_data_divergente | 0,12 |  |
| campo_ausente | 0,09 |  |
| campo_renomeado | 0,09 |  |
| tipo_divergente | 0,04 |  |
| escala_ou_unidade_errada | 0,02 |  |
| nulo_inesperado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2043 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:39:44 | caso lex-18 |
| 2044 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:39:44 | 3 de 46 verbetes entregues |
| 2046 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:39:44 | {"chars": 4040, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "e5f18880480c", "sha": "e5f18880480c7560"} |
| 2048 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:39:44 | diagnostico: 74,1 s |
| 2049 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:39:44 | causa_raiz: `valor_fora_do_dominio` |
| 2050 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:39:44 | campo: `resumo` |
| 2051 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:39:44 | impacto: `O usuário vê o resumo com caracteres inválidos e um nome corretamente formatado.` |
| 2052 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:39:44 | fonte: `[contrato-produto]` |
| 2053 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:39:44 | fonte_citada: `contrato-produto` |
| 2054 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | quatro_linhas_presentes: confere |
| 2055 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | rotulo_no_conjunto: confere |
| 2056 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | fonte_existe_na_biblioteca: confere |
| 2057 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | fonte_estava_no_contexto: confere |
| 2058 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | campo_existe_no_caso: confere |
| 2059 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2060 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | notas_nos_verbetes_citados: informativo |
| 2061 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | impacto: nao_verificavel |
| 2062 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | fonte_formato_valido: confere |
| 2063 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:39:44 | fonte_contem_termo_da_causa: nao_confere |
| 2064 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:39:44 | diagnostico: escolha valor_fora_do_dominio; divergência sim |

</details>

Nós de decisão:

- evento 2064, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 2044 (verbete_entregue, contrato-produto), evento 2044 (verbete_entregue, entidade-produto), evento 2044 (verbete_entregue, estado_da_tela_divergente), evento 2048 (resposta), evento 2053 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, entidade-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2043 a 2064 da trilha; hash dos eventos deste caso: `8bd1437539fac6f5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
