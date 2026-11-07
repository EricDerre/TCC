<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-26`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-26@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,95) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada no campo preco porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 8 a 10; a lista completa tem 14.
```

## 3. Contraste com a segunda causa

resposta_truncada e não campo_ausente: a escolha tem probabilidade 0,95 contra 0,02; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,95 | sim |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,01 |  |
| tipo_divergente | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [campo_ausente]` | confere | {"ids": ["contrato-produto", "campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-26 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 646 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:50:52 | caso sin-26 |
| 647 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:50:52 | 3 de 39 verbetes entregues |
| 649 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:50:52 | {"etapa": "diagnostico", "sha": "31236e8fd478f453", "prompt_sha256": "31236e8fd478", "chars": 3917, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 651 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:50:52 | diagnostico: 47,2 s |
| 652 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:50:52 | causa_raiz: `resposta_truncada` |
| 653 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:50:52 | campo: `preco` |
| 654 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:50:52 | impacto: `O usuário vê preços incorretos ou 'undefined' para alguns produtos, devido à lista truncada.` |
| 655 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:50:52 | fonte: `[contrato-produto], [campo_ausente]` |
| 656 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:50:52 | fonte_citada: `contrato-produto` |
| 657 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:50:52 | fonte_citada: `campo_ausente` |
| 658 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | quatro_linhas_presentes: confere |
| 659 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | rotulo_no_conjunto: confere |
| 660 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | fonte_existe_na_biblioteca: confere |
| 661 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | fonte_existe_na_biblioteca: confere |
| 662 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | fonte_estava_no_contexto: confere |
| 663 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | fonte_estava_no_contexto: confere |
| 664 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | campo_existe_no_caso: confere |
| 665 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 666 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | notas_nos_verbetes_citados: informativo |
| 667 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | impacto: nao_verificavel |
| 668 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | fonte_formato_valido: confere |
| 669 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | fonte_contem_termo_da_causa: nao_confere |
| 670 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:50:52 | fonte_contem_termo_da_causa: nao_confere |
| 671 | 24 | decisao | programa | ao_vivo | 2026-11-06T11:50:52 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 671, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 647 (verbete_entregue, entidade-produto), evento 647 (verbete_entregue, contrato-produto), evento 647 (verbete_entregue, campo_ausente), evento 651 (resposta), evento 656 (verbete_citado, contrato-produto), evento 657 (verbete_citado, campo_ausente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 646 a 671 da trilha; hash dos eventos deste caso: `5f30575df0041b4d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
