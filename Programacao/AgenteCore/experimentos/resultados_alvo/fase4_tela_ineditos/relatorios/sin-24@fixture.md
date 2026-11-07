<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-24@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **baixo** (p = 0,77)

**IMPACTO (declarado):** `O usuário vê a categoria de cada produto acompanhada por informações adicionais não desejadas, como {"valor":"Carnes","moeda":"BRL"}, em vez de apenas o nome da categoria.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo tipo porque os verbetes contrato-produto, entidade-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,10. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,77); trate como hipótese e confira o campo tipo antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal.
```

## 3. Contraste com a segunda causa

estrutura_aninhada_divergente e não campo_ausente: a escolha tem probabilidade 0,77 contra 0,10; verbete(s) na evidência: contrato-produto, entidade-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 0,77 | sim |
| campo_ausente | 0,10 |  |
| campo_renomeado | 0,10 |  |
| chave_de_juncao_errada | 0,10 |  |
| tipo_divergente | 0,03 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto] [estrutura_aninhada_divergente]`; verbetes citados: `entidade-produto`, `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `contrato-produto`, `entidade-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[entidade-produto] [estrutura_aninhada_divergente]` | confere | {"ids": ["entidade-produto", "estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "estrutura_aninhada_divergente"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-24 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 513 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:46:00 | caso sin-24 |
| 514 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:46:00 | 3 de 39 verbetes entregues |
| 516 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:46:00 | {"etapa": "diagnostico", "sha": "f7575fc7c33092ef", "prompt_sha256": "f7575fc7c330", "chars": 3953, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 518 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:46:00 | diagnostico: 67,6 s |
| 519 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:46:00 | causa_raiz: `estrutura_aninhada_divergente` |
| 520 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:46:00 | campo: `tipo` |
| 521 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:46:00 | impacto: `O usuário vê a categoria de cada produto acompanhada por informações adicionais não desejadas, como {"valor":"Carnes","moeda":"BRL"}, em vez de apenas o nome da categoria.` |
| 522 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:46:00 | fonte: `[entidade-produto] [estrutura_aninhada_divergente]` |
| 523 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:46:00 | fonte_citada: `entidade-produto` |
| 524 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:46:00 | fonte_citada: `estrutura_aninhada_divergente` |
| 525 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | quatro_linhas_presentes: confere |
| 526 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | rotulo_no_conjunto: confere |
| 527 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | fonte_existe_na_biblioteca: confere |
| 528 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | fonte_existe_na_biblioteca: confere |
| 529 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | fonte_estava_no_contexto: confere |
| 530 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | fonte_estava_no_contexto: confere |
| 531 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | campo_existe_no_caso: confere |
| 532 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 533 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | notas_nos_verbetes_citados: informativo |
| 534 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | impacto: nao_verificavel |
| 535 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | fonte_formato_valido: confere |
| 536 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | fonte_contem_termo_da_causa: nao_confere |
| 537 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:46:00 | fonte_contem_termo_da_causa: confere |
| 538 | 24 | decisao | programa | ao_vivo | 2026-11-06T11:46:00 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 538, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 514 (verbete_entregue, contrato-produto), evento 514 (verbete_entregue, entidade-produto), evento 514 (verbete_entregue, estrutura_aninhada_divergente), evento 518 (resposta), evento 523 (verbete_citado, entidade-produto), evento 524 (verbete_citado, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 513 a 538 da trilha; hash dos eventos deste caso: `f6b4db53858073b1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
