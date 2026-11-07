<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-26`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-26@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `resumo` · selo de probabilidade: **medio** (p = 0,91)

**IMPACTO (declarado):** `O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo resumo porque os verbetes contrato-produto, nulo_inesperado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,03. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/12

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}

SINTOMA OBSERVADO: O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200.

OBSERVAÇÃO ADICIONAL: A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 12) com o resumo preenchido. O contrato permite resumo nulo (texto|nulo).
```

## 3. Contraste com a segunda causa

nulo_inesperado e não campo_ausente: a escolha tem probabilidade 0,91 contra 0,03; verbete(s) na evidência: contrato-produto, nulo_inesperado, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,91 | sim |
| campo_ausente | 0,03 |  |
| campo_renomeado | 0,03 |  |
| chave_de_juncao_errada | 0,03 |  |
| valor_fora_do_dominio | 0,01 |  |
| tipo_divergente | 0,01 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `contrato-produto`, `nulo_inesperado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-26 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 967 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:02:16 | caso semt-26 |
| 968 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:02:16 | 3 de 39 verbetes entregues |
| 970 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:02:16 | {"etapa": "diagnostico", "sha": "98b4b66224a59fec", "prompt_sha256": "98b4b66224a5", "chars": 3672, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 972 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:02:16 | diagnostico: 64,6 s |
| 973 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:02:16 | causa_raiz: `nulo_inesperado` |
| 974 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:02:16 | campo: `resumo` |
| 975 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:02:16 | impacto: `O usuário vê uma descrição no cardápio, mas no modal, o campo 'Saiba Mais...' está vazio.` |
| 976 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:02:16 | fonte: `[nulo_inesperado]` |
| 977 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:02:16 | fonte_citada: `nulo_inesperado` |
| 978 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | quatro_linhas_presentes: confere |
| 979 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | rotulo_no_conjunto: confere |
| 980 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | fonte_existe_na_biblioteca: confere |
| 981 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | fonte_estava_no_contexto: confere |
| 982 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | campo_existe_no_caso: confere |
| 983 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 984 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | notas_nos_verbetes_citados: informativo |
| 985 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | impacto: nao_verificavel |
| 986 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | fonte_formato_valido: confere |
| 987 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:02:16 | fonte_contem_termo_da_causa: confere |
| 988 | 20 | decisao | programa | ao_vivo | 2026-11-06T12:02:16 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 988, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 968 (verbete_entregue, contrato-produto), evento 968 (verbete_entregue, nulo_inesperado), evento 968 (verbete_entregue, entidade-produto), evento 972 (resposta), evento 977 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: contrato-produto, nulo_inesperado, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 967 a 988 da trilha; hash dos eventos deste caso: `34c731bfd4d62e10`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
