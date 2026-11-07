<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-10`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/lex-10@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-10 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 752 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:22:56 | caso lex-10 |
| 753 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:22:56 | 3 de 39 verbetes entregues |
| 755 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:22:56 | {"etapa": "diagnostico", "sha": "eb7cf66afb2f0013", "prompt_sha256": "eb7cf66afb2f", "chars": 3823, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 757 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:22:56 | diagnostico: 75,5 s |
| 758 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | causa_raiz: `resposta_truncada` |
| 759 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | campo: `nenhum` |
| 760 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | impacto: `O usuário vê uma lista incompleta de produtos, com apenas os dois primeiros itens exibidos.` |
| 761 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | fonte: `[resposta_truncada] [contrato-produto]` |
| 762 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | fonte_citada: `resposta_truncada` |
| 763 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T10:22:56 | fonte_citada: `contrato-produto` |
| 764 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | quatro_linhas_presentes: confere |
| 765 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | rotulo_no_conjunto: confere |
| 766 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_existe_na_biblioteca: confere |
| 767 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_existe_na_biblioteca: confere |
| 768 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_estava_no_contexto: confere |
| 769 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_estava_no_contexto: confere |
| 770 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | campo_existe_no_caso: nao_se_aplica |
| 771 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 772 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | notas_nos_verbetes_citados: informativo |
| 773 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | impacto: nao_verificavel |
| 774 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_formato_valido: confere |
| 775 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_contem_termo_da_causa: confere |
| 776 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:22:56 | fonte_contem_termo_da_causa: nao_confere |
| 777 | 24 | decisao | programa | ao_vivo | 2026-11-06T10:22:56 | diagnostico: escolha resposta_truncada; divergência não |

</details>

Nós de decisão:

- evento 777, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 753 (verbete_entregue, entidade-produto), evento 753 (verbete_entregue, resposta_truncada), evento 753 (verbete_entregue, contrato-produto), evento 757 (resposta), evento 762 (verbete_citado, resposta_truncada), evento 763 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, resposta_truncada, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 752 a 777 da trilha; hash dos eventos deste caso: `8e4cee2e8947d393`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
