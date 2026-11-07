<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-10`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/lex-10@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque os verbetes entidade-produto, resposta_truncada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre

SINTOMA OBSERVADO: A lista carrega parcialmente. So acontece quando ha mais de 10 produtos.

OBSERVAÇÃO ADICIONAL: Content-Length declara 4096; o corpo recebido tem 4096 bytes exatos.
```

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, resposta_truncada, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| limite_de_requisicoes | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada] [contrato-produto]`; verbetes citados: `resposta_truncada`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada] [contrato-produto]` | confere | {"ids": ["resposta_truncada", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids lex-10 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 761 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:07:38 | caso lex-10 |
| 762 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:07:38 | 3 de 39 verbetes entregues |
| 764 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:07:38 | {"etapa": "diagnostico", "sha": "eb7cf66afb2f0013", "prompt_sha256": "eb7cf66afb2f", "chars": 3823, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 766 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:07:38 | diagnostico: 75,7 s |
| 767 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:07:38 | causa_raiz: `resposta_truncada` |
| 768 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:07:38 | campo: `nenhum` |
| 769 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:07:38 | impacto: `O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.` |
| 770 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:07:38 | fonte: `[resposta_truncada] [contrato-produto]` |
| 771 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:07:38 | fonte_citada: `resposta_truncada` |
| 772 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T19:07:38 | fonte_citada: `contrato-produto` |
| 773 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | quatro_linhas_presentes: confere |
| 774 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | rotulo_no_conjunto: confere |
| 775 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | fonte_existe_na_biblioteca: confere |
| 776 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | fonte_existe_na_biblioteca: confere |
| 777 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | fonte_estava_no_contexto: confere |
| 778 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | fonte_estava_no_contexto: confere |
| 779 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | campo_existe_no_caso: nao_se_aplica |
| 780 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 781 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | notas_nos_verbetes_citados: informativo |
| 782 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | impacto: nao_verificavel |
| 783 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | fonte_formato_valido: confere |
| 784 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | fonte_contem_termo_da_causa: confere |
| 785 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:07:38 | fonte_contem_termo_da_causa: nao_confere |
| 786 | 24 | decisao | programa | ao_vivo | 2026-11-05T19:07:38 | diagnostico: escolha resposta_truncada; divergência não |

</details>

Nós de decisão:

- evento 786, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 762 (verbete_entregue, entidade-produto), evento 762 (verbete_entregue, resposta_truncada), evento 762 (verbete_entregue, contrato-produto), evento 766 (resposta), evento 771 (verbete_citado, resposta_truncada), evento 772 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, resposta_truncada, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 761 a 786 da trilha; hash dos eventos deste caso: `ec1806ac55aafec5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
