<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-21@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo tipo porque os verbetes estrutura_aninhada_divergente, entidade-produto, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "{'id': 1, 'nome': 'Carnes'}", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria do produto aparece como o texto literal {'id': 1, 'nome': 'Carnes'} no card (aspas simples, no estilo de repr do Python), em vez de 'Carnes' — diferente de um objeto de verdade, que apareceria como [object Object].

OBSERVAÇÃO ADICIONAL: tipo e uma STRING cujo conteudo por acaso parece um dicionario serializado errado (aspas simples); nao e um objeto JSON aninhado de verdade, por isso o card nao mostra [object Object].
```

## 3. Contraste com a segunda causa

estrutura_aninhada_divergente e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: estrutura_aninhada_divergente, entidade-produto, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente]`; verbetes citados: `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[estrutura_aninhada_divergente]` | confere | {"ids": ["estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-21 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1638 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:13:14 | caso sin-21 |
| 1639 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:13:14 | 3 de 40 verbetes entregues |
| 1641 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:13:14 | {"etapa": "diagnostico", "sha": "eb454549ca8ff42f", "prompt_sha256": "eb454549ca8f", "chars": 3879, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1643 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:13:14 | diagnostico: 73,2 s |
| 1644 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:13:14 | causa_raiz: `estrutura_aninhada_divergente` |
| 1645 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:13:14 | campo: `tipo` |
| 1646 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:13:14 | impacto: `O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.` |
| 1647 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:13:14 | fonte: `[estrutura_aninhada_divergente]` |
| 1648 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:13:14 | fonte_citada: `estrutura_aninhada_divergente` |
| 1649 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | quatro_linhas_presentes: confere |
| 1650 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | rotulo_no_conjunto: confere |
| 1651 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | fonte_existe_na_biblioteca: confere |
| 1652 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | fonte_estava_no_contexto: confere |
| 1653 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | campo_existe_no_caso: confere |
| 1654 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1655 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | notas_nos_verbetes_citados: informativo |
| 1656 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | impacto: nao_verificavel |
| 1657 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | fonte_formato_valido: confere |
| 1658 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:13:14 | fonte_contem_termo_da_causa: confere |
| 1659 | 20 | decisao | programa | ao_vivo | 2026-11-01T12:13:14 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 1659, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 1639 (verbete_entregue, estrutura_aninhada_divergente), evento 1639 (verbete_entregue, entidade-produto), evento 1639 (verbete_entregue, pagina-produtos-api), evento 1643 (resposta), evento 1648 (verbete_citado, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: estrutura_aninhada_divergente, entidade-produto, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1638 a 1659 da trilha; hash dos eventos deste caso: `39f700a7e70eb266`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
